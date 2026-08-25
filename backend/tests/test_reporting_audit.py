import os
import unittest

from app.config.settings import settings
from app.database.connection import initialize_database, get_connection
from app.products.service import create_product
from app.inventory.service import get_or_create_inventory
from app.customers.service import create_customer
from app.cart.service import add_to_cart
from app.orders.service import checkout_order
from app.audit.service import log_audit, get_audit_trail
from app.reporting.service import (
    get_sales_report,
    get_inventory_report,
    get_customer_report,
    get_top_products_report
)


class TestReportingAndAudit(unittest.TestCase):

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
        connection.execute("DELETE FROM audit_logs")
        connection.execute("DELETE FROM order_items")
        connection.execute("DELETE FROM orders")
        connection.execute("DELETE FROM cart_items")
        connection.execute("DELETE FROM carts")
        connection.execute("DELETE FROM inventory_transactions")
        connection.execute("DELETE FROM inventory")
        connection.execute("DELETE FROM customers")
        connection.execute("DELETE FROM products")
        connection.commit()
        connection.close()

    def test_audit_logging(self):
        log_id = log_audit(action="CREATE", module="PRODUCTS", entity="PRODUCT", entity_id=1, details="Created product Dell Laptop")
        self.assertIsNotNone(log_id)

        logs = get_audit_trail(module="PRODUCTS")
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["action"], "CREATE")

    def test_reporting_foundation(self):
        c = create_customer({"first_name": "Frank", "last_name": "Ocean", "email": "frank@example.com"})
        p1 = create_product({"name": "Camera", "price": 50000, "quantity": 10})
        get_or_create_inventory(p1["id"], initial_stock=10)

        add_to_cart(c["id"], p1["id"], 2)
        checkout_order(c["id"])

        sales_report = get_sales_report()
        self.assertEqual(sales_report["total_orders"], 1)
        self.assertGreater(sales_report["total_revenue"], 100000.0)

        inv_report = get_inventory_report()
        self.assertEqual(inv_report["total_products"], 1)
        self.assertEqual(inv_report["total_stock"], 10)

        cust_report = get_customer_report()
        self.assertEqual(cust_report["total_customers"], 1)
        self.assertEqual(cust_report["active_purchasers"], 1)

        top_products = get_top_products_report(limit=5)
        self.assertEqual(len(top_products), 1)
        self.assertEqual(top_products[0]["name"], "Camera")
        self.assertEqual(top_products[0]["units_sold"], 2)
