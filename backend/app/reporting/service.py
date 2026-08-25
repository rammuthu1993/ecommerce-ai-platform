from app.reporting.repository import (
    query_sales_summary,
    query_purchase_summary,
    query_inventory_summary,
    query_customer_summary,
    query_product_performance
)

def get_sales_report(start_date=None, end_date=None):
    return query_sales_summary(start_date=start_date, end_date=end_date)

def get_purchase_report(start_date=None, end_date=None):
    return query_purchase_summary(start_date=start_date, end_date=end_date)

def get_inventory_report():
    return query_inventory_summary()

def get_customer_report():
    return query_customer_summary()

def get_top_products_report(limit=10):
    return query_product_performance(limit=limit)
