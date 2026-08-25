import unittest

from app.web.request import Request
from app.web.health import health_check_handler
from app.docs.api_docs import api_docs_handler


class TestHealthAndDocs(unittest.TestCase):

    def test_health_check_endpoint(self):
        req = Request(method="GET", path="/health")
        resp = health_check_handler(req)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.body["data"]["status"], "UP")
        self.assertEqual(resp.body["data"]["database"], "healthy")

    def test_api_docs_endpoint(self):
        req = Request(method="GET", path="/api/docs")
        resp = api_docs_handler(req)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.body["data"]["openapi"], "3.0.0")
        self.assertIn("Authentication", resp.body["data"]["endpoints"])
        self.assertIn("Products & Categories", resp.body["data"]["endpoints"])
