import io
import pandas as pd
from app.analytics.pandas_analytics import (
    extract_orders_dataframe,
    extract_order_items_dataframe,
    calculate_customer_rfm_segmentation
)
from app.database.connection import get_connection

def generate_export_dataset(dataset_type="sales", format_type="csv", connection=None):
    dataset_type = str(dataset_type).lower()
    format_type = str(format_type).lower()

    if dataset_type == "sales":
        df = extract_orders_dataframe(connection=connection)
    elif dataset_type == "items":
        df = extract_order_items_dataframe(connection=connection)
    elif dataset_type == "rfm":
        rfm_data = calculate_customer_rfm_segmentation(connection=connection)
        df = pd.DataFrame(rfm_data)
    elif dataset_type == "inventory":
        close_conn = False
        if connection is None:
            connection = get_connection()
            close_conn = True
        try:
            df = pd.read_sql_query(
                """SELECT i.id, p.name AS product_name, i.stock_quantity, i.reserved_quantity,
                          (i.stock_quantity - i.reserved_quantity) AS available_quantity,
                          p.price, (i.stock_quantity * p.price) AS total_valuation, i.location
                   FROM inventory i JOIN products p ON i.product_id = p.id""",
                connection
            )
        finally:
            if close_conn:
                connection.close()
    else:
        df = extract_orders_dataframe(connection=connection)

    if format_type == "json":
        return df.to_json(orient="records", date_format="iso"), "application/json"
    elif format_type == "excel":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name=dataset_type.capitalize())
        output.seek(0)
        return output.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    else:
        # Default CSV
        return df.to_csv(index=False), "text/csv"
