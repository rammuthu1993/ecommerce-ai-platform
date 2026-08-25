from app.categories.repository import (
    find_all_categories,
    count_all_categories,
    save_category,
    find_category_by_id,
    update_category,
    delete_category
)
from app.core.exceptions import CategoryNotFoundException, AppException

def validate_category_data(data):
    if not isinstance(data, dict):
        raise AppException("Invalid category payload", 400, "INVALID_CATEGORY")
    name = data.get("name")
    if not name or not isinstance(name, str) or not name.strip():
        raise AppException("Category name is required", 400, "INVALID_CATEGORY")

def get_categories(page=1, limit=10, search=None):
    categories = find_all_categories(page=page, limit=limit, search=search)
    total = count_all_categories(search=search)
    total_pages = (total + limit - 1) // limit if total > 0 else 0

    return {
        "categories": categories,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1
        }
    }

def create_category(data):
    validate_category_data(data)
    name = data["name"].strip()
    description = data.get("description")
    return save_category(name=name, description=description)

def get_category(category_id):
    category = find_category_by_id(category_id)
    if category is None:
        raise CategoryNotFoundException(category_id)
    return category

def update_category_service(category_id, data):
    existing = get_category(category_id)
    validate_category_data(data)
    name = data["name"].strip()
    description = data.get("description", existing.get("description"))

    updated = update_category(category_id, name, description)
    if not updated:
        raise CategoryNotFoundException(category_id)
    return {"id": category_id, "name": name, "description": description}

def delete_category_service(category_id):
    get_category(category_id)
    deleted = delete_category(category_id)
    if not deleted:
        raise CategoryNotFoundException(category_id)
    return True
