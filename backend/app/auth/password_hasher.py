import hashlib
import os

ITERATIONS = 100000
HASH_ALGORITHM = "sha256"

def hash_password(plain_password: str) -> tuple[str, str]:
    if not plain_password or not isinstance(plain_password, str):
        raise ValueError("Password must be a non-empty string")

    salt_bytes = os.urandom(32)
    salt_hex = salt_bytes.hex()

    hash_bytes = hashlib.pbkdf2_hmac(
        HASH_ALGORITHM,
        plain_password.encode("utf-8"),
        salt_bytes,
        ITERATIONS
    )
    hash_hex = hash_bytes.hex()
    return hash_hex, salt_hex

def verify_password(plain_password: str, hash_hex: str, salt_hex: str) -> bool:
    if not plain_password or not hash_hex or not salt_hex:
        return False

    try:
        salt_bytes = bytes.fromhex(salt_hex)
        expected_hash = hashlib.pbkdf2_hmac(
            HASH_ALGORITHM,
            plain_password.encode("utf-8"),
            salt_bytes,
            ITERATIONS
        ).hex()

        return hmac_compare_strings(expected_hash, hash_hex)
    except Exception:
        return False

def hmac_compare_strings(a: str, b: str) -> bool:
    """Constant-time string comparison to prevent timing attacks."""
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)
    return result == 0
