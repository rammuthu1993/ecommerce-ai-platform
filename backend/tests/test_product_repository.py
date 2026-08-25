import os
import unittest

from app.config.settings import settings
from app.database.connection import initialize_database, get_connection
from app.database.repository import (
    find_all,
    find_by_id,
    save,
    update,
    delete_product_by_id,
    count_all
)


class TestProductRepository(unittest.TestCase):

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
        connection.execute("DELETE FROM products")
        connection.commit()
        connection.close()

    def test_save_product(self):
        product = {
            "name": "Dell Laptop",
            "price": 50000,
            "quantity": 10
        }
        result = save(product)
        self.assertIsNotNone(result["id"])
        self.assertEqual(result["name"], "Dell Laptop")
        self.assertEqual(result["price"], 50000)
        self.assertEqual(result["quantity"], 10)

    def test_find_all(self):
        save({"name": "Laptop", "price": 50000, "quantity": 10})
        save({"name": "Mouse", "price": 1000, "quantity": 20})
        products = find_all()
        self.assertEqual(len(products), 2)

    def test_find_by_id(self):
        product = save({"name": "Keyboard", "price": 2000, "quantity": 15})
        result = find_by_id(product["id"])
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Keyboard")

    def test_find_by_id_not_found(self):
        result = find_by_id(999999)
        self.assertIsNone(result)

    def test_update_product(self):
        product = save({"name": "Monitor", "price": 15000, "quantity": 5})
        updated = update(product["id"], {"name": "4K Monitor", "price": 25000, "quantity": 3})
        self.assertTrue(updated)

        fetched = find_by_id(product["id"])
        self.assertEqual(fetched["name"], "4K Monitor")
        self.assertEqual(fetched["price"], 25000)

    def test_delete_product(self):
        product = save({"name": "Headphones", "price": 3000, "quantity": 8})
        deleted = delete_product_by_id(product["id"])
        self.assertTrue(deleted)
        self.assertIsNone(find_by_id(product["id"]))

    def test_find_all_with_search(self):
        save({"name": "Dell Laptop", "price": 50000, "quantity": 10})
        save({"name": "Wireless Mouse", "price": 1000, "quantity": 20})
        result = find_all(page=1, limit=10, search="Laptop")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Dell Laptop")

    def test_count_all_with_search(self):
        save({"name": "Dell Laptop", "price": 50000, "quantity": 10})
        save({"name": "HP Laptop", "price": 45000, "quantity": 5})
        save({"name": "Mouse", "price": 1000, "quantity": 20})

        total = count_all(search="Laptop")
        self.assertEqual(total, 2)

    def test_sorting(self):
        save({"name": "Cheap Item", "price": 10, "quantity": 100})
        save({"name": "Expensive Item", "price": 1000, "quantity": 1})

        asc_result = find_all(sort="price", order="asc")
        self.assertLessEqual(asc_result[0]["price"], asc_result[1]["price"])

        desc_result = find_all(sort="price", order="desc")
        self.assertGreaterEqual(desc_result[0]["price"], desc_result[1]["price"])