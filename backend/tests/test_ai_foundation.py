import unittest

from app.ai.provider import MockLLMProvider
from app.ai.token_tracker import token_tracker
from app.ai.structured_parser import parse_structured_json


class TestAIFoundation(unittest.TestCase):

    def setUp(self):
        token_tracker.reset()

    def test_mock_llm_provider(self):
        provider = MockLLMProvider()
        response = provider.generate("Tell me about ecommerce laptops")

        self.assertIsNotNone(response)
        self.assertIn("AI Assistant Response", response)

        summary = token_tracker.get_summary()
        self.assertEqual(summary["total_calls"], 1)
        self.assertGreater(summary["total_tokens"], 0)

    def test_structured_json_parser(self):
        valid_json_text = '```json\n{"status": "success", "items": [1, 2, 3]}\n```'
        parsed = parse_structured_json(valid_json_text)
        self.assertEqual(parsed["status"], "success")
        self.assertEqual(len(parsed["items"]), 3)

    def test_structured_json_parser_fallback(self):
        raw_text = 'Here is the response: {"result": "ok"} Thank you!'
        parsed = parse_structured_json(raw_text)
        self.assertEqual(parsed["result"], "ok")
