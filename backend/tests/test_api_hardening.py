import unittest
from unittest.mock import MagicMock

from app.web.request import Request
from app.web.response import Response
from app.middleware.security import security_headers_middleware, content_type_middleware
from app.middleware.rate_limit import rate_limiter, rate_limit_middleware
from app.core.exceptions import AppException, RateLimitExceededException


class TestAPIHardening(unittest.TestCase):

    def test_security_headers_middleware(self):
        req = Request(method="GET", path="/")
        next_handler = MagicMock(return_value=Response(data={"ok": True}))

        resp = security_headers_middleware(req, next_handler)
        self.assertEqual(resp.headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(resp.headers["X-Frame-Options"], "DENY")
        self.assertEqual(resp.headers["X-XSS-Protection"], "1; mode=block")

    def test_content_type_validation(self):
        req_valid = Request(method="POST", path="/api/products", headers={"Content-Type": "application/json"}, body='{"name":"X"}')
        next_handler = MagicMock(return_value=Response(data={"ok": True}))
        resp = content_type_middleware(req_valid, next_handler)
        self.assertIsNotNone(resp)

        req_invalid = Request(method="POST", path="/api/products", headers={"Content-Type": "text/plain"}, body='{"name":"X"}')
        with self.assertRaises(AppException) as ctx:
            content_type_middleware(req_invalid, next_handler)
        self.assertEqual(ctx.exception.status_code, 415)

    def test_rate_limiting(self):
        rate_limiter.reset()
        rate_limiter.limit = 3 # max 3 requests

        req = Request(method="GET", path="/", headers={"X-Forwarded-For": "192.168.1.100"})
        next_handler = MagicMock(return_value=Response(data={"ok": True}))

        # First 3 should succeed
        rate_limit_middleware(req, next_handler)
        rate_limit_middleware(req, next_handler)
        rate_limit_middleware(req, next_handler)

        # 4th request should raise RateLimitExceededException
        with self.assertRaises(RateLimitExceededException):
            rate_limit_middleware(req, next_handler)

        rate_limiter.reset()
