import json
from pathlib import Path
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class DocumentChunk:
    document_id: str
    title: str
    section: str
    jurisdiction: str
    classification: str
    text: str


class LocalPolicyRetriever:
    def __init__(self, corpus_path: str = "data/policies/policies.json"):
        raw = json.loads(Path(corpus_path).read_text())
        self.docs = [DocumentChunk(**d) for d in raw]
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform([d.text for d in self.docs])

    def search(self, query: str, jurisdiction: str = "US", k: int = 3) -> list[DocumentChunk]:
        candidates = [(i, d) for i, d in enumerate(self.docs) if d.jurisdiction in {jurisdiction, "GLOBAL"}]
        if not candidates:
            return []
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix).flatten()
        ranked = sorted(candidates, key=lambda x: scores[x[0]], reverse=True)
        return [d for i, d in ranked[:k] if scores[i] > 0]
