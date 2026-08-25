import pandas as pd
import numpy as np
from app.database.connection import get_connection

def extract_orders_dataframe(connection=None) -> pd.DataFrame:
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        query = """
            SELECT o.id AS order_id, o.order_number, o.customer_id,
                   c.first_name || ' ' || c.last_name AS customer_name,
                   c.email AS customer_email,
                   o.status, o.subtotal, o.tax_amount, o.discount_amount, o.total_amount,
                   o.created_at
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
        """
        conn = getattr(connection, "raw_conn", connection)
        df = pd.read_sql_query(query, conn)
        if df.empty:
            return pd.DataFrame(columns=[
                "order_id", "order_number", "customer_id", "customer_name",
                "customer_email", "status", "subtotal", "tax_amount", "discount_amount",
                "total_amount", "created_at"
            ])

        # Clean dates & types
        df["created_at"] = pd.to_datetime(df["created_at"])
        df["total_amount"] = df["total_amount"].astype(float)
        df["subtotal"] = df["subtotal"].astype(float)
        return df
    finally:
        if close_conn:
            connection.close()


def extract_order_items_dataframe(connection=None) -> pd.DataFrame:
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        query = """
            SELECT oi.id AS item_id, oi.order_id, oi.product_id, p.name AS product_name,
                   cat.name AS category_name, oi.quantity, oi.unit_price,
                   (oi.quantity * oi.unit_price) AS line_total, o.created_at
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            LEFT JOIN categories cat ON p.category_id = cat.id
            JOIN orders o ON oi.order_id = o.id
            WHERE o.status != 'CANCELLED'
        """
        conn = getattr(connection, "raw_conn", connection)
        df = pd.read_sql_query(query, conn)
        if df.empty:
            return pd.DataFrame(columns=[
                "item_id", "order_id", "product_id", "product_name",
                "category_name", "quantity", "unit_price", "line_total", "created_at"
            ])

        df["created_at"] = pd.to_datetime(df["created_at"])
        df["line_total"] = df["line_total"].astype(float)
        df["quantity"] = df["quantity"].astype(int)
        df["category_name"] = df["category_name"].fillna("Uncategorized")
        return df
    finally:
        if close_conn:
            connection.close()


def get_sales_by_groupby(groupby_field="category", connection=None) -> list:
    df = extract_order_items_dataframe(connection=connection)
    if df.empty:
        return []

    if groupby_field == "category":
        group_col = "category_name"
    elif groupby_field == "product":
        group_col = "product_name"
    else:
        group_col = "category_name"

    grouped = df.groupby(group_col).agg(
        total_quantity=("quantity", "sum"),
        total_revenue=("line_total", "sum"),
        average_price=("unit_price", "mean"),
        order_count=("order_id", "nunique")
    ).reset_index()

    grouped["total_revenue"] = grouped["total_revenue"].round(2)
    grouped["average_price"] = grouped["average_price"].round(2)
    grouped = grouped.sort_values(by="total_revenue", ascending=False)
    return grouped.to_dict(orient="records")


def get_sales_time_series(freq="D", connection=None) -> list:
    """
    freq can be 'D' (Daily), 'ME' or 'M' (Monthly), 'YE' or 'Y' (Yearly)
    """
    df = extract_orders_dataframe(connection=connection)
    if df.empty:
        return []

    # Filter out cancelled orders
    df = df[df["status"] != "CANCELLED"].copy()
    df.set_index("created_at", inplace=True)

    # Resample
    resampled = df.resample(freq).agg(
        total_revenue=("total_amount", "sum"),
        total_orders=("order_id", "count"),
        average_order_value=("total_amount", "mean")
    ).reset_index()

    resampled["total_revenue"] = resampled["total_revenue"].fillna(0.0).round(2)
    resampled["average_order_value"] = resampled["average_order_value"].fillna(0.0).round(2)
    resampled["total_orders"] = resampled["total_orders"].fillna(0).astype(int)

    # Add 7-period moving average for daily frequency
    if freq == "D":
        resampled["moving_avg_7d"] = resampled["total_revenue"].rolling(window=7, min_periods=1).mean().round(2)

    resampled["created_at"] = resampled["created_at"].dt.strftime("%Y-%m-%d")
    return resampled.to_dict(orient="records")


def calculate_customer_rfm_segmentation(connection=None) -> list:
    """
    Calculates Recency, Frequency, Monetary (RFM) Segmentation for Customers.
    """
    df = extract_orders_dataframe(connection=connection)
    if df.empty:
        return []

    df = df[df["status"] != "CANCELLED"].copy()
    if df.empty:
        return []

    now = df["created_at"].max() + pd.Timedelta(days=1)

    rfm = df.groupby(["customer_id", "customer_name", "customer_email"]).agg(
        recency_days=("created_at", lambda x: (now - x.max()).days),
        frequency=("order_id", "count"),
        monetary_value=("total_amount", "sum")
    ).reset_index()

    rfm["monetary_value"] = rfm["monetary_value"].round(2)

    # Segment classification rules
    def classify_rfm(row):
        m = row["monetary_value"]
        f = row["frequency"]
        r = row["recency_days"]

        if m >= 50000 or f >= 5:
            return "VIP Customer"
        elif f > 1 and r <= 30:
            return "Loyal Customer"
        elif r > 60:
            return "At-Risk Customer"
        else:
            return "Standard Customer"

    rfm["segment"] = rfm.apply(classify_rfm, axis=1)
    return rfm.to_dict(orient="records")
