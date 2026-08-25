import unittest
from unittest.mock import patch

from app.products.service import (
    get_products,
    create_product,
    get_product,
    update_product,
    delete_product
)
from app.core.exceptions import ProductNotFoundException


class TestProductService(unittest.TestCase):

    @patch("app.products.service.count_all")
    @patch("app.products.service.find_all")
    def test_get_products(self, mock_find_all, mock_count_all):
        mock_find_all.return_value = [
            {"id": 1, "name": "Laptop", "price": 50000, "quantity": 10}
        ]
        mock_count_all.return_value = 1

        result = get_products()

        self.assertEqual(len(result["products"]), 1)
        self.assertEqual(result["products"][0]["name"], "Laptop")
        self.assertEqual(result["pagination"]["total"], 1)
        mock_find_all.assert_called_once()
        mock_count_all.assert_called_once()

    @patch("app.products.service.save")
    def test_create_product(self, mock_save):
        data = {"name": "Dell Laptop", "price": 50000, "quantity": 10}
        mock_save.return_value = {"id": 1, "name": "Dell Laptop", "price": 50000, "quantity": 10}

        result = create_product(data)

        self.assertEqual(result["id"], 1)
        mock_save.assert_called_once_with({"category_id": None, "name": "Dell Laptop", "price": 50000, "quantity": 10})

    @patch("app.products.service.update")
    @patch("app.products.service.find_by_id")
    def test_update_product(self, mock_find_by_id, mock_update):
        mock_find_by_id.return_value = {"id": 1, "name": "Laptop", "price": 50000, "quantity": 10}
        mock_update.return_value = True

        data = {"name": "Updated Laptop", "price": 60000, "quantity": 5}
        result = update_product(1, data)

        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Updated Laptop")

    @patch("app.products.service.find_by_id")
    def test_update_product_not_found(self, mock_find_by_id):
        mock_find_by_id.return_value = None
        data = {"name": "Updated Laptop", "price": 60000, "quantity": 5}

        with self.assertRaises(ProductNotFoundException):
            update_product(999, data)

    @patch("app.products.service.delete_product_by_id")
    @patch("app.products.service.find_by_id")
    def test_delete_product(self, mock_find_by_id, mock_delete):
        mock_find_by_id.return_value = {"id": 1, "name": "Laptop", "price": 50000, "quantity": 10}
        mock_delete.return_value = True

        result = delete_product(1)
        self.assertTrue(result)

    @patch("app.products.service.find_by_id")
    def test_delete_product_not_found(self, mock_find_by_id):
        mock_find_by_id.return_value = None

        with self.assertRaises(ProductNotFoundException):
            delete_product(999)