from app.database.connection import get_connection

def save_inventory(product_id, stock_quantity=0, reserved_quantity=0, location=None, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            """INSERT INTO inventory (product_id, stock_quantity, reserved_quantity, location)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(product_id) DO UPDATE SET
               stock_quantity = excluded.stock_quantity,
               location = coalesce(excluded.location, inventory.location),
               updated_at = CURRENT_TIMESTAMP""",
            (product_id, stock_quantity, reserved_quantity, location)
        )
        if close_conn:
            connection.commit()
        return find_inventory_by_product_id(product_id, connection=connection)
    finally:
        if close_conn:
            connection.close()


def find_inventory_by_product_id(product_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        row = connection.execute(
            """SELECT id, product_id, stock_quantity, reserved_quantity,
                      (stock_quantity - reserved_quantity) AS available_quantity,
                      location, updated_at
               FROM inventory WHERE product_id = ?""",
            (product_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        if close_conn:
            connection.close()


def find_inventory_by_id(inventory_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        row = connection.execute(
            """SELECT id, product_id, stock_quantity, reserved_quantity,
                      (stock_quantity - reserved_quantity) AS available_quantity,
                      location, updated_at
               FROM inventory WHERE id = ?""",
            (inventory_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        if close_conn:
            connection.close()


def find_all_inventory(page=1, limit=10, connection=None):
    offset = (page - 1) * limit
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        rows = connection.execute(
            """SELECT i.id, i.product_id, p.name AS product_name, i.stock_quantity, i.reserved_quantity,
                      (i.stock_quantity - i.reserved_quantity) AS available_quantity, i.location, i.updated_at
               FROM inventory i
               LEFT JOIN products p ON i.product_id = p.id
               ORDER BY i.id ASC LIMIT ? OFFSET ?""",
            (limit, offset)
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        if close_conn:
            connection.close()


def update_inventory_stock(product_id, stock_change=0, reserved_change=0, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            """UPDATE inventory
               SET stock_quantity = stock_quantity + ?,
                   reserved_quantity = reserved_quantity + ?,
                   updated_at = CURRENT_TIMESTAMP
               WHERE product_id = ?""",
            (stock_change, reserved_change, product_id)
        )
        # Also sync product table quantity
        connection.execute(
            """UPDATE products SET quantity = (SELECT stock_quantity FROM inventory WHERE product_id = ?) WHERE id = ?""",
            (product_id, product_id)
        )
        if close_conn:
            connection.commit()
        return cursor.rowcount > 0
    finally:
        if close_conn:
            connection.close()


def save_inventory_transaction(inventory_id, tx_type, quantity, reference_type=None, reference_id=None, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            """INSERT INTO inventory_transactions (inventory_id, type, quantity, reference_type, reference_id)
               VALUES (?, ?, ?, ?, ?)""",
            (inventory_id, tx_type, quantity, reference_type, reference_id)
        )
        if close_conn:
            connection.commit()
        return cursor.lastrowid
    finally:
        if close_conn:
            connection.close()


def get_inventory_transactions(inventory_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        rows = connection.execute(
            """SELECT id, inventory_id, type, quantity, reference_type, reference_id, created_at
               FROM inventory_transactions
               WHERE inventory_id = ?
               ORDER BY id DESC""",
            (inventory_id,)
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        if close_conn:
            connection.close()


def find_low_stock_inventory(threshold=5, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        rows = connection.execute(
            """SELECT i.id, i.product_id, p.name AS product_name, i.stock_quantity, i.reserved_quantity,
                      (i.stock_quantity - i.reserved_quantity) AS available_quantity, i.location
               FROM inventory i
               JOIN products p ON i.product_id = p.id
               WHERE (i.stock_quantity - i.reserved_quantity) > 0 AND (i.stock_quantity - i.reserved_quantity) <= ?
               ORDER BY available_quantity ASC""",
            (threshold,)
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        if close_conn:
            connection.close()


def find_out_of_stock_inventory(connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        rows = connection.execute(
            """SELECT i.id, i.product_id, p.name AS product_name, i.stock_quantity, i.reserved_quantity,
                      (i.stock_quantity - i.reserved_quantity) AS available_quantity, i.location
               FROM inventory i
               JOIN products p ON i.product_id = p.id
               WHERE (i.stock_quantity - i.reserved_quantity) <= 0
               ORDER BY i.id ASC"""
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        if close_conn:
            connection.close()
