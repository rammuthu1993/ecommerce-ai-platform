from app.customers.repository import (
    save_customer,
    find_all_customers,
    count_all_customers,
    find_customer_by_id,
    find_customer_by_email,
    update_customer,
    delete_customer,
    save_customer_address,
    find_addresses_by_customer_id,
    find_address_by_id,
    delete_customer_address
)
from app.core.exceptions import CustomerNotFoundException, AddressNotFoundException, AppException

def validate_customer_payload(data):
    if not isinstance(data, dict):
        raise AppException("Invalid customer payload", 400, "INVALID_CUSTOMER")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")

    if not first_name or not isinstance(first_name, str) or not first_name.strip():
        raise AppException("First name is required", 400, "INVALID_CUSTOMER")
    if not last_name or not isinstance(last_name, str) or not last_name.strip():
        raise AppException("Last name is required", 400, "INVALID_CUSTOMER")
    if not email or not isinstance(email, str) or "@" not in email:
        raise AppException("Valid email is required", 400, "INVALID_CUSTOMER")

def create_customer(data, connection=None):
    validate_customer_payload(data)
    email = data["email"].strip().lower()
    if find_customer_by_email(email, connection=connection):
        raise AppException("Customer with this email already exists", 400, "DUPLICATE_EMAIL")

    return save_customer(
        first_name=data["first_name"].strip(),
        last_name=data["last_name"].strip(),
        email=email,
        phone=data.get("phone"),
        connection=connection
    )

def get_customers(page=1, limit=10, search=None, connection=None):
    customers = find_all_customers(page=page, limit=limit, search=search, connection=connection)
    total = count_all_customers(search=search, connection=connection)
    total_pages = (total + limit - 1) // limit if total > 0 else 0
    return {
        "customers": customers,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1
        }
    }

def get_customer(customer_id, connection=None):
    c = find_customer_by_id(customer_id, connection=connection)
    if c is None:
        raise CustomerNotFoundException(customer_id)
    return c

def update_customer_service(customer_id, data, connection=None):
    existing = get_customer(customer_id, connection=connection)
    validate_customer_payload(data)
    email = data["email"].strip().lower()
    if email != existing["email"] and find_customer_by_email(email, connection=connection):
        raise AppException("Customer with this email already exists", 400, "DUPLICATE_EMAIL")

    updated = update_customer(
        customer_id=customer_id,
        first_name=data["first_name"].strip(),
        last_name=data["last_name"].strip(),
        email=email,
        phone=data.get("phone", existing.get("phone")),
        connection=connection
    )
    if not updated:
        raise CustomerNotFoundException(customer_id)
    return get_customer(customer_id, connection=connection)

def delete_customer_service(customer_id, connection=None):
    get_customer(customer_id, connection=connection)
    deleted = delete_customer(customer_id, connection=connection)
    if not deleted:
        raise CustomerNotFoundException(customer_id)
    return True

def add_customer_address(customer_id, data, connection=None):
    get_customer(customer_id, connection=connection)
    if not isinstance(data, dict):
        raise AppException("Invalid address payload", 400, "INVALID_ADDRESS")

    address_type = data.get("address_type", "SHIPPING").upper()
    if address_type not in ["BILLING", "SHIPPING"]:
        raise AppException("Address type must be BILLING or SHIPPING", 400, "INVALID_ADDRESS")

    street = data.get("street")
    city = data.get("city")
    postal_code = data.get("postal_code")
    country = data.get("country")

    if not street or not city or not postal_code or not country:
        raise AppException("Street, city, postal_code, and country are required", 400, "INVALID_ADDRESS")

    return save_customer_address(
        customer_id=customer_id,
        address_type=address_type,
        street=street,
        city=city,
        state=data.get("state"),
        postal_code=postal_code,
        country=country,
        is_default=1 if data.get("is_default") else 0,
        connection=connection
    )

def get_customer_addresses(customer_id, connection=None):
    get_customer(customer_id, connection=connection)
    return find_addresses_by_customer_id(customer_id, connection=connection)

def delete_address_service(address_id, connection=None):
    addr = find_address_by_id(address_id, connection=connection)
    if addr is None:
        raise AddressNotFoundException(address_id)
    deleted = delete_customer_address(address_id, connection=connection)
    if not deleted:
        raise AddressNotFoundException(address_id)
    return True
