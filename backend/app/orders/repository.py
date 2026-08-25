from app.database.connection import get_connection

def save_order(order_number, customer_id, items, subtotal, tax_amount, discount_amount, total_amount, shipping_address_id=None, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            """INSERT INTO orders (order_number, customer_id, status, subtotal, tax_amount, discount_amount, total_amount, shipping_address_id)
               VALUES (?, ?, 'PENDING', ?, ?, ?, ?, ?)""",
            (order_number, customer_id, subtotal, tax_amount, discount_amount, total_amount, shipping_address_id)
        )
        order_id = cursor.lastrowid

        for item in items:
            connection.execute(
                """INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                   VALUES (?, ?, ?, ?)""",
                (order_id, item["product_id"], item["quantity"], item["unit_price"])
            )

        if close_conn:
            connection.commit()
        return find_order_by_id(order_id, connection=connection)
    finally:
        if close_conn:
            connection.close()


def find_order_by_id(order_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        row = connection.execute(
            """SELECT o.id, o.order_number, o.customer_id, c.first_name || ' ' || c.last_name AS customer_name,
                      o.status, o.subtotal, o.tax_amount, o.discount_amount, o.total_amount, o.shipping_address_id, o.created_at
               FROM orders o
               JOIN customers c ON o.customer_id = c.id
               WHERE o.id = ?""",
            (order_id,)
        ).fetchone()

        if not row:
            return None

        order = dict(row)
        item_rows = connection.execute(
            """SELECT oi.id, oi.product_id, p.name AS product_name, oi.quantity, oi.unit_price,
                      (oi.quantity * oi.unit_price) AS line_total
               FROM order_items oi
               JOIN products p ON oi.product_id = p.id
               WHERE oi.order_id = ?""",
            (order_id,)
        ).fetchall()

        order["items"] = [dict(r) for r in item_rows]
        return order
    finally:
        if close_conn:
            connection.close()


def find_all_orders(page=1, limit=10, customer_id=None, status=None, connection=None):
    offset = (page - 1) * limit
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    query = """SELECT o.id, o.order_number, o.customer_id, c.first_name || ' ' || c.last_name AS customer_name,
                      o.status, o.subtotal, o.tax_amount, o.discount_amount, o.total_amount, o.created_at
               FROM orders o
               JOIN customers c ON o.customer_id = c.id"""
    conditions = []
    params = []

    if customer_id:
        conditions.append("o.customer_id = ?")
        params.append(customer_id)
    if status:
        conditions.append("o.status = ?")
        params.append(status)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY o.id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    try:
        rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        if close_conn:
            connection.close()


def count_all_orders(customer_id=None, status=None, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    query = "SELECT COUNT(*) AS total FROM orders"
    conditions = []
    params = []

    if customer_id:
        conditions.append("customer_id = ?")
        params.append(customer_id)
    if status:
        conditions.append("status = ?")
        params.append(status)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    try:
        row = connection.execute(query, params).fetchone()
        return row["total"] if row else 0
    finally:
        if close_conn:
            connection.close()


def update_order_status(order_id, new_status, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
        if close_conn:
            connection.commit()
        return cursor.rowcount > 0
    finally:
        if close_conn:
            connection.close()
