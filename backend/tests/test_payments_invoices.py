import os
import unittest

from app.config.settings import settings
from app.database.connection import initialize_database, get_connection
from app.products.service import create_product
from app.inventory.service import get_or_create_inventory
from app.customers.service import create_customer
from app.cart.service import add_to_cart
from app.orders.service import checkout_order
from app.discounts.service import create_discount, calculate_discount
from app.payments.service import record_payment, get_payments_for_order
from app.invoices.service import get_invoice_by_order
from app.core.exceptions import AppException


class TestPaymentsInvoicesDiscounts(unittest.TestCase):

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
        connection.execute("DELETE FROM invoices")
        connection.execute("DELETE FROM payments")
        connection.execute("DELETE FROM discounts")
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

    def test_discounts(self):
        disc = create_discount(code="SAVE10", discount_type="PERCENTAGE", value=10, min_purchase=500)
        self.assertEqual(disc["code"], "SAVE10")

        applied = calculate_discount("SAVE10", 1000)
        self.assertEqual(applied, 100.0)

        with self.assertRaises(AppException):
            calculate_discount("SAVE10", 200) # Below min purchase

    def test_payment_and_automatic_invoice_generation(self):
        c = create_customer({"first_name": "Eve", "last_name": "Polastri", "email": "eve@example.com"})
        p = create_product({"name": "Laptop Stand", "price": 2000, "quantity": 10})
        get_or_create_inventory(p["id"], initial_stock=10)

        add_to_cart(c["id"], p["id"], 1)
        order = checkout_order(c["id"])

        result = record_payment(
            order_id=order["id"],
            payment_method="CREDIT_CARD",
            amount=order["total_amount"],
            transaction_reference="TXN123456"
        )

        self.assertEqual(result["payment"]["status"], "COMPLETED")
        self.assertIsNotNone(result["invoice"]["invoice_number"])
        self.assertEqual(result["invoice"]["total"], order["total_amount"])

        # Order status should automatically transition to CONFIRMED
        payments = get_payments_for_order(order["id"])
        self.assertEqual(len(payments), 1)

        inv = get_invoice_by_order(order["id"])
        self.assertEqual(inv["order_id"], order["id"])
