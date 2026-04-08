from app.models import SkillMastery


def get_or_create_mastery(db, user_id: int, skill_tag: str) -> SkillMastery:
    mastery = (
        db.query(SkillMastery)
        .filter(SkillMastery.user_id == user_id, SkillMastery.skill_tag == skill_tag)
        .first()
    )
    if mastery:
        return mastery
    mastery = SkillMastery(user_id=user_id, skill_tag=skill_tag, mastery=0.5, attempts=0)
    db.add(mastery)
    db.flush()
    return mastery


def update_mastery(mastery: SkillMastery, is_correct: bool, hints_used: int, time_spent_sec: float) -> tuple[float, float]:
    before = mastery.mastery
    delta = 0.12 if is_correct else -0.13
    delta -= 0.03 * min(hints_used, 2)
    if time_spent_sec > 120:
        delta -= 0.03
    elif is_correct and time_spent_sec < 35:
        delta += 0.02
    mastery.mastery = min(0.95, max(0.05, mastery.mastery + delta))
    mastery.attempts += 1
    return before, mastery.mastery


def classify_learner_state(accuracy: float, avg_hints: float) -> str:
    if accuracy >= 0.8 and avg_hints <= 0.5:
        return "Advanced"
    if accuracy <= 0.45 or avg_hints >= 1.5:
        return "Needs support"
    return "Stable"
