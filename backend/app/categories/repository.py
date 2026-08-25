from app.database.connection import get_connection

def save_category(name, description=None, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            """INSERT INTO categories (name, description) VALUES (?, ?)""",
            (name, description)
        )
        if close_conn:
            connection.commit()
        return {"id": cursor.lastrowid, "name": name, "description": description}
    finally:
        if close_conn:
            connection.close()


def find_all_categories(page=1, limit=10, search=None, connection=None):
    offset = (page - 1) * limit
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    query = "SELECT id, name, description, created_at FROM categories"
    params = []

    if search:
        query += " WHERE name LIKE ?"
        params.append(f"%{search}%")

    query += " ORDER BY id ASC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    try:
        rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        if close_conn:
            connection.close()


def count_all_categories(search=None, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    query = "SELECT COUNT(*) AS total FROM categories"
    params = []

    if search:
        query += " WHERE name LIKE ?"
        params.append(f"%{search}%")

    try:
        row = connection.execute(query, params).fetchone()
        return row["total"] if row else 0
    finally:
        if close_conn:
            connection.close()


def find_category_by_id(category_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        row = connection.execute(
            "SELECT id, name, description, created_at FROM categories WHERE id = ?",
            (category_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        if close_conn:
            connection.close()


def find_category_by_name(name, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        row = connection.execute(
            "SELECT id, name, description, created_at FROM categories WHERE name = ?",
            (name,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        if close_conn:
            connection.close()


def update_category(category_id, name, description=None, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            "UPDATE categories SET name = ?, description = ? WHERE id = ?",
            (name, description, category_id)
        )
        if close_conn:
            connection.commit()
        return cursor.rowcount > 0
    finally:
        if close_conn:
            connection.close()


def delete_category(category_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            "DELETE FROM categories WHERE id = ?",
            (category_id,)
        )
        if close_conn:
            connection.commit()
        return cursor.rowcount > 0
    finally:
        if close_conn:
            connection.close()
