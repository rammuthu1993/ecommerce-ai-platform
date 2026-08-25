import os
import unittest

from app.config.settings import settings
from app.database.connection import initialize_database, get_connection
from app.categories.service import (
    create_category,
    get_categories,
    get_category,
    update_category_service,
    delete_category_service
)
from app.products.service import create_product, get_products
from app.core.exceptions import CategoryNotFoundException, AppException


class TestCategoryModule(unittest.TestCase):

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
        connection.execute("DELETE FROM categories")
        connection.commit()
        connection.close()

    def test_create_and_get_category(self):
        cat = create_category({"name": "Electronics", "description": "Gadgets"})
        self.assertIsNotNone(cat["id"])
        self.assertEqual(cat["name"], "Electronics")

        fetched = get_category(cat["id"])
        self.assertEqual(fetched["name"], "Electronics")

    def test_category_not_found(self):
        with self.assertRaises(CategoryNotFoundException):
            get_category(99999)

    def test_invalid_category(self):
        with self.assertRaises(AppException):
            create_category({"name": "   "})

    def test_update_and_delete_category(self):
        cat = create_category({"name": "Books", "description": "Novels"})
        updated = update_category_service(cat["id"], {"name": "Textbooks", "description": "Educational"})
        self.assertEqual(updated["name"], "Textbooks")

        deleted = delete_category_service(cat["id"])
        self.assertTrue(deleted)
        with self.assertRaises(CategoryNotFoundException):
            get_category(cat["id"])

    def test_product_category_relationship(self):
        cat = create_category({"name": "Computers"})
        prod = create_product({
            "category_id": cat["id"],
            "name": "MacBook Pro",
            "price": 150000,
            "quantity": 5
        })

        self.assertEqual(prod["category_id"], cat["id"])

        filtered = get_products(category_id=cat["id"])
        self.assertEqual(len(filtered["products"]), 1)
        self.assertEqual(filtered["products"][0]["name"], "MacBook Pro")
