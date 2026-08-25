import os
import unittest

from app.config.settings import settings
from app.database.connection import initialize_database, get_connection
from app.products.service import create_product
from app.inventory.service import get_or_create_inventory
from app.suppliers.service import (
    create_supplier,
    get_supplier,
    get_suppliers,
    update_supplier_service,
    delete_supplier_service
)
from app.purchases.service import (
    create_purchase,
    get_purchase,
    receive_purchase
)
from app.core.exceptions import SupplierNotFoundException, AppException


class TestSuppliersAndPurchases(unittest.TestCase):

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
        connection.execute("DELETE FROM purchase_items")
        connection.execute("DELETE FROM purchases")
        connection.execute("DELETE FROM suppliers")
        connection.execute("DELETE FROM products")
        connection.commit()
        connection.close()

    def test_supplier_crud(self):
        sup = create_supplier({"name": "Acme Corp", "contact_email": "acme@example.com", "phone": "1234567890"})
        self.assertIsNotNone(sup["id"])
        self.assertEqual(sup["name"], "Acme Corp")

        fetched = get_supplier(sup["id"])
        self.assertEqual(fetched["contact_email"], "acme@example.com")

        updated = update_supplier_service(sup["id"], {"name": "Acme Corp Global"})
        self.assertEqual(updated["name"], "Acme Corp Global")

    def test_purchase_creation_and_receiving(self):
        sup = create_supplier({"name": "Tech Supplier"})
        prod = create_product({"name": "RAM Chip", "price": 4000, "quantity": 10})
        get_or_create_inventory(prod["id"], initial_stock=10)

        po = create_purchase(
            supplier_id=sup["id"],
            items=[{"product_id": prod["id"], "quantity": 50, "unit_cost": 2500}]
        )
        self.assertEqual(po["status"], "DRAFT")
        self.assertEqual(po["total_amount"], 125000.0)

        # Receive purchase order -> triggers inventory STOCK_IN
        received = receive_purchase(po["id"])
        self.assertEqual(received["status"], "RECEIVED")

        inv = get_or_create_inventory(prod["id"])
        self.assertEqual(inv["stock_quantity"], 60) # 10 initial + 50 received
