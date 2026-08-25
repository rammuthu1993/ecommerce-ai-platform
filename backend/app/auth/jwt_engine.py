import base64
import hmac
import hashlib
import json
import time
import os

from app.core.exceptions import InvalidTokenException, TokenExpiredException

SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-ecommerce-ai-platform-jwt-key-2026")

def base64url_encode(input_bytes: bytes) -> str:
    return base64.urlsafe_b64encode(input_bytes).decode("utf-8").rstrip("=")

def base64url_decode(input_str: str) -> bytes:
    remainder = len(input_str) % 4
    if remainder > 0:
        input_str += "=" * (4 - remainder)
    return base64.urlsafe_b64decode(input_str.encode("utf-8"))

def generate_jwt(user_id, email: str, roles: list = None, expires_in: int = 3600, secret_key: str = None) -> str:
    secret = secret_key or SECRET_KEY
    now = int(time.time())

    header = {
        "alg": "HS256",
        "typ": "JWT"
    }

    payload = {
        "sub": user_id,
        "email": email,
        "roles": roles or ["CUSTOMER"],
        "iat": now,
        "exp": now + expires_in
    }

    header_bytes = json.dumps(header, separators=(",", ":")).encode("utf-8")
    payload_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")

    header_b64 = base64url_encode(header_bytes)
    payload_b64 = base64url_encode(payload_bytes)

    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    signature_b64 = base64url_encode(signature)

    return f"{header_b64}.{payload_b64}.{signature_b64}"

def verify_jwt(token: str, secret_key: str = None) -> dict:
    if not token or not isinstance(token, str):
        raise InvalidTokenException("Token must be a non-empty string")

    parts = token.split(".")
    if len(parts) != 3:
        raise InvalidTokenException("Token structure is invalid")

    header_b64, payload_b64, signature_b64 = parts
    secret = secret_key or SECRET_KEY

    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    expected_signature = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    expected_signature_b64 = base64url_encode(expected_signature)

    if not hmac.compare_digest(signature_b64, expected_signature_b64):
        raise InvalidTokenException("Token signature verification failed")

    try:
        payload_bytes = base64url_decode(payload_b64)
        payload = json.loads(payload_bytes.decode("utf-8"))
    except Exception:
        raise InvalidTokenException("Failed to decode token payload")

    now = int(time.time())
    exp = payload.get("exp")
    if exp and now > exp:
        raise TokenExpiredException("Token has expired")

    return payload
