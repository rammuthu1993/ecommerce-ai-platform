from app.database.connection import get_connection

def save_supplier(name, contact_email=None, phone=None, address=None, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            """INSERT INTO suppliers (name, contact_email, phone, address) VALUES (?, ?, ?, ?)""",
            (name, contact_email, phone, address)
        )
        if close_conn:
            connection.commit()
        return {"id": cursor.lastrowid, "name": name, "contact_email": contact_email, "phone": phone, "address": address}
    finally:
        if close_conn:
            connection.close()


def find_all_suppliers(page=1, limit=10, search=None, connection=None):
    offset = (page - 1) * limit
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    query = "SELECT id, name, contact_email, phone, address, created_at FROM suppliers"
    params = []
    if search:
        query += " WHERE name LIKE ? OR contact_email LIKE ?"
        params.extend([f"%{search}%", f"%{search}%"])

    query += " ORDER BY id ASC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    try:
        rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        if close_conn:
            connection.close()


def count_all_suppliers(search=None, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    query = "SELECT COUNT(*) AS total FROM suppliers"
    params = []
    if search:
        query += " WHERE name LIKE ? OR contact_email LIKE ?"
        params.extend([f"%{search}%", f"%{search}%"])

    try:
        row = connection.execute(query, params).fetchone()
        return row["total"] if row else 0
    finally:
        if close_conn:
            connection.close()


def find_supplier_by_id(supplier_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        row = connection.execute(
            "SELECT id, name, contact_email, phone, address, created_at FROM suppliers WHERE id = ?",
            (supplier_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        if close_conn:
            connection.close()


def update_supplier(supplier_id, name, contact_email=None, phone=None, address=None, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            "UPDATE suppliers SET name = ?, contact_email = ?, phone = ?, address = ? WHERE id = ?",
            (name, contact_email, phone, address, supplier_id)
        )
        if close_conn:
            connection.commit()
        return cursor.rowcount > 0
    finally:
        if close_conn:
            connection.close()


def delete_supplier(supplier_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            "DELETE FROM suppliers WHERE id = ?",
            (supplier_id,)
        )
        if close_conn:
            connection.commit()
        return cursor.rowcount > 0
    finally:
        if close_conn:
            connection.close()
