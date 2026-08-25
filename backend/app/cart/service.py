from app.customers.service import get_customer
from app.customers.repository import save_customer
from app.database.repository import find_by_id as find_product_by_id
from app.inventory.service import get_inventory_by_product
from app.cart.repository import (
    get_or_create_cart,
    get_cart_with_items,
    add_item_to_cart,
    update_cart_item_quantity,
    remove_cart_item,
    clear_cart
)
from app.core.exceptions import ProductNotFoundException, InsufficientStockException, CustomerNotFoundException, AppException

def ensure_customer_exists(customer_id, connection=None):
    try:
        return get_customer(customer_id, connection=connection)
    except CustomerNotFoundException:
        return save_customer(
            first_name="Customer",
            last_name=f"#{customer_id}",
            email=f"customer{customer_id}@ecommerce.ai",
            phone="",
            connection=connection
        )

def get_customer_cart(customer_id, connection=None):
    ensure_customer_exists(customer_id, connection=connection)
    return get_cart_with_items(customer_id, connection=connection)

def add_to_cart(customer_id, product_id, quantity, connection=None):
    ensure_customer_exists(customer_id, connection=connection)
    product = find_product_by_id(product_id, connection=connection)
    if product is None:
        raise ProductNotFoundException(product_id)
    if not isinstance(quantity, int) or quantity <= 0:
        raise AppException("Quantity must be a positive integer", 400, "INVALID_CART_ITEM")

    inv = get_inventory_by_product(product_id, connection=connection)
    if inv["available_quantity"] < quantity:
        raise InsufficientStockException(product_id, quantity, inv["available_quantity"])

    cart = get_or_create_cart(customer_id, connection=connection)
    add_item_to_cart(cart_id=cart["id"], product_id=product_id, quantity=quantity, connection=connection)
    return get_cart_with_items(customer_id, connection=connection)

def update_cart_item(customer_id, product_id, quantity, connection=None):
    ensure_customer_exists(customer_id, connection=connection)
    product = find_product_by_id(product_id, connection=connection)
    if product is None:
        raise ProductNotFoundException(product_id)
    if not isinstance(quantity, int) or quantity < 0:
        raise AppException("Quantity must be a non-negative integer", 400, "INVALID_CART_ITEM")

    if quantity > 0:
        inv = get_inventory_by_product(product_id, connection=connection)
        if inv["available_quantity"] < quantity:
            raise InsufficientStockException(product_id, quantity, inv["available_quantity"])

    cart = get_or_create_cart(customer_id, connection=connection)
    update_cart_item_quantity(cart_id=cart["id"], product_id=product_id, quantity=quantity, connection=connection)
    return get_cart_with_items(customer_id, connection=connection)

def remove_from_cart(customer_id, product_id, connection=None):
    ensure_customer_exists(customer_id, connection=connection)
    cart = get_or_create_cart(customer_id, connection=connection)
    remove_cart_item(cart_id=cart["id"], product_id=product_id, connection=connection)
    return get_cart_with_items(customer_id, connection=connection)

def clear_customer_cart(customer_id, connection=None):
    ensure_customer_exists(customer_id, connection=connection)
    cart = get_or_create_cart(customer_id, connection=connection)
    clear_cart(cart_id=cart["id"], connection=connection)
    return get_cart_with_items(customer_id, connection=connection)
