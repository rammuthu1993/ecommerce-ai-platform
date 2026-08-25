import unittest

from app.rag.document_processor import build_knowledge_chunks
from app.rag.vector_store import VectorStore
from app.rag.rag_service import answer_rag_query


class TestRAGEngine(unittest.TestCase):

    def test_document_chunking(self):
        chunks = build_knowledge_chunks()
        self.assertGreater(len(chunks), 0)
        self.assertIn("chunk_id", chunks[0])
        self.assertIn("content", chunks[0])

    def test_vector_store_indexing_and_search(self):
        vs = VectorStore()
        vs.index_documents()

        results = vs.search("What is the return policy?", top_k=2)
        self.assertGreaterEqual(len(results), 1)
        self.assertIn("Return & Refund Policy", [r["title"] for r in results])
        self.assertGreater(results[0]["score"], 0.0)

    def test_rag_query_answering_with_citations(self):
        res = answer_rag_query("What is the shipping cost for orders below 50 dollars?")
        self.assertIsNotNone(res["answer"])
        self.assertIn("Shipping Policy", res["sources"])
        self.assertGreater(len(res["retrieved_chunks"]), 0)
