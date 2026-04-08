from __future__ import annotations

import hashlib
import secrets
from collections import Counter, defaultdict
from datetime import datetime

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload

from .database import Base, engine, get_db
from .models import (
    Course,
    CourseDocument,
    Exercise,
    ExerciseAttempt,
    PortfolioEntry,
    Quest,
    QuestSubmission,
    QuizAttempt,
    QuizQuestion,
    RewardRedemption,
    TeamChallenge,
    TeamChallengeSubmission,
    TeacherFeedback,
    User,
)
from .schemas import (
    AchievementOut,
    AttemptCreate,
    AttemptResult,
    CourseOut,
    DashboardOut,
    ExerciseOut,
    LeaderboardEntry,
    LoginRequest,
    LoginResponse,
    MasteryItem,
    PortfolioCreate,
    PortfolioOut,
    QuestOut,
    QuizOut,
    ReviewQueueItemOut,
    ShowcaseOut,
    SubmissionOut,
    TeamAttemptCreate,
    TeamChallengeOut,
    TeamLeaderboardEntry,
    TeacherFeedbackCreate,
    TeacherFeedbackOut,
    TeacherOverview,
    TutorQuery,
    TutorResponse,
    UserOut,
)
from .seed_data import COURSES, COURSE_DOCUMENTS, EXERCISES, QUESTS, QUIZZES, TEAM_CHALLENGES, USERS
from .services.feedback_engine import build_llm_feedback, evaluate_item
from .services.gamification import update_progress
from .services.learner_model import classify_learner_state, get_or_create_mastery, update_mastery
from .services.rag import RagService

