from app.users.repository import (
    find_user_by_id,
    find_all_users,
    count_all_users,
    assign_role_to_user,
    update_user_status,
    delete_user
)
from app.core.exceptions import UserNotFoundException, AppException

def get_user(user_id):
    user = find_user_by_id(user_id)
    if user is None:
        raise UserNotFoundException(user_id)
    return user

def get_users(page=1, limit=10, search=None):
    users = find_all_users(page=page, limit=limit, search=search)
    total = count_all_users(search=search)
    total_pages = (total + limit - 1) // limit if total > 0 else 0
    return {
        "users": users,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1
        }
    }

def assign_user_role(user_id, role_name):
    get_user(user_id)
    if not role_name or not isinstance(role_name, str):
        raise AppException("Role name is required", 400, "INVALID_ROLE")
    assign_role_to_user(user_id, role_name.upper())
    return get_user(user_id)

def change_user_status(user_id, status):
    get_user(user_id)
    st = status.upper()
    if st not in ["ACTIVE", "INACTIVE", "SUSPENDED"]:
        raise AppException("Status must be ACTIVE, INACTIVE, or SUSPENDED", 400, "INVALID_STATUS")
    update_user_status(user_id, st)
    return get_user(user_id)

def delete_user_account(user_id):
    get_user(user_id)
    deleted = delete_user(user_id)
    if not deleted:
        raise UserNotFoundException(user_id)
    return True
