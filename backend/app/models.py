from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="student")
    interests: Mapped[str] = mapped_column(String(255), default="")
    team_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    coins: Mapped[int] = mapped_column(Integer, default=100)
    level: Mapped[int] = mapped_column(Integer, default=1)
    streak: Mapped[int] = mapped_column(Integer, default=0)

    quest_submissions = relationship("QuestSubmission", back_populates="user", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="user", cascade="all, delete-orphan")
    exercise_attempts = relationship("ExerciseAttempt", back_populates="user", cascade="all, delete-orphan")
    portfolio_entries = relationship("PortfolioEntry", back_populates="user", cascade="all, delete-orphan")
    mastery_entries = relationship("SkillMastery", back_populates="user", cascade="all, delete-orphan")
    reward_redemptions = relationship("RewardRedemption", back_populates="user", cascade="all, delete-orphan")
    team_submissions = relationship("TeamChallengeSubmission", back_populates="user", cascade="all, delete-orphan")
    feedback_received = relationship("TeacherFeedback", foreign_keys="TeacherFeedback.student_id", back_populates="student", cascade="all, delete-orphan")
    feedback_given = relationship("TeacherFeedback", foreign_keys="TeacherFeedback.teacher_id", back_populates="teacher", cascade="all, delete-orphan")


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    level: Mapped[str] = mapped_column(String(40), nullable=False)
    duration: Mapped[str] = mapped_column(String(40), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    learning_outcomes: Mapped[str] = mapped_column(Text, nullable=False)
    lessons_json: Mapped[str] = mapped_column(Text, default="[]")
    bonus_reward_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    bonus_reward_cost: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bonus_module_title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    bonus_module_content: Mapped[str | None] = mapped_column(Text, nullable=True)

    quizzes = relationship("QuizQuestion", back_populates="course", cascade="all, delete-orphan")
    exercises = relationship("Exercise", back_populates="course", cascade="all, delete-orphan")


class Quest(Base):
    __tablename__ = "quests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    track: Mapped[str] = mapped_column(String(100), nullable=False)
    skill_tag: Mapped[str] = mapped_column(String(100), nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, default=2)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(String(40), nullable=False)
    accepted_answers: Mapped[str] = mapped_column(Text, nullable=False)
    hint: Mapped[str] = mapped_column(Text, default="Think about the key concept before choosing an answer.")
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    badge_name: Mapped[str] = mapped_column(String(100), nullable=False)
    reward_coins: Mapped[int] = mapped_column(Integer, default=20)

    submissions = relationship("QuestSubmission", back_populates="quest", cascade="all, delete-orphan")


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    topic: Mapped[str] = mapped_column(String(100), nullable=False)
    skill_tag: Mapped[str] = mapped_column(String(100), nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, default=2)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(String(40), nullable=False)
    accepted_answers: Mapped[str] = mapped_column(Text, nullable=False)
    options_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    hint: Mapped[str] = mapped_column(Text, default="Use the concept summary before choosing an option.")
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    reward_coins: Mapped[int] = mapped_column(Integer, default=15)

    course = relationship("Course", back_populates="quizzes")
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    topic: Mapped[str] = mapped_column(String(100), nullable=False)
    skill_tag: Mapped[str] = mapped_column(String(100), nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, default=2)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(String(40), nullable=False)
    accepted_answers: Mapped[str] = mapped_column(Text, nullable=False)
    hint: Mapped[str] = mapped_column(Text, nullable=False)
    solution: Mapped[str] = mapped_column(Text, nullable=False)
    reward_coins: Mapped[int] = mapped_column(Integer, default=25)

    course = relationship("Course", back_populates="exercises")
    attempts = relationship("ExerciseAttempt", back_populates="exercise", cascade="all, delete-orphan")


class TeamChallenge(Base):
    __tablename__ = "team_challenges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    theme: Mapped[str] = mapped_column(String(100), nullable=False)
    skill_tag: Mapped[str] = mapped_column(String(100), nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, default=2)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    accepted_answers: Mapped[str] = mapped_column(Text, nullable=False)
    hint: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    badge_name: Mapped[str] = mapped_column(String(100), nullable=False)
    reward_coins: Mapped[int] = mapped_column(Integer, default=30)

    submissions = relationship("TeamChallengeSubmission", back_populates="challenge", cascade="all, delete-orphan")


class QuestSubmission(Base):
    __tablename__ = "quest_submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    quest_id: Mapped[int] = mapped_column(ForeignKey("quests.id"), nullable=False)
    user_answer: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    confidence: Mapped[int] = mapped_column(Integer, default=3)
    helpfulness: Mapped[int] = mapped_column(Integer, default=3)
    hints_used: Mapped[int] = mapped_column(Integer, default=0)
    time_spent_sec: Mapped[float] = mapped_column(Float, default=0.0)
    misconception: Mapped[str | None] = mapped_column(Text, nullable=True)
    mastery_before: Mapped[float] = mapped_column(Float, default=0.5)
    mastery_after: Mapped[float] = mapped_column(Float, default=0.5)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="quest_submissions")
    quest = relationship("Quest", back_populates="submissions")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz_questions.id"), nullable=False)
    user_answer: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    hints_used: Mapped[int] = mapped_column(Integer, default=0)
    time_spent_sec: Mapped[float] = mapped_column(Float, default=0.0)
    misconception: Mapped[str | None] = mapped_column(Text, nullable=True)
    mastery_before: Mapped[float] = mapped_column(Float, default=0.5)
    mastery_after: Mapped[float] = mapped_column(Float, default=0.5)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("QuizQuestion", back_populates="attempts")


