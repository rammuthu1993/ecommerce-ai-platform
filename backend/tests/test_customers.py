import os
import unittest

from app.config.settings import settings
from app.database.connection import initialize_database, get_connection
from app.customers.service import (
    create_customer,
    get_customer,
    get_customers,
    update_customer_service,
    delete_customer_service,
    add_customer_address,
    get_customer_addresses,
    delete_address_service
)
from app.core.exceptions import CustomerNotFoundException, AddressNotFoundException, AppException


class TestCustomersAndAddresses(unittest.TestCase):

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
        connection.execute("DELETE FROM customer_addresses")
        connection.execute("DELETE FROM customers")
        connection.commit()
        connection.close()

    def test_customer_crud(self):
        c = create_customer({"first_name": "John", "last_name": "Doe", "email": "john@example.com", "phone": "1234567890"})
        self.assertIsNotNone(c["id"])
        self.assertEqual(c["email"], "john@example.com")

        fetched = get_customer(c["id"])
        self.assertEqual(fetched["first_name"], "John")

        updated = update_customer_service(c["id"], {"first_name": "Johnny", "last_name": "Doe", "email": "john@example.com"})
        self.assertEqual(updated["first_name"], "Johnny")

    def test_duplicate_email(self):
        create_customer({"first_name": "User1", "last_name": "Test", "email": "dup@example.com"})
        with self.assertRaises(AppException):
            create_customer({"first_name": "User2", "last_name": "Test", "email": "dup@example.com"})

    def test_customer_addresses(self):
        c = create_customer({"first_name": "Alice", "last_name": "Smith", "email": "alice@example.com"})
        addr = add_customer_address(c["id"], {
            "address_type": "SHIPPING",
            "street": "123 Main St",
            "city": "Springfield",
            "state": "IL",
            "postal_code": "62701",
            "country": "USA",
            "is_default": True
        })

        self.assertIsNotNone(addr["id"])
        self.assertEqual(addr["city"], "Springfield")

        addresses = get_customer_addresses(c["id"])
        self.assertEqual(len(addresses), 1)

        deleted = delete_address_service(addr["id"])
        self.assertTrue(deleted)
        self.assertEqual(len(get_customer_addresses(c["id"])), 0)
