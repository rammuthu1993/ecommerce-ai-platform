import time
import random
from app.invoices.repository import save_invoice, find_invoice_by_id, find_invoice_by_order_id
from app.orders.repository import find_order_by_id
from app.core.exceptions import OrderNotFoundException, AppException

def generate_invoice_number():
    timestamp = int(time.time())
    rand = random.randint(1000, 9999)
    return f"INV-{timestamp}-{rand}"

def create_invoice_for_order(order_id, connection=None):
    existing = find_invoice_by_order_id(order_id, connection=connection)
    if existing:
        return existing

    order = find_order_by_id(order_id, connection=connection)
    if not order:
        raise OrderNotFoundException(order_id)

    inv_num = generate_invoice_number()
    return save_invoice(
        invoice_number=inv_num,
        order_id=order_id,
        subtotal=order["subtotal"],
        tax=order["tax_amount"],
        discount=order["discount_amount"],
        total=order["total_amount"],
        connection=connection
    )

def get_invoice_by_order(order_id):
    inv = find_invoice_by_order_id(order_id)
    if not inv:
        raise AppException(f"Invoice for order {order_id} not found", 404, "INVOICE_NOT_FOUND")
    return inv