app = FastAPI(title="EduQuest AI API", version="5.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_service = RagService()
SESSIONS: dict[str, int] = {}


# ---------- helpers ----------

def verify_password(password: str, stored_hash: str) -> bool:
    return hashlib.sha256(password.encode("utf-8")).hexdigest() == stored_hash


def seed_if_needed(db: Session) -> None:
    if not db.query(User).first():
        for item in USERS:
            db.add(User(**item))
    if not db.query(Course).first():
        for item in COURSES:
            db.add(Course(**item))
        db.flush()
        course_map = {course.slug: course.id for course in db.query(Course).all()}
        for item in QUESTS:
            db.add(Quest(**item))
        for item in QUIZZES:
            payload = dict(item)
            course_slug = payload.pop("course_slug")
            db.add(QuizQuestion(course_id=course_map[course_slug], **payload))
        for item in EXERCISES:
            payload = dict(item)
            course_slug = payload.pop("course_slug")
            db.add(Exercise(course_id=course_map[course_slug], **payload))
        for item in COURSE_DOCUMENTS:
            db.add(CourseDocument(**item))
    if not db.query(TeamChallenge).first():
        for item in TEAM_CHALLENGES:
            db.add(TeamChallenge(**item))
    db.commit()


def get_current_user(authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing auth token")
    token = authorization.replace("Bearer ", "", 1)
    user_id = SESSIONS.get(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def require_teacher(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Teacher access required")
    return current_user


def is_bonus_unlocked(db: Session, user_id: int, course: Course) -> bool:
    if not course.bonus_reward_code:
        return False
    return (
        db.query(RewardRedemption)
        .filter(RewardRedemption.user_id == user_id, RewardRedemption.reward_code == course.bonus_reward_code)
        .first()
        is not None
    )


def course_out(course: Course, unlocked: bool = False) -> CourseOut:
    return CourseOut(
        id=course.id,
        title=course.title,
        slug=course.slug,
        category=course.category,
        level=course.level,
        duration=course.duration,
        description=course.description,
        learning_outcomes=course.learning_outcomes,
        lessons_json=course.lessons_json,
        bonus_reward_code=course.bonus_reward_code,
        bonus_reward_cost=course.bonus_reward_cost,
        bonus_module_title=course.bonus_module_title,
        bonus_module_content=course.bonus_module_content,
        bonus_unlocked=unlocked,
    )


def all_attempts_for_user(db: Session, user_id: int) -> list[dict]:
    activity = []
    quests = db.query(QuestSubmission).options(joinedload(QuestSubmission.quest)).filter(QuestSubmission.user_id == user_id).all()
    quizzes = db.query(QuizAttempt).options(joinedload(QuizAttempt.quiz)).filter(QuizAttempt.user_id == user_id).all()
    exercises = db.query(ExerciseAttempt).options(joinedload(ExerciseAttempt.exercise)).filter(ExerciseAttempt.user_id == user_id).all()
    teams = db.query(TeamChallengeSubmission).options(joinedload(TeamChallengeSubmission.challenge)).filter(TeamChallengeSubmission.user_id == user_id).all()
    activity.extend({"item_type": "quest", "item_title": row.quest.title, "is_correct": row.is_correct, "created_at": row.created_at} for row in quests)
    activity.extend({"item_type": "quiz", "item_title": row.quiz.title, "is_correct": row.is_correct, "created_at": row.created_at} for row in quizzes)
    activity.extend({"item_type": "exercise", "item_title": row.exercise.title, "is_correct": row.is_correct, "created_at": row.created_at} for row in exercises)
    activity.extend({"item_type": "team", "item_title": row.challenge.title, "is_correct": row.is_correct, "created_at": row.created_at} for row in teams)
    activity.sort(key=lambda x: x["created_at"], reverse=True)
    return activity


def compute_learner_state(db: Session, user_id: int) -> tuple[float, float, str]:
    attempts = (
        db.query(QuestSubmission).filter(QuestSubmission.user_id == user_id).all()
        + db.query(QuizAttempt).filter(QuizAttempt.user_id == user_id).all()
        + db.query(ExerciseAttempt).filter(ExerciseAttempt.user_id == user_id).all()
        + db.query(TeamChallengeSubmission).filter(TeamChallengeSubmission.user_id == user_id).all()
    )
    accuracy = sum(1 for row in attempts if row.is_correct) / max(1, len(attempts))
    recent = attempts[-5:]
    avg_hints = sum(row.hints_used for row in recent) / max(1, len(recent)) if recent else 0
    return accuracy, avg_hints, classify_learner_state(accuracy, avg_hints)


def build_achievements(db: Session, user: User) -> list[AchievementOut]:
    achievements: list[AchievementOut] = []

    seen_badges = set()
    correct_quests = (
        db.query(QuestSubmission)
        .options(joinedload(QuestSubmission.quest))
        .filter(QuestSubmission.user_id == user.id, QuestSubmission.is_correct == True)  # noqa: E712
        .all()
    )
    for row in correct_quests:
        quest = row.quest
        if quest.badge_name in seen_badges:
            continue
        seen_badges.add(quest.badge_name)
        achievements.append(
            AchievementOut(
                id=f"quest-{quest.id}",
                title=quest.badge_name,
                kind="Quest Badge",
                issuer="EduQuest AI",
                issued_on=row.created_at.date().isoformat(),
                skill_tag=quest.skill_tag,
                description=f"Awarded for completing the quest '{quest.title}'.",
                share_path=f"/showcase/{user.id}",
            )
        )

    correct_team = (
        db.query(TeamChallengeSubmission)
        .options(joinedload(TeamChallengeSubmission.challenge))
        .filter(TeamChallengeSubmission.user_id == user.id, TeamChallengeSubmission.is_correct == True)  # noqa: E712
        .all()
    )
    for row in correct_team:
        challenge = row.challenge
        if challenge.badge_name in seen_badges:
            continue
        seen_badges.add(challenge.badge_name)
        achievements.append(
            AchievementOut(
                id=f"team-{challenge.id}",
                title=challenge.badge_name,
                kind="Collaboration Badge",
                issuer="EduQuest AI",
                issued_on=row.created_at.date().isoformat(),
                skill_tag=challenge.skill_tag,
                description=f"Awarded for collaborative completion of '{challenge.title}'.",
                share_path=f"/showcase/{user.id}",
            )
        )

    for mastery in user.mastery_entries:
        if mastery.mastery >= 0.75 and mastery.attempts >= 2:
            achievements.append(
                AchievementOut(
                    id=f"mastery-{mastery.skill_tag}",
                    title=f"Skill Badge · {mastery.skill_tag.replace('_', ' ').title()}",
                    kind="Skill Badge",
                    issuer="EduQuest AI",
                    issued_on=datetime.utcnow().date().isoformat(),
                    skill_tag=mastery.skill_tag,
                    description=f"Demonstrates consistent performance with {round(mastery.mastery * 100)}% mastery.",
                    share_path=f"/showcase/{user.id}",
                )
            )

    for course in db.query(Course).all():
        total_quizzes = db.query(QuizQuestion).filter(QuizQuestion.course_id == course.id).count()
        total_exercises = db.query(Exercise).filter(Exercise.course_id == course.id).count()
        passed_quizzes = (
            db.query(QuizAttempt)
            .join(QuizQuestion)
            .filter(QuizAttempt.user_id == user.id, QuizAttempt.is_correct == True, QuizQuestion.course_id == course.id)  # noqa: E712
            .distinct(QuizAttempt.quiz_id)
            .count()
        )
        passed_exercises = (
            db.query(ExerciseAttempt)
            .join(Exercise)
            .filter(ExerciseAttempt.user_id == user.id, ExerciseAttempt.is_correct == True, Exercise.course_id == course.id)  # noqa: E712
            .distinct(ExerciseAttempt.exercise_id)
            .count()
        )
        if total_quizzes and total_exercises and passed_quizzes >= total_quizzes and passed_exercises >= total_exercises:
            achievements.append(
                AchievementOut(
                    id=f"course-{course.slug}",
                    title=f"Certificate · {course.title}",
                    kind="Course Certificate",
                    issuer="EduQuest AI",
                    issued_on=datetime.utcnow().date().isoformat(),
                    skill_tag=course.slug,
                    description=f"Completed all core quizzes and exercises in {course.title}.",
                    share_path=f"/showcase/{user.id}",
                )
            )

    teacher_endorsements = db.query(TeacherFeedback).filter(TeacherFeedback.student_id == user.id, TeacherFeedback.is_endorsement == True).all()  # noqa: E712
    for row in teacher_endorsements:
        achievements.append(
            AchievementOut(
                id=f"endorsement-{row.id}",
                title=f"Teacher Endorsement · {row.title}",
                kind="Teacher Endorsement",
                issuer="EduQuest AI",
                issued_on=row.created_at.date().isoformat(),
                skill_tag=row.target_type,
                description=row.comment,
                share_path=f"/showcase/{user.id}",
            )
        )

    achievements.sort(key=lambda item: (item.kind, item.issued_on, item.title), reverse=True)
    return achievements


def _feedback_out(row: TeacherFeedback) -> TeacherFeedbackOut:
    return TeacherFeedbackOut(
        id=row.id,
        student_id=row.student_id,
        teacher_name=row.teacher.name if row.teacher else "Teacher",
        target_type=row.target_type,
        target_id=row.target_id,
        title=row.title,
        comment=row.comment,
        is_endorsement=row.is_endorsement,
        created_at=row.created_at,
    )


def process_attempt(*, db: Session, user: User, item, user_answer: str, hints_used: int, time_spent_sec: float, confidence: int = 3, helpfulness: int = 3, kind: str = "quest", collaborator_note: str | None = None) -> AttemptResult:
    mastery = get_or_create_mastery(db, user.id, item.skill_tag)
    is_correct, misconception, rule_feedback = evaluate_item(item, user_answer)
    before, after = update_mastery(mastery, is_correct=is_correct, hints_used=hints_used, time_spent_sec=time_spent_sec)
    update_progress(user, is_correct, item.reward_coins)

    if kind == "quest":
        db.add(QuestSubmission(user_id=user.id, quest_id=item.id, user_answer=user_answer, is_correct=is_correct, confidence=confidence, helpfulness=helpfulness, hints_used=hints_used, time_spent_sec=time_spent_sec, misconception=misconception, mastery_before=before, mastery_after=after))
    elif kind == "quiz":
        db.add(QuizAttempt(user_id=user.id, quiz_id=item.id, user_answer=user_answer, is_correct=is_correct, hints_used=hints_used, time_spent_sec=time_spent_sec, misconception=misconception, mastery_before=before, mastery_after=after))
    elif kind == "exercise":
        db.add(ExerciseAttempt(user_id=user.id, exercise_id=item.id, user_answer=user_answer, is_correct=is_correct, hints_used=hints_used, time_spent_sec=time_spent_sec, misconception=misconception, mastery_before=before, mastery_after=after))
    else:
        db.add(TeamChallengeSubmission(user_id=user.id, challenge_id=item.id, team_name=user.team_name, user_answer=user_answer, collaborator_note=collaborator_note, is_correct=is_correct, hints_used=hints_used, time_spent_sec=time_spent_sec, misconception=misconception, mastery_before=before, mastery_after=after))
    db.commit()
    db.refresh(user)
    _, _, learner_state = compute_learner_state(db, user.id)
    llm_feedback = build_llm_feedback(item, user_answer, is_correct, misconception)
    expected_explanation = getattr(item, "explanation", getattr(item, "solution", ""))
    return AttemptResult(
        is_correct=is_correct,
        misconception=misconception,
        rule_feedback=rule_feedback,
        llm_feedback=llm_feedback,
        expected_explanation=expected_explanation,
        mastery_before=round(before, 2),
        mastery_after=round(after, 2),
        learner_state=learner_state,
        coins=user.coins,
        level=user.level,
        streak=user.streak,
    )


def build_review_queue(db: Session) -> list[ReviewQueueItemOut]:
    queue: list[ReviewQueueItemOut] = []

    incorrect_quests = db.query(QuestSubmission).options(joinedload(QuestSubmission.user), joinedload(QuestSubmission.quest)).filter(QuestSubmission.is_correct == False).all()  # noqa: E712
    for row in incorrect_quests:
        queue.append(ReviewQueueItemOut(
            target_type="quest",
            target_id=row.id,
            student_id=row.user_id,
            student_name=row.user.name,
            team_name=row.user.team_name,
            title=row.quest.title,
            submitted_answer=row.user_answer,
            status="Needs teacher feedback",
            created_at=row.created_at,
            existing_feedback=db.query(TeacherFeedback).filter(TeacherFeedback.target_type == "quest", TeacherFeedback.target_id == row.id).count(),
        ))

    incorrect_quizzes = db.query(QuizAttempt).options(joinedload(QuizAttempt.user), joinedload(QuizAttempt.quiz)).filter(QuizAttempt.is_correct == False).all()  # noqa: E712
    for row in incorrect_quizzes:
        queue.append(ReviewQueueItemOut(
            target_type="quiz",
            target_id=row.id,
            student_id=row.user_id,
            student_name=row.user.name,
            team_name=row.user.team_name,
            title=row.quiz.title,
            submitted_answer=row.user_answer,
            status="Needs teacher feedback",
            created_at=row.created_at,
            existing_feedback=db.query(TeacherFeedback).filter(TeacherFeedback.target_type == "quiz", TeacherFeedback.target_id == row.id).count(),
        ))

    team_rows = db.query(TeamChallengeSubmission).options(joinedload(TeamChallengeSubmission.user), joinedload(TeamChallengeSubmission.challenge)).all()
    for row in team_rows:
        queue.append(ReviewQueueItemOut(
            target_type="team",
            target_id=row.id,
            student_id=row.user_id,
            student_name=row.user.name,
            team_name=row.team_name,
            title=row.challenge.title,
            submitted_answer=row.user_answer,
            status="Collaborative submission",
            created_at=row.created_at,
            existing_feedback=db.query(TeacherFeedback).filter(TeacherFeedback.target_type == "team", TeacherFeedback.target_id == row.id).count(),
        ))

    queue.sort(key=lambda item: item.created_at, reverse=True)
    return queue[:20]


# ---------- startup ----------
@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    try:
        seed_if_needed(db)
        rag_service.load(db.query(CourseDocument).all())
    finally:
        db.close()


# ---------- auth ----------
@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = secrets.token_urlsafe(24)
    SESSIONS[token] = user.id
    return LoginResponse(token=token, user=user)


@app.get("/api/auth/me", response_model=UserOut)
def auth_me(current_user: User = Depends(get_current_user)):
    return current_user


# ---------- content ----------
@app.get("/api/courses", response_model=list[CourseOut])
def list_courses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    courses = db.query(Course).order_by(Course.title.asc()).all()
    return [course_out(course, is_bonus_unlocked(db, current_user.id, course)) for course in courses]


@app.post("/api/courses/{course_slug}/unlock-bonus", response_model=UserOut)
def unlock_course_bonus(course_slug: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.slug == course_slug).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if not course.bonus_reward_code or not course.bonus_reward_cost:
        raise HTTPException(status_code=400, detail="This course does not have an unlockable bonus module")
    if is_bonus_unlocked(db, current_user.id, course):
        raise HTTPException(status_code=400, detail="Bonus module already unlocked")
    if current_user.coins < course.bonus_reward_cost:
        raise HTTPException(status_code=400, detail=f"Not enough coins. You need {course.bonus_reward_cost} coins.")
    current_user.coins -= course.bonus_reward_cost
    db.add(RewardRedemption(user_id=current_user.id, reward_code=course.bonus_reward_code, title=course.bonus_module_title or "Bonus module", cost=course.bonus_reward_cost))
    db.commit()
    db.refresh(current_user)
    return current_user


@app.get("/api/quests", response_model=list[QuestOut])
def list_quests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Quest).order_by(Quest.track.asc(), Quest.difficulty.asc()).all()


@app.post("/api/quests/{quest_id}/submit", response_model=AttemptResult)
def submit_quest(quest_id: int, payload: AttemptCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    quest = db.query(Quest).filter(Quest.id == quest_id).first()
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")
    return process_attempt(db=db, user=current_user, item=quest, user_answer=payload.user_answer, hints_used=payload.hints_used, time_spent_sec=payload.time_spent_sec, confidence=payload.confidence, helpfulness=payload.helpfulness, kind="quest")


@app.get("/api/quizzes", response_model=list[QuizOut])
def list_quizzes(course_id: int | None = None, topic: str | None = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(QuizQuestion).order_by(QuizQuestion.course_id.asc(), QuizQuestion.topic.asc(), QuizQuestion.difficulty.asc())
    if course_id:
        query = query.filter(QuizQuestion.course_id == course_id)
    if topic:
        query = query.filter(QuizQuestion.topic == topic)
    return query.all()


@app.post("/api/quizzes/{quiz_id}/submit", response_model=AttemptResult)
def submit_quiz(quiz_id: int, payload: AttemptCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    quiz = db.query(QuizQuestion).filter(QuizQuestion.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return process_attempt(db=db, user=current_user, item=quiz, user_answer=payload.user_answer, hints_used=payload.hints_used, time_spent_sec=payload.time_spent_sec, confidence=payload.confidence, helpfulness=payload.helpfulness, kind="quiz")


@app.get("/api/exercises", response_model=list[ExerciseOut])
def list_exercises(course_id: int | None = None, topic: str | None = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(Exercise).order_by(Exercise.course_id.asc(), Exercise.topic.asc(), Exercise.difficulty.asc())
    if course_id:
        query = query.filter(Exercise.course_id == course_id)
    if topic:
        query = query.filter(Exercise.topic == topic)
    return query.all()


@app.post("/api/exercises/{exercise_id}/submit", response_model=AttemptResult)
def submit_exercise(exercise_id: int, payload: AttemptCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return process_attempt(db=db, user=current_user, item=exercise, user_answer=payload.user_answer, hints_used=payload.hints_used, time_spent_sec=payload.time_spent_sec, confidence=payload.confidence, helpfulness=payload.helpfulness, kind="exercise")


@app.get("/api/team-challenges", response_model=list[TeamChallengeOut])
def list_team_challenges(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(TeamChallenge).order_by(TeamChallenge.theme.asc(), TeamChallenge.difficulty.asc()).all()


@app.post("/api/team-challenges/{challenge_id}/submit", response_model=AttemptResult)
def submit_team_challenge(challenge_id: int, payload: TeamAttemptCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    challenge = db.query(TeamChallenge).filter(TeamChallenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return process_attempt(db=db, user=current_user, item=challenge, user_answer=payload.user_answer, hints_used=payload.hints_used, time_spent_sec=payload.time_spent_sec, kind="team", collaborator_note=payload.collaborator_note)


@app.get("/api/team-leaderboard", response_model=list[TeamLeaderboardEntry])
def team_leaderboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    team_members: dict[str, set[int]] = defaultdict(set)
    points: dict[str, int] = defaultdict(int)
    completions: dict[str, int] = defaultdict(int)
    for user in db.query(User).filter(User.role == "student").all():
        team = user.team_name or "Independent"
        team_members[team].add(user.id)
        points[team] += user.coins
    for row in db.query(TeamChallengeSubmission).filter(TeamChallengeSubmission.is_correct == True).all():  # noqa: E712
        team = row.team_name or "Independent"
        completions[team] += 1
    rows = [
        TeamLeaderboardEntry(team_name=team, members=len(members), collaboration_points=points[team], completed_challenges=completions[team])
        for team, members in team_members.items()
    ]
    rows.sort(key=lambda item: (item.completed_challenges, item.collaboration_points), reverse=True)
    return rows


# ---------- dashboards ----------
@app.get("/api/dashboard/me", response_model=DashboardOut)
def student_dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    all_activity = all_attempts_for_user(db, current_user.id)
    accuracy, _, learner_state = compute_learner_state(db, current_user.id)
    mastery_rows = current_user.mastery_entries

    weak_skills = sorted(mastery_rows, key=lambda row: row.mastery)
    preferred_skills = {row.skill_tag for row in weak_skills[:2]}
    completed_quest_ids = {row.quest_id for row in db.query(QuestSubmission).filter(QuestSubmission.user_id == current_user.id, QuestSubmission.is_correct == True).all()}  # noqa: E712
    quest_query = db.query(Quest)
    if completed_quest_ids:
        quest_query = quest_query.filter(~Quest.id.in_(completed_quest_ids))
    recommended_quests = quest_query.filter(Quest.skill_tag.in_(preferred_skills)).limit(3).all() if preferred_skills else quest_query.limit(3).all()
    if len(recommended_quests) < 3:
        existing = {q.id for q in recommended_quests}
        extras = db.query(Quest).filter(~Quest.id.in_(existing)).limit(3 - len(recommended_quests)).all()
        recommended_quests.extend(extras)

    courses = db.query(Course).all()
    interest_tokens = {token.strip().lower() for token in current_user.interests.split(",") if token.strip()}
    recommended_courses = [course for course in courses if any(token in course.title.lower() or token in course.description.lower() for token in interest_tokens)]
    if not recommended_courses:
        recommended_courses = courses[:3]

    return DashboardOut(
        user=current_user,
        learner_state=learner_state,
        total_attempts=len(all_activity),
        total_correct=sum(1 for row in all_activity if row["is_correct"]),
        accuracy=round(accuracy, 2),
        mastery=[MasteryItem(skill_tag=row.skill_tag, mastery=round(row.mastery, 2), attempts=row.attempts) for row in mastery_rows],
        recent_activity=[SubmissionOut(id=index + 1, item_type=row["item_type"], item_title=row["item_title"], is_correct=row["is_correct"], created_at=row["created_at"]) for index, row in enumerate(all_activity[:8])],
        recommended_quests=recommended_quests,
        recommended_courses=[course_out(course, is_bonus_unlocked(db, current_user.id, course)) for course in recommended_courses[:3]],
    )


@app.get("/api/portfolio/me", response_model=list[PortfolioOut])
def list_portfolio(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(PortfolioEntry).filter(PortfolioEntry.user_id == current_user.id).order_by(PortfolioEntry.created_at.desc()).all()


@app.post("/api/portfolio", response_model=PortfolioOut)
def create_portfolio_entry(payload: PortfolioCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    entry = PortfolioEntry(user_id=current_user.id, **payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@app.get("/api/portfolio/showcase", response_model=ShowcaseOut)
def get_showcase(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    achievements = build_achievements(db, current_user)
    return ShowcaseOut(
        user_id=current_user.id,
        owner_name=current_user.name,
        headline="Shareable badges, endorsements, and course certificates earned through guided practice.",
        achievements=achievements,
    )


@app.get("/api/showcase/{user_id}", response_model=ShowcaseOut)
def public_showcase(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id, User.role == "student").first()
    if not user:
        raise HTTPException(status_code=404, detail="Showcase not found")
    achievements = build_achievements(db, user)
    return ShowcaseOut(
        user_id=user.id,
        owner_name=user.name,
        headline="Shareable badges, endorsements, and course certificates earned through guided practice.",
        achievements=achievements,
    )


@app.get("/api/leaderboard", response_model=list[LeaderboardEntry])
def leaderboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    students = db.query(User).filter(User.role == "student").all()
    rows = []
    for student in students:
        completed = (
            db.query(QuestSubmission).filter(QuestSubmission.user_id == student.id, QuestSubmission.is_correct == True).count()  # noqa: E712
            + db.query(QuizAttempt).filter(QuizAttempt.user_id == student.id, QuizAttempt.is_correct == True).count()  # noqa: E712
            + db.query(ExerciseAttempt).filter(ExerciseAttempt.user_id == student.id, ExerciseAttempt.is_correct == True).count()  # noqa: E712
            + db.query(TeamChallengeSubmission).filter(TeamChallengeSubmission.user_id == student.id, TeamChallengeSubmission.is_correct == True).count()  # noqa: E712
        )
        rows.append(LeaderboardEntry(name=student.name, coins=student.coins, level=student.level, streak=student.streak, completed=completed))
    rows.sort(key=lambda row: (row.coins, row.completed, row.streak), reverse=True)
    return rows


# ---------- teacher review & analytics ----------
@app.get("/api/teacher/overview", response_model=TeacherOverview)
def teacher_overview(current_user: User = Depends(require_teacher), db: Session = Depends(get_db)):
    students = db.query(User).filter(User.role == "student").all()
    submissions = db.query(QuestSubmission).all() + db.query(QuizAttempt).all() + db.query(ExerciseAttempt).all() + db.query(TeamChallengeSubmission).all()
    accuracy = sum(1 for row in submissions if row.is_correct) / max(1, len(submissions))
    misconception_counter = Counter(row.misconception for row in submissions if row.misconception)

    course_engagement = []
    for course in db.query(Course).all():
        quiz_attempts = db.query(QuizAttempt).join(QuizQuestion).filter(QuizQuestion.course_id == course.id).count()
        exercise_attempts = db.query(ExerciseAttempt).join(Exercise).filter(Exercise.course_id == course.id).count()
        course_engagement.append({"course": course.title, "interactions": quiz_attempts + exercise_attempts})

    skill_mastery = []
    for student in students:
        for row in student.mastery_entries:
            skill_mastery.append({"learner": student.name, "skill_tag": row.skill_tag, "mastery": round(row.mastery, 2), "attempts": row.attempts})

    team_activity = [item.model_dump() for item in team_leaderboard(current_user=current_user, db=db)]

    return TeacherOverview(
        total_students=len(students),
        total_submissions=len(submissions),
        average_accuracy=round(accuracy, 2),
        common_misconceptions=[{"label": label, "count": count} for label, count in misconception_counter.most_common(6)],
        leaderboard=[item.model_dump() for item in leaderboard(current_user=current_user, db=db)],
        course_engagement=course_engagement,
        skill_mastery=skill_mastery,
        team_activity=team_activity,
    )


@app.get("/api/teacher/review-queue", response_model=list[ReviewQueueItemOut])
def teacher_review_queue(current_user: User = Depends(require_teacher), db: Session = Depends(get_db)):
    return build_review_queue(db)


@app.post("/api/teacher/feedback", response_model=TeacherFeedbackOut)
def create_teacher_feedback(payload: TeacherFeedbackCreate, current_user: User = Depends(require_teacher), db: Session = Depends(get_db)):
    student = db.query(User).filter(User.id == payload.student_id, User.role == "student").first()
    if not student:
        raise HTTPException(status_code=404, detail="Learner not found")
    row = TeacherFeedback(
        teacher_id=current_user.id,
        student_id=payload.student_id,
        target_type=payload.target_type,
        target_id=payload.target_id,
        title=payload.title,
        comment=payload.comment,
        is_endorsement=payload.is_endorsement,
    )
    if payload.is_endorsement:
        student.coins += 10
    db.add(row)
    db.commit()
    db.refresh(row)
    return _feedback_out(row)


@app.get("/api/teacher-feedback/me", response_model=list[TeacherFeedbackOut])
def list_my_feedback(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = (
        db.query(TeacherFeedback)
        .options(joinedload(TeacherFeedback.teacher))
        .filter(TeacherFeedback.student_id == current_user.id)
        .order_by(TeacherFeedback.created_at.desc())
        .all()
    )
    return [_feedback_out(row) for row in rows]


# ---------- tutor ----------
@app.post("/api/tutor/query", response_model=TutorResponse)
def tutor_query(payload: TutorQuery, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    answer, citations, mode = rag_service.answer(payload.question, payload.course_slug)
    return TutorResponse(answer=answer, citations=citations, mode=mode)
