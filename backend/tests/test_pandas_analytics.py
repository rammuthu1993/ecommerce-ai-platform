import os
import unittest

from app.config.settings import settings
from app.database.connection import initialize_database, get_connection
from app.products.service import create_product
from app.categories.service import create_category
from app.inventory.service import get_or_create_inventory
from app.customers.service import create_customer
from app.cart.service import add_to_cart
from app.orders.service import checkout_order
from app.analytics.pandas_analytics import (
    get_sales_by_groupby,
    get_sales_time_series,
    calculate_customer_rfm_segmentation
)


class TestPandasAnalytics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        settings.database = "test_ecommerce.db"
        initialize_database()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("test_ecommerce.db"):
            try:
                os.remove("test_ecommerce.db")
            except OSError:
                pass

    def setUp(self):
        connection = get_connection()
        connection.execute("DELETE FROM order_items")
        connection.execute("DELETE FROM orders")
        connection.execute("DELETE FROM cart_items")
        connection.execute("DELETE FROM carts")
        connection.execute("DELETE FROM inventory_transactions")
        connection.execute("DELETE FROM inventory")
        connection.execute("DELETE FROM customers")
        connection.execute("DELETE FROM products")
        connection.execute("DELETE FROM categories")
        connection.commit()
        connection.close()

    def test_pandas_groupby_and_time_series(self):
        cat = create_category({"name": "Audio"})
        p = create_product({"category_id": cat["id"], "name": "Wireless Speaker", "price": 5000, "quantity": 20})
        get_or_create_inventory(p["id"], initial_stock=20)
        c = create_customer({"first_name": "Grace", "last_name": "Hopper", "email": "grace@example.com"})

        add_to_cart(c["id"], p["id"], 2)
        checkout_order(c["id"])

        # Category GroupBy
        cat_sales = get_sales_by_groupby(groupby_field="category")
        self.assertEqual(len(cat_sales), 1)
        self.assertEqual(cat_sales[0]["category_name"], "Audio")
        self.assertEqual(cat_sales[0]["total_quantity"], 2)

        # Time Series Resampling
        trend = get_sales_time_series(freq="D")
        self.assertGreaterEqual(len(trend), 1)
        self.assertIn("moving_avg_7d", trend[0])

        # RFM Customer Segmentation
        rfm = calculate_customer_rfm_segmentation()
        self.assertEqual(len(rfm), 1)
        self.assertEqual(rfm[0]["customer_name"], "Grace Hopper")
        self.assertIn("segment", rfm[0])
