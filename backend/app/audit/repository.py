from app.database.connection import get_connection

def save_audit_log(action, module, entity, entity_id=None, user_id=None, details=None, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            """INSERT INTO audit_logs (user_id, action, module, entity, entity_id, details)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, action, module, entity, entity_id, str(details) if details else None)
        )
        if close_conn:
            connection.commit()
        return cursor.lastrowid
    finally:
        if close_conn:
            connection.close()


def find_audit_logs(page=1, limit=10, module=None, entity=None, connection=None):
    offset = (page - 1) * limit
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    query = "SELECT id, user_id, action, module, entity, entity_id, details, timestamp FROM audit_logs"
    conditions = []
    params = []

    if module:
        conditions.append("module = ?")
        params.append(module)
    if entity:
        conditions.append("entity = ?")
        params.append(entity)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    try:
        rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        if close_conn:
            connection.close()
