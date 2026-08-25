from app.database.connection import get_connection

def save_invoice(invoice_number, order_id, subtotal, tax, discount, total, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            """INSERT INTO invoices (invoice_number, order_id, subtotal, tax, discount, total)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (invoice_number, order_id, subtotal, tax, discount, total)
        )
        if close_conn:
            connection.commit()
        return find_invoice_by_id(cursor.lastrowid, connection=connection)
    finally:
        if close_conn:
            connection.close()


def find_invoice_by_id(invoice_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        row = connection.execute(
            "SELECT id, invoice_number, order_id, subtotal, tax, discount, total, issued_at FROM invoices WHERE id = ?",
            (invoice_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        if close_conn:
            connection.close()


def find_invoice_by_order_id(order_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        row = connection.execute(
            "SELECT id, invoice_number, order_id, subtotal, tax, discount, total, issued_at FROM invoices WHERE order_id = ?",
            (order_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        if close_conn:
            connection.close()
