from app.database.connection import get_connection

def save_customer(first_name, last_name, email, phone=None, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            """INSERT INTO customers (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)""",
            (first_name, last_name, email, phone)
        )
        if close_conn:
            connection.commit()
        return {"id": cursor.lastrowid, "first_name": first_name, "last_name": last_name, "email": email, "phone": phone}
    finally:
        if close_conn:
            connection.close()


def find_all_customers(page=1, limit=10, search=None, connection=None):
    offset = (page - 1) * limit
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    query = "SELECT id, first_name, last_name, email, phone, created_at FROM customers"
    params = []
    if search:
        query += " WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ?"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])

    query += " ORDER BY id ASC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    try:
        rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        if close_conn:
            connection.close()


def count_all_customers(search=None, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    query = "SELECT COUNT(*) AS total FROM customers"
    params = []
    if search:
        query += " WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ?"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%"])

    try:
        row = connection.execute(query, params).fetchone()
        return row["total"] if row else 0
    finally:
        if close_conn:
            connection.close()


def find_customer_by_id(customer_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        row = connection.execute(
            "SELECT id, first_name, last_name, email, phone, created_at FROM customers WHERE id = ?",
            (customer_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        if close_conn:
            connection.close()


def find_customer_by_email(email, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        row = connection.execute(
            "SELECT id, first_name, last_name, email, phone, created_at FROM customers WHERE email = ?",
            (email,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        if close_conn:
            connection.close()


def update_customer(customer_id, first_name, last_name, email, phone=None, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            "UPDATE customers SET first_name = ?, last_name = ?, email = ?, phone = ? WHERE id = ?",
            (first_name, last_name, email, phone, customer_id)
        )
        if close_conn:
            connection.commit()
        return cursor.rowcount > 0
    finally:
        if close_conn:
            connection.close()


def delete_customer(customer_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        if close_conn:
            connection.commit()
        return cursor.rowcount > 0
    finally:
        if close_conn:
            connection.close()


def save_customer_address(customer_id, address_type, street, city, state, postal_code, country, is_default=0, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        if is_default:
            connection.execute(
                "UPDATE customer_addresses SET is_default = 0 WHERE customer_id = ? AND address_type = ?",
                (customer_id, address_type)
            )

        cursor = connection.execute(
            """INSERT INTO customer_addresses (customer_id, address_type, street, city, state, postal_code, country, is_default)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (customer_id, address_type, street, city, state, postal_code, country, is_default)
        )
        if close_conn:
            connection.commit()
        return {
            "id": cursor.lastrowid,
            "customer_id": customer_id,
            "address_type": address_type,
            "street": street,
            "city": city,
            "state": state,
            "postal_code": postal_code,
            "country": country,
            "is_default": is_default
        }
    finally:
        if close_conn:
            connection.close()


def find_addresses_by_customer_id(customer_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        rows = connection.execute(
            "SELECT id, customer_id, address_type, street, city, state, postal_code, country, is_default FROM customer_addresses WHERE customer_id = ?",
            (customer_id,)
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        if close_conn:
            connection.close()


def find_address_by_id(address_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        row = connection.execute(
            "SELECT id, customer_id, address_type, street, city, state, postal_code, country, is_default FROM customer_addresses WHERE id = ?",
            (address_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        if close_conn:
            connection.close()


def delete_customer_address(address_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute("DELETE FROM customer_addresses WHERE id = ?", (address_id,))
        if close_conn:
            connection.commit()
        return cursor.rowcount > 0
    finally:
        if close_conn:
            connection.close()
