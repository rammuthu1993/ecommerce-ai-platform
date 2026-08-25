from app.database.connection import get_connection

def save_purchase(supplier_id, items, total_amount, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            """INSERT INTO purchases (supplier_id, status, total_amount) VALUES (?, 'DRAFT', ?)""",
            (supplier_id, total_amount)
        )
        purchase_id = cursor.lastrowid

        for item in items:
            connection.execute(
                """INSERT INTO purchase_items (purchase_id, product_id, quantity, unit_cost) VALUES (?, ?, ?, ?)""",
                (purchase_id, item["product_id"], item["quantity"], item["unit_cost"])
            )

        if close_conn:
            connection.commit()
        return find_purchase_by_id(purchase_id, connection=connection)
    finally:
        if close_conn:
            connection.close()


def find_purchase_by_id(purchase_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        purchase_row = connection.execute(
            """SELECT p.id, p.supplier_id, s.name AS supplier_name, p.status, p.total_amount, p.created_at
               FROM purchases p
               JOIN suppliers s ON p.supplier_id = s.id
               WHERE p.id = ?""",
            (purchase_id,)
        ).fetchone()

        if not purchase_row:
            return None

        purchase = dict(purchase_row)
        item_rows = connection.execute(
            """SELECT pi.id, pi.product_id, prod.name AS product_name, pi.quantity, pi.unit_cost
               FROM purchase_items pi
               JOIN products prod ON pi.product_id = prod.id
               WHERE pi.purchase_id = ?""",
            (purchase_id,)
        ).fetchall()

        purchase["items"] = [dict(row) for row in item_rows]
        return purchase
    finally:
        if close_conn:
            connection.close()


def find_all_purchases(page=1, limit=10, status=None, connection=None):
    offset = (page - 1) * limit
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    query = """SELECT p.id, p.supplier_id, s.name AS supplier_name, p.status, p.total_amount, p.created_at
               FROM purchases p
               JOIN suppliers s ON p.supplier_id = s.id"""
    params = []
    if status:
        query += " WHERE p.status = ?"
        params.append(status)

    query += " ORDER BY p.id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    try:
        rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        if close_conn:
            connection.close()


def update_purchase_status(purchase_id, status, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            "UPDATE purchases SET status = ? WHERE id = ?",
            (status, purchase_id)
        )
        if close_conn:
            connection.commit()
        return cursor.rowcount > 0
    finally:
        if close_conn:
            connection.close()
