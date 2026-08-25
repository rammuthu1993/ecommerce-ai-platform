from app.database.connection import get_connection

def get_or_create_cart(customer_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        row = connection.execute(
            "SELECT id, customer_id, created_at, updated_at FROM carts WHERE customer_id = ?",
            (customer_id,)
        ).fetchone()
        print(row,"row")
        if row:
            return dict(row)

        cursor = connection.execute(
            "INSERT INTO carts (customer_id) VALUES (?)",
            (customer_id,)
        )
        if close_conn:
            connection.commit()
        return {"id": cursor.lastrowid, "customer_id": customer_id}
    finally:
        if close_conn:
            connection.close()


def get_cart_with_items(customer_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cart = get_or_create_cart(customer_id, connection=connection)
        items_rows = connection.execute(
            """SELECT ci.id, ci.cart_id, ci.product_id, p.name AS product_name, p.price, ci.quantity,
                      (p.price * ci.quantity) AS item_total
               FROM cart_items ci
               JOIN products p ON ci.product_id = p.id
               WHERE ci.cart_id = ?""",
            (cart["id"],)
        ).fetchall()
        print(items_rows,"itms")
        items = [dict(row) for row in items_rows]
        total_amount = sum(item["item_total"] for item in items)
        cart["items"] = items
        cart["total_amount"] = total_amount
        return cart
    finally:
        if close_conn:
            connection.close()


def add_item_to_cart(cart_id, product_id, quantity, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            """INSERT INTO cart_items (cart_id, product_id, quantity)
               VALUES (?, ?, ?)
               ON CONFLICT(cart_id, product_id) DO UPDATE SET
               quantity = cart_items.quantity + excluded.quantity""",
            (cart_id, product_id, quantity)
        )
        connection.execute("UPDATE carts SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (cart_id,))
        if close_conn:
            connection.commit()
        return cursor.lastrowid
    finally:
        if close_conn:
            connection.close()


def update_cart_item_quantity(cart_id, product_id, quantity, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        if quantity <= 0:
            cursor = connection.execute("DELETE FROM cart_items WHERE cart_id = ? AND product_id = ?", (cart_id, product_id))
        else:
            cursor = connection.execute(
                "UPDATE cart_items SET quantity = ? WHERE cart_id = ? AND product_id = ?",
                (quantity, cart_id, product_id)
            )
        connection.execute("UPDATE carts SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (cart_id,))
        if close_conn:
            connection.commit()
        return cursor.rowcount > 0
    finally:
        if close_conn:
            connection.close()


def remove_cart_item(cart_id, product_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute("DELETE FROM cart_items WHERE cart_id = ? AND product_id = ?", (cart_id, product_id))
        connection.execute("UPDATE carts SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (cart_id,))
        if close_conn:
            connection.commit()
        return cursor.rowcount > 0
    finally:
        if close_conn:
            connection.close()


def clear_cart(cart_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute("DELETE FROM cart_items WHERE cart_id = ?", (cart_id,))
        connection.execute("UPDATE carts SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (cart_id,))
        if close_conn:
            connection.commit()
        return cursor.rowcount > 0
    finally:
        if close_conn:
            connection.close()
