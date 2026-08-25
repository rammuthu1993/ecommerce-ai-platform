from app.database.connection import get_connection

def save_discount(code, discount_type, value, min_purchase=0.0, is_active=1, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            """INSERT INTO discounts (code, type, value, min_purchase, is_active)
               VALUES (?, ?, ?, ?, ?)""",
            (code.upper(), discount_type.upper(), value, min_purchase, is_active)
        )
        if close_conn:
            connection.commit()
        return find_discount_by_code(code, connection=connection)
    finally:
        if close_conn:
            connection.close()


def find_discount_by_code(code, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        row = connection.execute(
            "SELECT id, code, type, value, min_purchase, is_active, created_at FROM discounts WHERE code = ?",
            (code.upper(),)
        ).fetchone()
        return dict(row) if row else None
    finally:
        if close_conn:
            connection.close()


def find_all_discounts(connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        rows = connection.execute("SELECT id, code, type, value, min_purchase, is_active, created_at FROM discounts").fetchall()
        return [dict(row) for row in rows]
    finally:
        if close_conn:
            connection.close()
