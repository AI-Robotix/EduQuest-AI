from __future__ import annotations

import math
import os
from typing import Tuple

try:
    import ollama
except Exception:  # pragma: no cover
    ollama = None

LLM_MODEL = os.getenv("OLLAMA_LLM_MODEL", "qwen2.5:7b")
USE_LLM_EXPLANATIONS = os.getenv("USE_LLM_EXPLANATIONS", "0") == "1"


def _normalize(text: str) -> str:
    return text.strip().lower()


def evaluate_item(item, user_answer: str) -> Tuple[bool, str | None, str]:
    answer = _normalize(user_answer)
    accepted = [_normalize(part) for part in item.accepted_answers.split("|")]

    if item.question_type == "mcq":
        is_correct = answer in accepted
    elif item.question_type == "numeric":
        try:
            is_correct = math.isclose(float(answer), float(accepted[0]), rel_tol=1e-4, abs_tol=1e-4)
        except ValueError:
            is_correct = False
    elif item.question_type == "contains_any":
        is_correct = any(keyword in answer for keyword in accepted)
    else:
        is_correct = answer in accepted

    misconception = detect_misconception(item.skill_tag, answer, is_correct)
    return is_correct, misconception, build_rule_feedback(is_correct, misconception)


def detect_misconception(skill_tag: str, answer: str, is_correct: bool) -> str | None:
    if is_correct:
        return None

    if skill_tag in {"metrics_precision", "metrics_recall", "metrics_accuracy"}:
        try:
            value = float(answer)
        except ValueError:
            return "Enter the metric as a decimal value between 0 and 1."
        if value > 1:
            return "Use a decimal between 0 and 1, not a percentage."
        return "Recheck the metric formula and especially the denominator."

    if skill_tag == "python_loops" and "if" in answer and "for" not in answer:
        return "You selected a condition instead of the iteration keyword."
    if skill_tag == "python_lists" and "tuple" in answer:
        return "A tuple is fixed after creation, but a list can change."
    if skill_tag == "gradient_descent" and "increase" in answer:
        return "Gradient descent moves parameters to reduce the loss."
    if skill_tag == "nn_layers" and "more layers always" in answer:
        return "More layers do not guarantee better results without suitable training and regularization."
    if skill_tag == "prompting" and "creative" in answer:
        return "The stronger prompt is the one with task, context, and output constraints."
    if skill_tag == "rag_grounding" and "faster" in answer:
        return "Grounding is mainly about evidence and reliability, not just speed."
    if skill_tag == "privacy" and "share everything" in answer:
        return "Privacy by design starts with data minimization and removing unnecessary identifiers."

    return "Review the key concept and try again with a more precise answer."


def build_rule_feedback(is_correct: bool, misconception: str | None) -> str:
    if is_correct:
        return "Correct. You can move to a slightly more challenging task."
    if misconception:
        return f"Not quite yet. {misconception}"
    return "Not quite yet. Review the concept and try again."


def _deterministic_explanation(item, is_correct: bool, misconception: str | None) -> str:
    reference = getattr(item, "explanation", getattr(item, "solution", "")).strip()
    if is_correct:
        return reference
    if misconception:
        return f"Why this answer matters: {reference}"
    return reference or "Review the provided concept explanation and try again."


def build_llm_feedback(item, user_answer: str, is_correct: bool, misconception: str | None) -> str:
    reference = getattr(item, "explanation", getattr(item, "solution", "")).strip()
    if not reference:
        reference = "Review the model answer and the underlying concept."

    if not USE_LLM_EXPLANATIONS or ollama is None:
        return _deterministic_explanation(item, is_correct, misconception)

    try:
        response = ollama.chat(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a concise teaching assistant. Return exactly one short explanation sentence. "
                        "Do not mention regulations, next steps, or extra advice. "
                        "Explain only why the correct answer is correct or why the chosen answer is incorrect."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Prompt: {item.prompt}\n"
                        f"Learner answer: {user_answer}\n"
                        f"Correct: {is_correct}\n"
                        f"Misconception: {misconception or 'None'}\n"
                        f"Reference explanation: {reference}"
                    ),
                },
            ],
        )
        message = response["message"]["content"].strip()
        return message if message else reference
    except Exception:
        return _deterministic_explanation(item, is_correct, misconception)
