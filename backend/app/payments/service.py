from app.database.transaction import db_transaction
from app.orders.repository import find_order_by_id, update_order_status
from app.invoices.service import create_invoice_for_order
from app.payments.repository import save_payment, find_payments_by_order_id, find_payment_by_id
from app.core.exceptions import OrderNotFoundException, AppException

def record_payment(order_id, payment_method, amount, transaction_reference=None):
    order = find_order_by_id(order_id)
    if not order:
        raise OrderNotFoundException(order_id)

    if order["status"] == "CANCELLED":
        raise AppException("Cannot process payment for a cancelled order", 400, "ORDER_CANCELLED")

    if abs(float(amount) - float(order["total_amount"])) > 0.01:
        raise AppException(f"Payment amount {amount} does not match order total {order['total_amount']}", 400, "INVALID_PAYMENT_AMOUNT")

    with db_transaction() as conn:
        payment = save_payment(
            order_id=order_id,
            payment_method=payment_method.upper(),
            amount=float(amount),
            status="COMPLETED",
            transaction_reference=transaction_reference,
            connection=conn
        )

        if order["status"] == "PENDING":
            update_order_status(order_id, "CONFIRMED", connection=conn)

        invoice = create_invoice_for_order(order_id, connection=conn)

    return {
        "payment": payment,
        "invoice": invoice
    }

def get_payments_for_order(order_id):
    order = find_order_by_id(order_id)
    if not order:
        raise OrderNotFoundException(order_id)
    return find_payments_by_order_id(order_id)
