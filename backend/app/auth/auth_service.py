from app.database.transaction import db_transaction
from app.users.repository import (
    save_user,
    find_user_by_email,
    find_user_by_id,
    assign_role_to_user,
    update_user_password
)
from app.auth.password_hasher import hash_password, verify_password
from app.auth.jwt_engine import generate_jwt
from app.core.exceptions import AppException, UserNotFoundException, UnauthorizedException

def register_user(username: str, email: str, password: str, roles: list = None):
    if not username or not isinstance(username, str) or not username.strip():
        raise AppException("Username is required", 400, "INVALID_REGISTRATION")
    if not email or not isinstance(email, str) or "@" not in email:
        raise AppException("Valid email is required", 400, "INVALID_REGISTRATION")
    if not password or not isinstance(password, str) or len(password) < 6:
        raise AppException("Password must be at least 6 characters long", 400, "INVALID_REGISTRATION")

    clean_email = email.strip().lower()
    clean_username = username.strip()

    if find_user_by_email(clean_email):
        raise AppException("User with this email already exists", 400, "DUPLICATE_EMAIL")

    hash_hex, salt_hex = hash_password(password)

    with db_transaction() as conn:
        user = save_user(
            username=clean_username,
            email=clean_email,
            password_hash=hash_hex,
            salt=salt_hex,
            status="ACTIVE",
            connection=conn
        )

        user_roles = roles or ["CUSTOMER"]
        for role in user_roles:
            assign_role_to_user(user["id"], role, connection=conn)

        user["roles"] = user_roles

    token = generate_jwt(user_id=user["id"], email=user["email"], roles=user["roles"])
    return {
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "status": user["status"],
            "roles": user["roles"]
        },
        "access_token": token
    }

def login_user(email: str, password: str):
    if not email or not password:
        raise UnauthorizedException("Email and password are required")

    clean_email = email.strip().lower()
    user = find_user_by_email(clean_email)
    if not user:
        raise UnauthorizedException("Invalid email or password")

    if user["status"] != "ACTIVE":
        raise UnauthorizedException(f"User account is {user['status'].lower()}")

    if not verify_password(password, user["password_hash"], user["salt"]):
        raise UnauthorizedException("Invalid email or password")

    token = generate_jwt(user_id=user["id"], email=user["email"], roles=user["roles"])
    return {
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "status": user["status"],
            "roles": user["roles"]
        },
        "access_token": token
    }

def change_password(user_id: int, old_password: str, new_password: str):
    user = find_user_by_id(user_id)
    if not user:
        raise UserNotFoundException(user_id)

    if not verify_password(old_password, user["password_hash"], user["salt"]):
        raise UnauthorizedException("Incorrect current password")

    if not new_password or len(new_password) < 6:
        raise AppException("New password must be at least 6 characters long", 400, "INVALID_PASSWORD")

    new_hash, new_salt = hash_password(new_password)
    update_user_password(user_id, new_hash, new_salt)
    return True
