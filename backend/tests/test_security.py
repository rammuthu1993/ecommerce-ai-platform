import time
import unittest

from app.auth.password_hasher import hash_password, verify_password
from app.auth.jwt_engine import generate_jwt, verify_jwt
from app.core.exceptions import InvalidTokenException, TokenExpiredException


class TestSecurityModule(unittest.TestCase):

    def test_password_hashing_and_verification(self):
        password = "SecretPassword123!"
        hash_hex, salt_hex = hash_password(password)

        self.assertIsNotNone(hash_hex)
        self.assertIsNotNone(salt_hex)
        self.assertNotEqual(password, hash_hex)

        # Verification
        self.assertTrue(verify_password(password, hash_hex, salt_hex))

        # Incorrect password
        self.assertFalse(verify_password("WrongPass123!", hash_hex, salt_hex))

    def test_jwt_generation_and_verification(self):
        token = generate_jwt(user_id=101, email="test@example.com", roles=["ADMIN"], expires_in=3600)
        self.assertIsNotNone(token)
        self.assertEqual(len(token.split(".")), 3)

        payload = verify_jwt(token)
        self.assertEqual(payload["sub"], 101)
        self.assertEqual(payload["email"], "test@example.com")
        self.assertIn("ADMIN", payload["roles"])

    def test_jwt_signature_tampering(self):
        token = generate_jwt(user_id=101, email="test@example.com", roles=["CUSTOMER"])
        parts = token.split(".")
        tampered_token = f"{parts[0]}.{parts[1]}.invalid_signature"

        with self.assertRaises(InvalidTokenException):
            verify_jwt(tampered_token)

    def test_jwt_expiration(self):
        # Token expires in -1 second (already expired)
        token = generate_jwt(user_id=102, email="expired@example.com", expires_in=-1)

        with self.assertRaises(TokenExpiredException):
            verify_jwt(token)
