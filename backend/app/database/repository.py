from .connection import get_connection

SORT_FIELDS = {
    "id": "id",
    "name": "name",
    "price": "price",
    "quantity": "quantity"
}

def _build_product_where_clause(search=None, category_id=None, min_price=None, max_price=None, in_stock=None):
    conditions = []
    parameters = []

    if search:
        conditions.append("name LIKE ?")
        parameters.append(f"%{search}%")

    if category_id is not None:
        conditions.append("category_id = ?")
        parameters.append(category_id)

    if min_price is not None:
        conditions.append("price >= ?")
        parameters.append(min_price)

    if max_price is not None:
        conditions.append("price <= ?")
        parameters.append(max_price)

    if in_stock is True:
        conditions.append("quantity > 0")
    elif in_stock is False:
        conditions.append("quantity = 0")

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    return where_clause, parameters


def find_all(
    page=1,
    limit=10,
    search=None,
    sort="id",
    order="asc",
    category_id=None,
    min_price=None,
    max_price=None,
    in_stock=None,
    connection=None
):
    offset = (page - 1) * limit
    sort_column = SORT_FIELDS.get(sort, "id")
    sort_order = "DESC" if str(order).lower() == "desc" else "ASC"

    where_clause, parameters = _build_product_where_clause(
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock
    )

    query = f"""
        SELECT id, category_id, name, price, quantity
        FROM products
        {where_clause}
        ORDER BY {sort_column} {sort_order}
        LIMIT ? OFFSET ?
    """
    parameters.extend([limit, offset])

    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        rows = connection.execute(query, parameters).fetchall()
        return [dict(row) for row in rows]
    finally:
        if close_conn:
            connection.close()


def count_all(
    search=None,
    category_id=None,
    min_price=None,
    max_price=None,
    in_stock=None,
    connection=None
):
    where_clause, parameters = _build_product_where_clause(
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock
    )

    query = f"""
        SELECT COUNT(*) AS total
        FROM products
        {where_clause}
    """

    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        row = connection.execute(query, parameters).fetchone()
        return row["total"] if row else 0
    finally:
        if close_conn:
            connection.close()


def save(product, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    category_id = product.get("category_id")
    try:
        cursor = connection.execute(
            """INSERT INTO products (category_id, name, price, quantity) VALUES (?, ?, ?, ?)""",
            (category_id, product["name"], product["price"], product["quantity"])
        )
        if close_conn:
            connection.commit()
        product_id = cursor.lastrowid
        return {"id": product_id, "category_id": category_id, **product}
    finally:
        if close_conn:
            connection.close()


def find_by_id(product_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        row = connection.execute(
            """SELECT id, category_id, name, price, quantity FROM products WHERE id = ?""",
            (product_id,)
        ).fetchone()
        if row is None:
            return None
        return dict(row)
    finally:
        if close_conn:
            connection.close()


def update(product_id, product, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    category_id = product.get("category_id")
    try:
        cursor = connection.execute(
            """UPDATE products SET category_id = ?, name = ?, price = ?, quantity = ? WHERE id = ?""",
            (category_id, product["name"], product["price"], product["quantity"], product_id)
        )
        if close_conn:
            connection.commit()
        return cursor.rowcount > 0
    finally:
        if close_conn:
            connection.close()


def delete_product_by_id(product_id, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        cursor = connection.execute(
            """DELETE FROM products WHERE id = ?""",
            (product_id,)
        )
        if close_conn:
            connection.commit()
        return cursor.rowcount > 0
    finally:
        if close_conn:
            connection.close()