class ExerciseAttempt(Base):
    __tablename__ = "exercise_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"), nullable=False)
    user_answer: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    hints_used: Mapped[int] = mapped_column(Integer, default=0)
    time_spent_sec: Mapped[float] = mapped_column(Float, default=0.0)
    misconception: Mapped[str | None] = mapped_column(Text, nullable=True)
    mastery_before: Mapped[float] = mapped_column(Float, default=0.5)
    mastery_after: Mapped[float] = mapped_column(Float, default=0.5)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="exercise_attempts")
    exercise = relationship("Exercise", back_populates="attempts")


class TeamChallengeSubmission(Base):
    __tablename__ = "team_challenge_submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    challenge_id: Mapped[int] = mapped_column(ForeignKey("team_challenges.id"), nullable=False)
    team_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    user_answer: Mapped[str] = mapped_column(Text, nullable=False)
    collaborator_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    hints_used: Mapped[int] = mapped_column(Integer, default=0)
    time_spent_sec: Mapped[float] = mapped_column(Float, default=0.0)
    misconception: Mapped[str | None] = mapped_column(Text, nullable=True)
    mastery_before: Mapped[float] = mapped_column(Float, default=0.5)
    mastery_after: Mapped[float] = mapped_column(Float, default=0.5)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="team_submissions")
    challenge = relationship("TeamChallenge", back_populates="submissions")


class PortfolioEntry(Base):
    __tablename__ = "portfolio_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    reflection: Mapped[str] = mapped_column(Text, nullable=False)
    artifact_url: Mapped[str | None] = mapped_column(String(300), nullable=True)
    skill_tag: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="portfolio_entries")


class SkillMastery(Base):
    __tablename__ = "skill_mastery"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    skill_tag: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    mastery: Mapped[float] = mapped_column(Float, default=0.5)
    attempts: Mapped[int] = mapped_column(Integer, default=0)

    user = relationship("User", back_populates="mastery_entries")


class CourseDocument(Base):
    __tablename__ = "course_documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    source: Mapped[str] = mapped_column(String(200), nullable=False)
    course_slug: Mapped[str] = mapped_column(String(80), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)


class RewardRedemption(Base):
    __tablename__ = "reward_redemptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    reward_code: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reward_redemptions")


class TeacherFeedback(Base):
    __tablename__ = "teacher_feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    target_type: Mapped[str] = mapped_column(String(40), nullable=False)
    target_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    is_endorsement: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    teacher = relationship("User", foreign_keys=[teacher_id], back_populates="feedback_given")
    student = relationship("User", foreign_keys=[student_id], back_populates="feedback_received")
