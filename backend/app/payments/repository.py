from app.database.connection import get_connection

def save_payment(order_id, payment_method, amount, status="COMPLETED", transaction_reference=None, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            """INSERT INTO payments (order_id, payment_method, status, transaction_reference, amount)
               VALUES (?, ?, ?, ?, ?)""",
            (order_id, payment_method, status, transaction_reference, amount)
        )
        if close_conn:
            connection.commit()
        return find_payment_by_id(cursor.lastrowid, connection=connection)
    finally:
        if close_conn:
            connection.close()


def find_payment_by_id(payment_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        row = connection.execute(
            "SELECT id, order_id, payment_method, status, transaction_reference, amount, created_at FROM payments WHERE id = ?",
            (payment_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        if close_conn:
            connection.close()


def find_payments_by_order_id(order_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        rows = connection.execute(
            "SELECT id, order_id, payment_method, status, transaction_reference, amount, created_at FROM payments WHERE order_id = ?",
            (order_id,)
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        if close_conn:
            connection.close()
