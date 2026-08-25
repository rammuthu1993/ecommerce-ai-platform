import os
import unittest

from app.config.settings import settings
from app.database.connection import initialize_database, get_connection
from app.products.service import create_product
from app.inventory.service import (
    get_or_create_inventory,
    adjust_stock,
    reserve_stock,
    release_stock,
    get_low_stock,
    get_out_of_stock,
    get_transaction_history
)
from app.core.exceptions import InsufficientStockException


class TestInventoryModule(unittest.TestCase):

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
        connection.execute("DELETE FROM inventory_transactions")
        connection.execute("DELETE FROM inventory")
        connection.execute("DELETE FROM products")
        connection.commit()
        connection.close()

    def test_inventory_creation_and_adjustment(self):
        prod = create_product({"name": "Keyboard", "price": 2000, "quantity": 10})
        inv = get_or_create_inventory(prod["id"], initial_stock=10)
        self.assertEqual(inv["stock_quantity"], 10)
        self.assertEqual(inv["available_quantity"], 10)

        # Stock-in (increase by 5)
        updated = adjust_stock(prod["id"], 5, tx_type="STOCK_IN")
        self.assertEqual(updated["stock_quantity"], 15)
        self.assertEqual(updated["available_quantity"], 15)

        # Stock-out (decrease by 3)
        updated = adjust_stock(prod["id"], -3, tx_type="STOCK_OUT")
        self.assertEqual(updated["stock_quantity"], 12)

    def test_stock_reservation_and_release(self):
        prod = create_product({"name": "Mouse", "price": 1000, "quantity": 5})
        get_or_create_inventory(prod["id"], initial_stock=5)

        res = reserve_stock(prod["id"], 2, reference_type="ORDER", reference_id=101)
        self.assertTrue(res)

        inv = get_or_create_inventory(prod["id"])
        self.assertEqual(inv["stock_quantity"], 5)
        self.assertEqual(inv["reserved_quantity"], 2)
        self.assertEqual(inv["available_quantity"], 3)

        # Attempt to reserve more than available
        with self.assertRaises(InsufficientStockException):
            reserve_stock(prod["id"], 10)

        # Release stock
        release_stock(prod["id"], 2)
        inv = get_or_create_inventory(prod["id"])
        self.assertEqual(inv["reserved_quantity"], 0)
        self.assertEqual(inv["available_quantity"], 5)

    def test_low_stock_and_out_of_stock_alerts(self):
        p1 = create_product({"name": "P1", "price": 100, "quantity": 3})
        p2 = create_product({"name": "P2", "price": 100, "quantity": 0})
        p3 = create_product({"name": "P3", "price": 100, "quantity": 50})

        get_or_create_inventory(p1["id"], initial_stock=3)
        get_or_create_inventory(p2["id"], initial_stock=0)
        get_or_create_inventory(p3["id"], initial_stock=50)

        low = get_low_stock(threshold=5)
        self.assertEqual(len(low), 1)
        self.assertEqual(low[0]["product_id"], p1["id"])

        out = get_out_of_stock()
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["product_id"], p2["id"])

    def test_transaction_history(self):
        prod = create_product({"name": "Headphones", "price": 5000, "quantity": 20})
        get_or_create_inventory(prod["id"], initial_stock=20)
        adjust_stock(prod["id"], 10, tx_type="STOCK_IN")
        adjust_stock(prod["id"], -5, tx_type="STOCK_OUT")

        history = get_transaction_history(prod["id"])
        self.assertGreaterEqual(len(history), 2)
