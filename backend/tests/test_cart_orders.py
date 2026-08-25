import os
import unittest

from app.config.settings import settings
from app.database.connection import initialize_database, get_connection
from app.products.service import create_product
from app.inventory.service import get_or_create_inventory
from app.customers.service import create_customer
from app.cart.service import add_to_cart, get_customer_cart, update_cart_item, remove_from_cart
from app.orders.service import checkout_order, get_order, update_order_status_service
from app.core.exceptions import InvalidOrderTransitionException, InsufficientStockException, AppException


class TestCartAndOrders(unittest.TestCase):

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
        connection.commit()
        connection.close()

    def test_cart_operations(self):
        c = create_customer({"first_name": "Bob", "last_name": "Martin", "email": "bob@example.com"})
        p = create_product({"name": "Headphones", "price": 3000, "quantity": 15})
        get_or_create_inventory(p["id"], initial_stock=15)

        cart = add_to_cart(c["id"], p["id"], 2)
        self.assertEqual(len(cart["items"]), 1)
        self.assertEqual(cart["total_amount"], 6000.0)

        # Update cart item quantity
        cart = update_cart_item(c["id"], p["id"], 5)
        self.assertEqual(cart["items"][0]["quantity"], 5)
        self.assertEqual(cart["total_amount"], 15000.0)

        # Remove from cart
        cart = remove_from_cart(c["id"], p["id"])
        self.assertEqual(len(cart["items"]), 0)

    def test_checkout_and_stock_reservation(self):
        c = create_customer({"first_name": "Carol", "last_name": "Danvers", "email": "carol@example.com"})
        p = create_product({"name": "Smart Watch", "price": 10000, "quantity": 8})
        get_or_create_inventory(p["id"], initial_stock=8)

        add_to_cart(c["id"], p["id"], 3)
        order = checkout_order(c["id"])

        self.assertEqual(order["status"], "PENDING")
        self.assertEqual(order["subtotal"], 30000.0)
        self.assertGreater(order["total_amount"], 30000.0) # subtotal + tax

        # Verify stock reservation
        inv = get_or_create_inventory(p["id"])
        self.assertEqual(inv["reserved_quantity"], 3)
        self.assertEqual(inv["available_quantity"], 5)

        # Verify cart was cleared after checkout
        cart = get_customer_cart(c["id"])
        self.assertEqual(len(cart["items"]), 0)

    def test_order_lifecycle_and_cancellation(self):
        c = create_customer({"first_name": "Dave", "last_name": "Grohl", "email": "dave@example.com"})
        p = create_product({"name": "Guitar", "price": 45000, "quantity": 4})
        get_or_create_inventory(p["id"], initial_stock=4)

        add_to_cart(c["id"], p["id"], 2)
        order = checkout_order(c["id"])

        # PENDING -> CONFIRMED
        confirmed = update_order_status_service(order["id"], "CONFIRMED")
        self.assertEqual(confirmed["status"], "CONFIRMED")

        # Invalid transition: CONFIRMED -> DELIVERED (must go through PROCESSING, SHIPPED first)
        with self.assertRaises(InvalidOrderTransitionException):
            update_order_status_service(order["id"], "DELIVERED")

        # Cancel order -> restores reserved stock
        cancelled = update_order_status_service(order["id"], "CANCELLED")
        self.assertEqual(cancelled["status"], "CANCELLED")

        inv = get_or_create_inventory(p["id"])
        self.assertEqual(inv["reserved_quantity"], 0)
        self.assertEqual(inv["available_quantity"], 4)
