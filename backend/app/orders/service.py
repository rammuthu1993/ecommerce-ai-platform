import time
import random
from app.database.transaction import db_transaction
from app.cart.service import get_customer_cart, clear_customer_cart
from app.inventory.service import reserve_stock, release_stock, adjust_stock, get_inventory_by_product
from app.customers.service import get_customer
from app.orders.repository import (
    save_order,
    find_order_by_id,
    find_all_orders,
    count_all_orders,
    update_order_status
)
from app.core.exceptions import (
    OrderNotFoundException,
    InvalidOrderTransitionException,
    InsufficientStockException,
    AppException
)

VALID_TRANSITIONS = {
    "PENDING": ["CONFIRMED", "CANCELLED"],
    "CONFIRMED": ["PROCESSING", "CANCELLED"],
    "PROCESSING": ["SHIPPED", "CANCELLED"],
    "SHIPPED": ["DELIVERED"],
    "DELIVERED": [],
    "CANCELLED": []
}

def generate_order_number():
    timestamp = int(time.time())
    rand = random.randint(1000, 9999)
    return f"ORD-{timestamp}-{rand}"

def checkout_order(customer_id, shipping_address_id=None, tax_rate=0.10, discount_amount=0.0):
    get_customer(customer_id)
    cart = get_customer_cart(customer_id)

    if not cart["items"]:
        raise AppException("Cannot checkout with an empty cart", 400, "EMPTY_CART")

    order_number = generate_order_number()
    items = []
    subtotal = 0.0

    with db_transaction() as conn:
        for cart_item in cart["items"]:
            product_id = cart_item["product_id"]
            qty = cart_item["quantity"]
            price = float(cart_item["price"])

            inv = get_inventory_by_product(product_id, connection=conn)
            if inv["available_quantity"] < qty:
                raise InsufficientStockException(product_id, qty, inv["available_quantity"])

            line_subtotal = price * qty
            subtotal += line_subtotal
            items.append({
                "product_id": product_id,
                "quantity": qty,
                "unit_price": price
            })

        effective_discount = min(discount_amount, subtotal)
        taxable_amount = max(0.0, subtotal - effective_discount)
        tax_amount = round(taxable_amount * tax_rate, 2)
        total_amount = round(taxable_amount + tax_amount, 2)

        order = save_order(
            order_number=order_number,
            customer_id=customer_id,
            items=items,
            subtotal=subtotal,
            tax_amount=tax_amount,
            discount_amount=effective_discount,
            total_amount=total_amount,
            shipping_address_id=shipping_address_id,
            connection=conn
        )

        for item in items:
            reserve_stock(
                product_id=item["product_id"],
                quantity=item["quantity"],
                reference_type="ORDER",
                reference_id=order["id"],
                connection=conn
            )

        clear_customer_cart(customer_id, connection=conn)
        return order

def get_order(order_id, connection=None):
    order = find_order_by_id(order_id, connection=connection)
    if order is None:
        raise OrderNotFoundException(order_id)
    return order

def get_orders(page=1, limit=10, customer_id=None, status=None, connection=None):
    orders = find_all_orders(page=page, limit=limit, customer_id=customer_id, status=status, connection=connection)
    total = count_all_orders(customer_id=customer_id, status=status, connection=connection)
    total_pages = (total + limit - 1) // limit if total > 0 else 0
    return {
        "orders": orders,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1
        }
    }

def update_order_status_service(order_id, target_status):
    order = get_order(order_id)
    current_status = order["status"]

    target_status = target_status.upper()
    allowed = VALID_TRANSITIONS.get(current_status, [])

    if target_status not in allowed:
        raise InvalidOrderTransitionException(current_status, target_status)

    with db_transaction() as conn:
        if target_status == "CANCELLED":
            for item in order["items"]:
                if current_status in ["PENDING", "CONFIRMED"]:
                    release_stock(item["product_id"], item["quantity"], reference_type="ORDER", reference_id=order_id, connection=conn)
                elif current_status in ["PROCESSING", "SHIPPED"]:
                    adjust_stock(item["product_id"], item["quantity"], tx_type="STOCK_IN", reference_type="ORDER_CANCEL", reference_id=order_id, connection=conn)
        elif target_status == "PROCESSING" and current_status == "CONFIRMED":
            for item in order["items"]:
                release_stock(item["product_id"], item["quantity"], reference_type="ORDER", reference_id=order_id, connection=conn)
                adjust_stock(item["product_id"], -item["quantity"], tx_type="STOCK_OUT", reference_type="ORDER_SHIPPED", reference_id=order_id, connection=conn)

        update_order_status(order_id, target_status, connection=conn)
        return find_order_by_id(order_id, connection=conn)
