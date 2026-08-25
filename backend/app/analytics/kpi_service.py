import pandas as pd
from app.analytics.pandas_analytics import extract_orders_dataframe, extract_order_items_dataframe
from app.database.connection import get_connection

def get_executive_kpis(connection=None) -> dict:
    orders_df = extract_orders_dataframe(connection=connection)
    items_df = extract_order_items_dataframe(connection=connection)

    if orders_df.empty:
        return {
            "total_revenue": 0.0,
            "gross_profit": 0.0,
            "gross_margin_percentage": 0.0,
            "total_orders": 0,
            "average_order_value": 0.0,
            "total_units_sold": 0,
            "active_customers": 0,
            "customer_lifetime_value": 0.0,
            "inventory_valuation": 0.0
        }

    valid_orders = orders_df[orders_df["status"] != "CANCELLED"]

    total_revenue = float(valid_orders["total_amount"].sum())
    total_orders = int(len(valid_orders))
    aov = float(valid_orders["total_amount"].mean()) if total_orders > 0 else 0.0
    units_sold = int(items_df["quantity"].sum()) if not items_df.empty else 0

    # Customer Lifetime Value (CLV)
    unique_customers = int(valid_orders["customer_id"].nunique())
    clv = (total_revenue / unique_customers) if unique_customers > 0 else 0.0

    # Estimate COGS & Inventory Valuation from DB
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        inv_row = connection.execute(
            """SELECT COALESCE(SUM(i.stock_quantity * p.price), 0.0) AS valuation
               FROM products p JOIN inventory i ON p.id = i.product_id"""
        ).fetchone()
        inventory_val = float(inv_row["valuation"]) if inv_row else 0.0
    finally:
        if close_conn:
            connection.close()

    # Estimate Gross Profit at 35% margin for demo baseline
    gross_profit = total_revenue * 0.35
    gross_margin = 35.0 if total_revenue > 0 else 0.0

    return {
        "total_revenue": round(total_revenue, 2),
        "gross_profit": round(gross_profit, 2),
        "gross_margin_percentage": round(gross_margin, 2),
        "total_orders": total_orders,
        "average_order_value": round(aov, 2),
        "total_units_sold": units_sold,
        "active_customers": unique_customers,
        "customer_lifetime_value": round(clv, 2),
        "inventory_valuation": round(inventory_val, 2)
    }
