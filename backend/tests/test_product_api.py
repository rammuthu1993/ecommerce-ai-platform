import os
import unittest

from app.config.settings import settings
from app.database.connection import initialize_database, get_connection
from app.web.request import Request
from app.web.server import (
    products_handler,
    create_product_handler,
    get_product_handler,
    update_product_handler,
    delete_product_handler
)
from app.core.exceptions import (
    InvalidProductException,
    ProductNotFoundException,
    InvalidPaginationException,
    InvalidSortingException,
    InvalidJsonException
)


class TestProductAPI(unittest.TestCase):

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

    def test_post_product(self):
        req = Request(method="POST", path="/api/products", body='{"name": "Gaming Laptop", "price": 80000, "quantity": 5}')
        resp = create_product_handler(req)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.body["data"]["name"], "Gaming Laptop")

    def test_post_product_invalid_data(self):
        req = Request(method="POST", path="/api/products", body='{"name": "", "price": -50, "quantity": 0}')
        with self.assertRaises(InvalidProductException):
            create_product_handler(req)

    def test_post_product_invalid_json(self):
        req = Request(method="POST", path="/api/products", body='{invalid json}')
        with self.assertRaises(InvalidJsonException):
            create_product_handler(req)

    def test_get_product_collection_and_single(self):
        # Create product via API handler
        post_req = Request(method="POST", path="/api/products", body='{"name": "Mechanical Keyboard", "price": 4000, "quantity": 20}')
        created_resp = create_product_handler(post_req)
        prod_id = created_resp.body["data"]["id"]

        # GET single
        get_req = Request(method="GET", path=f"/api/products/{prod_id}", params={"id": str(prod_id)})
        get_resp = get_product_handler(get_req)
        self.assertEqual(get_resp.status_code, 200)
        self.assertEqual(get_resp.body["data"]["name"], "Mechanical Keyboard")

        # GET collection
        col_req = Request(method="GET", path="/api/products?page=1&limit=10")
        col_resp = products_handler(col_req)
        self.assertEqual(col_resp.status_code, 200)
        self.assertEqual(len(col_resp.body["data"]), 1)

    def test_get_single_not_found(self):
        req = Request(method="GET", path="/api/products/9999", params={"id": "9999"})
        with self.assertRaises(ProductNotFoundException):
            get_product_handler(req)

    def test_put_product(self):
        post_req = Request(method="POST", path="/api/products", body='{"name": "Old Name", "price": 100, "quantity": 1}')
        created = create_product_handler(post_req)
        prod_id = created.body["data"]["id"]

        put_req = Request(method="PUT", path=f"/api/products/{prod_id}", params={"id": str(prod_id)}, body='{"name": "New Name", "price": 150, "quantity": 2}')
        put_resp = update_product_handler(put_req)
        self.assertEqual(put_resp.status_code, 200)
        self.assertEqual(put_resp.body["data"]["name"], "New Name")

    def test_delete_product(self):
        post_req = Request(method="POST", path="/api/products", body='{"name": "To Delete", "price": 50, "quantity": 1}')
        created = create_product_handler(post_req)
        prod_id = created.body["data"]["id"]

        del_req = Request(method="DELETE", path=f"/api/products/{prod_id}", params={"id": str(prod_id)})
        del_resp = delete_product_handler(del_req)
        self.assertEqual(del_resp.status_code, 200)

    def test_invalid_pagination(self):
        req = Request(method="GET", path="/api/products?page=0&limit=10")
        with self.assertRaises(InvalidPaginationException):
            products_handler(req)

    def test_invalid_sorting(self):
        req = Request(method="GET", path="/api/products?sort=invalid_col&order=asc")
        with self.assertRaises(InvalidSortingException):
            products_handler(req)
