from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, List, Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    import ollama
except Exception:  # pragma: no cover
    ollama = None


@dataclass
class RetrievalHit:
    title: str
    source: str
    content: str
    score: float
    course_slug: Optional[str] = None


class RagService:
    def __init__(self) -> None:
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.doc_texts: List[str] = []
        self.doc_meta: List[dict] = []
        self.doc_vectors = None
        self.llm_model = os.getenv("OLLAMA_LLM_MODEL", "qwen2.5:7b")

    def _normalize_doc(self, doc: Any) -> dict:
        if isinstance(doc, dict):
            return {
                "title": doc.get("title", "Untitled"),
                "source": doc.get("source", "Unknown"),
                "content": doc.get("content", ""),
                "course_slug": doc.get("course_slug"),
            }
        return {
            "title": getattr(doc, "title", "Untitled"),
            "source": getattr(doc, "source", "Unknown"),
            "content": getattr(doc, "content", ""),
            "course_slug": getattr(doc, "course_slug", None),
        }

    def index_documents(self, docs: List[Any]) -> None:
        normalized = []
        for doc in docs:
            item = self._normalize_doc(doc)
            if item["content"].strip():
                normalized.append(item)
        self.doc_meta = normalized
        self.doc_texts = [doc["content"] for doc in normalized]
        self.doc_vectors = self.vectorizer.fit_transform(self.doc_texts) if self.doc_texts else None

    def load(self, docs: List[Any]) -> None:
        self.index_documents(docs)

    def retrieve(self, question: str, top_k: int = 3, course_slug: str | None = None) -> List[RetrievalHit]:
        if not self.doc_texts or self.doc_vectors is None:
            return []

        candidate_indices = list(range(len(self.doc_meta)))
        if course_slug:
            candidate_indices = [idx for idx, meta in enumerate(self.doc_meta) if meta.get("course_slug") == course_slug]
        if not candidate_indices:
            return []

        candidate_texts = [self.doc_texts[idx] for idx in candidate_indices]
        candidate_vectors = self.vectorizer.transform(candidate_texts)
        q_vec = self.vectorizer.transform([question])
        sims = cosine_similarity(q_vec, candidate_vectors)[0]
        ranked_local = sims.argsort()[::-1][:top_k]
        hits: List[RetrievalHit] = []
        for local_idx in ranked_local:
            global_idx = candidate_indices[local_idx]
            meta = self.doc_meta[global_idx]
            hits.append(
                RetrievalHit(
                    title=meta["title"],
                    source=meta["source"],
                    content=meta["content"],
                    score=float(sims[local_idx]),
                    course_slug=meta.get("course_slug"),
                )
            )
        return hits

    def answer(self, question: str, course_slug: str | None = None) -> tuple[str, list[dict], str]:
        hits = self.retrieve(question, top_k=3, course_slug=course_slug)
        citations = [
            {"title": hit.title, "source": hit.source, "score": round(hit.score, 3), "course_slug": hit.course_slug}
            for hit in hits
        ]
        if not hits:
            return "No indexed course material is available yet for this topic.", [], "fallback"

        context = "\n\n".join(f"[{i + 1}] {hit.title} ({hit.source})\n{hit.content}" for i, hit in enumerate(hits))
        if ollama is not None:
            try:
                response = ollama.chat(
                    model=self.llm_model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Answer only from the provided course context. "
                                "If the context is insufficient, say so clearly. Cite sources like [1] or [2]."
                            ),
                        },
                        {"role": "user", "content": f"Question: {question}\n\nContext:\n{context}"},
                    ],
                )
                return response["message"]["content"], citations, "ollama_rag"
            except Exception:
                pass
        return f"Based on the indexed notes: {hits[0].content}", citations, "tfidf_fallback"
