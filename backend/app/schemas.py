from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    interests: str
    team_name: Optional[str] = None
    coins: int
    level: int
    streak: int

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str
    user: UserOut


class CourseOut(BaseModel):
    id: int
    title: str
    slug: str
    category: str
    level: str
    duration: str
    description: str
    learning_outcomes: str
    lessons_json: Optional[str] = None
    bonus_reward_code: Optional[str] = None
    bonus_reward_cost: Optional[int] = None
    bonus_module_title: Optional[str] = None
    bonus_module_content: Optional[str] = None
    bonus_unlocked: bool = False

    model_config = {"from_attributes": True}


class QuestOut(BaseModel):
    id: int
    title: str
    track: str
    skill_tag: str
    difficulty: int
    description: str
    prompt: str
    question_type: str
    hint: str
    explanation: str
    badge_name: str
    reward_coins: int

    model_config = {"from_attributes": True}


class QuizOut(BaseModel):
    id: int
    course_id: int
    title: str
    topic: str
    skill_tag: str
    difficulty: int
    prompt: str
    question_type: str
    options_json: Optional[str] = None
    hint: str
    explanation: str
    reward_coins: int

    model_config = {"from_attributes": True}


class ExerciseOut(BaseModel):
    id: int
    course_id: int
    title: str
    topic: str
    skill_tag: str
    difficulty: int
    prompt: str
    question_type: str
    hint: str
    solution: str
    reward_coins: int

    model_config = {"from_attributes": True}


class TeamChallengeOut(BaseModel):
    id: int
    title: str
    theme: str
    skill_tag: str
    difficulty: int
    description: str
    prompt: str
    hint: str
    explanation: str
    badge_name: str
    reward_coins: int

    model_config = {"from_attributes": True}


class AttemptCreate(BaseModel):
    user_answer: str
    confidence: int = Field(default=3, ge=1, le=5)
    helpfulness: int = Field(default=3, ge=1, le=5)
    hints_used: int = Field(default=0, ge=0, le=5)
    time_spent_sec: float = Field(default=0, ge=0)


class TeamAttemptCreate(BaseModel):
    user_answer: str
    collaborator_note: Optional[str] = None
    hints_used: int = Field(default=0, ge=0, le=5)
    time_spent_sec: float = Field(default=0, ge=0)


class AttemptResult(BaseModel):
    is_correct: bool
    misconception: Optional[str] = None
    rule_feedback: str
    llm_feedback: str
    expected_explanation: str
    mastery_before: float
    mastery_after: float
    learner_state: str
    coins: int
    level: int
    streak: int


class SubmissionOut(BaseModel):
    id: int
    item_type: str
    item_title: str
    is_correct: bool
    created_at: datetime


class PortfolioCreate(BaseModel):
    title: str
    reflection: str
    artifact_url: Optional[str] = None
    skill_tag: str


class PortfolioOut(BaseModel):
    id: int
    title: str
    reflection: str
    artifact_url: Optional[str] = None
    skill_tag: str
    created_at: datetime

    model_config = {"from_attributes": True}


class MasteryItem(BaseModel):
    skill_tag: str
    mastery: float
    attempts: int


class DashboardOut(BaseModel):
    user: UserOut
    learner_state: str
    total_attempts: int
    total_correct: int
    accuracy: float
    mastery: list[MasteryItem]
    recent_activity: list[SubmissionOut]
    recommended_quests: list[QuestOut]
    recommended_courses: list[CourseOut]


class TeacherOverview(BaseModel):
    total_students: int
    total_submissions: int
    average_accuracy: float
    common_misconceptions: list[dict]
    leaderboard: list[dict]
    course_engagement: list[dict]
    skill_mastery: list[dict]
    team_activity: list[dict] = []


class TutorQuery(BaseModel):
    question: str
    course_slug: Optional[str] = None


class TutorResponse(BaseModel):
    answer: str
    citations: list[dict]
    mode: str


class LeaderboardEntry(BaseModel):
    name: str
    coins: int
    level: int
    streak: int
    completed: int


class TeamLeaderboardEntry(BaseModel):
    team_name: str
    members: int
    collaboration_points: int
    completed_challenges: int


class AchievementOut(BaseModel):
    id: str
    title: str
    kind: str
    issuer: str
    issued_on: str
    skill_tag: str
    description: str
    share_path: str


class ShowcaseOut(BaseModel):
    user_id: int
    owner_name: str
    headline: str
    achievements: list[AchievementOut]


class TeacherFeedbackCreate(BaseModel):
    student_id: int
    target_type: str
    target_id: int
    title: str
    comment: str
    is_endorsement: bool = False


class TeacherFeedbackOut(BaseModel):
    id: int
    student_id: int
    teacher_name: str
    target_type: str
    target_id: int
    title: str
    comment: str
    is_endorsement: bool
    created_at: datetime


class ReviewQueueItemOut(BaseModel):
    target_type: str
    target_id: int
    student_id: int
    student_name: str
    team_name: Optional[str] = None
    title: str
    submitted_answer: str
    status: str
    created_at: datetime
    existing_feedback: int = 0
