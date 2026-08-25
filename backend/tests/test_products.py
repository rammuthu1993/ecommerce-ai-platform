import unittest
from app.utils.validators import validate_product

class TestProductValidation(unittest.TestCase):
    def test_valid_product(self):
        product = {"name": "dell", "price": 10000, "quantity": 10}
        result = validate_product(product)
        self.assertTrue(result)

    def test_invalid_product_empty_name(self):
        product = {
            "name": "",
            "price": 50000,
            "quantity": 10
        }
        result = validate_product(product)
        self.assertFalse(result)

    def test_negative_price(self):
        product = {
            "name": "Laptop",
            "price": -100,
            "quantity": 10
        }
        result = validate_product(product)
        self.assertFalse(result)

    def test_negative_quantity(self):
        product = {
            "name": "Laptop",
            "price": 50000,
            "quantity": -5
        }
        result = validate_product(product)
        self.assertFalse(result)

    def test_zero_quantity_is_valid(self):
        product = {
            "name": "Laptop",
            "price": 50000,
            "quantity": 0
        }
        result = validate_product(product)
        self.assertTrue(result)