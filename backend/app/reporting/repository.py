from app.database.connection import get_connection

def query_sales_summary(start_date=None, end_date=None, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    query = """
        SELECT COUNT(id) AS total_orders,
               COALESCE(SUM(total_amount), 0.0) AS total_revenue,
               COALESCE(AVG(total_amount), 0.0) AS average_order_value,
               SUM(CASE WHEN status = 'DELIVERED' THEN total_amount ELSE 0.0 END) AS delivered_revenue
        FROM orders
        WHERE status != 'CANCELLED'
    """
    params = []
    if start_date:
        query += " AND created_at >= ?"
        params.append(start_date)
    if end_date:
        query += " AND created_at <= ?"
        params.append(end_date)

    try:
        row = connection.execute(query, params).fetchone()
        return dict(row) if row else {}
    finally:
        if close_conn:
            connection.close()


def query_purchase_summary(start_date=None, end_date=None, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    query = """
        SELECT COUNT(id) AS total_purchases,
               COALESCE(SUM(total_amount), 0.0) AS total_spend
        FROM purchases
        WHERE status != 'CANCELLED'
    """
    params = []
    if start_date:
        query += " AND created_at >= ?"
        params.append(start_date)
    if end_date:
        query += " AND created_at <= ?"
        params.append(end_date)

    try:
        row = connection.execute(query, params).fetchone()
        return dict(row) if row else {}
    finally:
        if close_conn:
            connection.close()


def query_inventory_summary(connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        row = connection.execute(
            """SELECT COUNT(p.id) AS total_products,
                      COALESCE(SUM(i.stock_quantity), 0) AS total_stock,
                      COALESCE(SUM(i.stock_quantity * p.price), 0.0) AS inventory_valuation,
                      SUM(CASE WHEN (i.stock_quantity - i.reserved_quantity) <= 5 AND (i.stock_quantity - i.reserved_quantity) > 0 THEN 1 ELSE 0 END) AS low_stock_count,
                      SUM(CASE WHEN (i.stock_quantity - i.reserved_quantity) <= 0 THEN 1 ELSE 0 END) AS out_of_stock_count
               FROM products p
               LEFT JOIN inventory i ON p.id = i.product_id"""
        ).fetchone()
        return dict(row) if row else {}
    finally:
        if close_conn:
            connection.close()


def query_customer_summary(connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        row = connection.execute(
            """SELECT COUNT(c.id) AS total_customers,
                      COUNT(DISTINCT o.customer_id) AS active_purchasers
               FROM customers c
               LEFT JOIN orders o ON c.id = o.customer_id"""
        ).fetchone()
        return dict(row) if row else {}
    finally:
        if close_conn:
            connection.close()


def query_product_performance(limit=10, connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        rows = connection.execute(
            """SELECT p.id, p.name, COALESCE(SUM(oi.quantity), 0) AS units_sold,
                      COALESCE(SUM(oi.quantity * oi.unit_price), 0.0) AS total_revenue
               FROM products p
               LEFT JOIN order_items oi ON p.id = oi.product_id
               LEFT JOIN orders o ON oi.order_id = o.id AND o.status != 'CANCELLED'
               GROUP BY p.id, p.name
               ORDER BY total_revenue DESC, units_sold DESC
               LIMIT ?""",
            (limit,)
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        if close_conn:
            connection.close()
