from app.suppliers.repository import (
    save_supplier,
    find_all_suppliers,
    count_all_suppliers,
    find_supplier_by_id,
    update_supplier,
    delete_supplier
)
from app.core.exceptions import SupplierNotFoundException, AppException

def validate_supplier_data(data):
    if not isinstance(data, dict):
        raise AppException("Invalid supplier payload", 400, "INVALID_SUPPLIER")
    name = data.get("name")
    if not name or not isinstance(name, str) or not name.strip():
        raise AppException("Supplier name is required", 400, "INVALID_SUPPLIER")

def get_suppliers(page=1, limit=10, search=None):
    suppliers = find_all_suppliers(page=page, limit=limit, search=search)
    total = count_all_suppliers(search=search)
    total_pages = (total + limit - 1) // limit if total > 0 else 0
    return {
        "suppliers": suppliers,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1
        }
    }

def create_supplier(data):
    validate_supplier_data(data)
    return save_supplier(
        name=data["name"].strip(),
        contact_email=data.get("contact_email"),
        phone=data.get("phone"),
        address=data.get("address")
    )

def get_supplier(supplier_id):
    supplier = find_supplier_by_id(supplier_id)
    if supplier is None:
        raise SupplierNotFoundException(supplier_id)
    return supplier

def update_supplier_service(supplier_id, data):
    existing = get_supplier(supplier_id)
    validate_supplier_data(data)
    updated = update_supplier(
        supplier_id=supplier_id,
        name=data["name"].strip(),
        contact_email=data.get("contact_email", existing.get("contact_email")),
        phone=data.get("phone", existing.get("phone")),
        address=data.get("address", existing.get("address"))
    )
    if not updated:
        raise SupplierNotFoundException(supplier_id)
    return get_supplier(supplier_id)

def delete_supplier_service(supplier_id):
    get_supplier(supplier_id)
    deleted = delete_supplier(supplier_id)
    if not deleted:
        raise SupplierNotFoundException(supplier_id)
    return True
