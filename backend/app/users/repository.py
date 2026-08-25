from app.database.connection import get_connection

def save_user(username, email, password_hash, salt, status="ACTIVE", connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            """INSERT INTO users (username, email, password_hash, salt, status)
               VALUES (?, ?, ?, ?, ?)""",
            (username, email, password_hash, salt, status)
        )
        if close_conn:
            connection.commit()
        return find_user_by_id(cursor.lastrowid, connection=connection)
    finally:
        if close_conn:
            connection.close()


def find_user_by_id(user_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        row = connection.execute(
            """SELECT id, username, email, password_hash, salt, status, created_at, updated_at
               FROM users WHERE id = ?""",
            (user_id,)
        ).fetchone()

        if not row:
            return None

        user = dict(row)
        user["roles"] = get_user_roles(user_id, connection=connection)
        user["permissions"] = get_user_permissions(user_id, connection=connection)
        return user
    finally:
        if close_conn:
            connection.close()


def find_user_by_email(email, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        row = connection.execute(
            """SELECT id, username, email, password_hash, salt, status, created_at, updated_at
               FROM users WHERE email = ?""",
            (email,)
        ).fetchone()

        if not row:
            return None

        user = dict(row)
        user["roles"] = get_user_roles(user["id"], connection=connection)
        user["permissions"] = get_user_permissions(user["id"], connection=connection)
        return user
    finally:
        if close_conn:
            connection.close()


def find_all_users(page=1, limit=10, search=None, connection=None):
    offset = (page - 1) * limit
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    query = "SELECT id, username, email, status, created_at FROM users"
    params = []
    if search:
        query += " WHERE username LIKE ? OR email LIKE ?"
        params.extend([f"%{search}%", f"%{search}%"])

    query += " ORDER BY id ASC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    try:
        rows = connection.execute(query, params).fetchall()
        result = []
        for r in rows:
            u = dict(r)
            u["roles"] = get_user_roles(u["id"], connection=connection)
            result.append(u)
        return result
    finally:
        if close_conn:
            connection.close()


def count_all_users(search=None, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    query = "SELECT COUNT(*) AS total FROM users"
    params = []
    if search:
        query += " WHERE username LIKE ? OR email LIKE ?"
        params.extend([f"%{search}%", f"%{search}%"])

    try:
        row = connection.execute(query, params).fetchone()
        return row["total"] if row else 0
    finally:
        if close_conn:
            connection.close()


def update_user_status(user_id, status, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute("UPDATE users SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (status, user_id))
        if close_conn:
            connection.commit()
        return cursor.rowcount > 0
    finally:
        if close_conn:
            connection.close()


def update_user_password(user_id, password_hash, salt, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute("UPDATE users SET password_hash = ?, salt = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (password_hash, salt, user_id))
        if close_conn:
            connection.commit()
        return cursor.rowcount > 0
    finally:
        if close_conn:
            connection.close()


def delete_user(user_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute("DELETE FROM users WHERE id = ?", (user_id,))
        if close_conn:
            connection.commit()
        return cursor.rowcount > 0
    finally:
        if close_conn:
            connection.close()


# Role & Permission Queries
def assign_role_to_user(user_id, role_name, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        role_row = connection.execute("SELECT id FROM roles WHERE name = ?", (role_name.upper(),)).fetchone()
        if not role_row:
            cursor = connection.execute("INSERT INTO roles (name, description) VALUES (?, ?)", (role_name.upper(), f"{role_name} Role"))
            role_id = cursor.lastrowid
        else:
            role_id = role_row["id"]

        connection.execute(
            """INSERT OR IGNORE INTO user_roles (user_id, role_id) VALUES (?, ?)""",
            (user_id, role_id)
        )
        if close_conn:
            connection.commit()
        return True
    finally:
        if close_conn:
            connection.close()


def get_user_roles(user_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        rows = connection.execute(
            """SELECT r.name FROM roles r
               JOIN user_roles ur ON r.id = ur.role_id
               WHERE ur.user_id = ?""",
            (user_id,)
        ).fetchall()
        return [row["name"] for row in rows]
    finally:
        if close_conn:
            connection.close()


def get_user_permissions(user_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        rows = connection.execute(
            """SELECT DISTINCT p.name FROM permissions p
               JOIN role_permissions rp ON p.id = rp.permission_id
               JOIN user_roles ur ON rp.role_id = ur.role_id
               WHERE ur.user_id = ?""",
            (user_id,)
        ).fetchall()
        return [row["name"] for row in rows]
    finally:
        if close_conn:
            connection.close()
