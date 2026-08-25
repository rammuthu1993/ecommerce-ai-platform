import math
import re
from collections import Counter
from app.rag.document_processor import build_knowledge_chunks

class VectorStore:

    def __init__(self):
        self.chunks = []
        self.vocabulary = {}
        self.idf = {}
        self.doc_vectors = []
        self.is_indexed = False

    def _tokenize(self, text: str) -> list:
        return re.findall(r"\w+", text.lower())

    def index_documents(self, chunks: list = None):
        self.chunks = chunks if chunks is not None else build_knowledge_chunks()
        if not self.chunks:
            return

        # Build vocabulary & Term Frequency (TF)
        doc_count = len(self.chunks)
        doc_freqs = Counter()

        tokenized_docs = []
        for chunk in self.chunks:
            tokens = self._tokenize(chunk["content"] + " " + chunk["title"])
            tokenized_docs.append(tokens)
            unique_tokens = set(tokens)
            for token in unique_tokens:
                doc_freqs[token] += 1

        # Calculate Inverse Document Frequency (IDF)
        self.idf = {
            term: math.log((doc_count + 1) / (df + 1)) + 1
            for term, df in doc_freqs.items()
        }

        # Build TF-IDF Vectors
        self.doc_vectors = []
        for tokens in tokenized_docs:
            vector = self._compute_tfidf_vector(tokens)
            self.doc_vectors.append(vector)

        self.is_indexed = True

    def _compute_tfidf_vector(self, tokens: list) -> dict:
        total_tokens = len(tokens)
        if total_tokens == 0:
            return {}

        tf_counter = Counter(tokens)
        vector = {}
        for token, count in tf_counter.items():
            tf = count / total_tokens
            vector[token] = tf * self.idf.get(token, 0.0)
        return vector

    def _cosine_similarity(self, vec1: dict, vec2: dict) -> float:
        intersection = set(vec1.keys()).intersection(set(vec2.keys()))
        if not intersection:
            return 0.0

        dot_product = sum(vec1[token] * vec2[token] for token in intersection)
        mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))

        if mag1 == 0.0 or mag2 == 0.0:
            return 0.0

        return dot_product / (mag1 * mag2)

    def search(self, query: str, top_k: int = 3) -> list:
        if not self.is_indexed:
            self.index_documents()

        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        query_vector = self._compute_tfidf_vector(query_tokens)

        results = []
        for i, doc_vector in enumerate(self.doc_vectors):
            sim = self._cosine_similarity(query_vector, doc_vector)
            if sim > 0.01:
                chunk = self.chunks[i].copy()
                chunk["score"] = round(sim, 4)
                results.append(chunk)

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

vector_store = VectorStore()
