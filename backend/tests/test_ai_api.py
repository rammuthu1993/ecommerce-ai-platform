import os
import unittest

from app.config.settings import settings
from app.database.connection import initialize_database
from app.web.request import Request
from app.web.server import (
    ai_chat_handler,
    ai_rag_handler,
    ai_agent_handler,
    ai_knowledge_handler,
    ai_token_usage_handler
)


class TestAIAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        settings.database = "test_ecommerce.db"
        initialize_database()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("test_ecommerce.db"):
            try:
                os.remove("test_ecommerce.db")
            except OSError:
                pass

    def test_ai_chat_endpoint(self):
        req = Request(method="POST", path="/api/ai/chat", body='{"prompt": "Hello AI"}')
        resp = ai_chat_handler(req)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("reply", resp.body["data"])

    def test_ai_rag_endpoint(self):
        req = Request(method="POST", path="/api/ai/rag/query", body='{"query": "What is the return policy?"}')
        resp = ai_rag_handler(req)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("sources", resp.body["data"])

    def test_ai_agent_endpoint(self):
        req = Request(method="POST", path="/api/ai/agent/query", body='{"query": "Find laptops below 60000"}')
        resp = ai_agent_handler(req)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("final_answer", resp.body["data"])

    def test_ai_knowledge_endpoint(self):
        req = Request(method="GET", path="/api/ai/knowledge")
        resp = ai_knowledge_handler(req)
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.body["data"]), 0)

    def test_ai_token_usage_endpoint(self):
        req = Request(method="GET", path="/api/ai/token-usage")
        resp = ai_token_usage_handler(req)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("total_tokens", resp.body["data"])
