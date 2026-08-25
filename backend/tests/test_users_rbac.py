import os
import unittest

from app.config.settings import settings
from app.database.connection import initialize_database, get_connection
from app.auth.auth_service import register_user, login_user, change_password
from app.users.service import get_user, get_users, assign_user_role, change_user_status
from app.middleware.auth import require_roles
from app.web.request import Request
from app.core.exceptions import UnauthorizedException, ForbiddenException, AppException


class TestUsersAndRBAC(unittest.TestCase):

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
        connection.execute("DELETE FROM user_roles")
        connection.execute("DELETE FROM users")
        connection.commit()
        connection.close()

    def test_user_registration_and_login(self):
        reg = register_user(username="johndoe", email="john@example.com", password="Password123!")
        self.assertEqual(reg["user"]["email"], "john@example.com")
        self.assertIsNotNone(reg["access_token"])

        login_res = login_user("john@example.com", "Password123!")
        self.assertIsNotNone(login_res["access_token"])

    def test_invalid_login_credentials(self):
        register_user(username="janedoe", email="jane@example.com", password="Password123!")

        with self.assertRaises(UnauthorizedException):
            login_user("jane@example.com", "WrongPassword")

    def test_role_assignment_and_permission_checks(self):
        reg = register_user(username="manager1", email="mgr@example.com", password="Password123!", roles=["MANAGER"])
        user_id = reg["user"]["id"]

        updated = assign_user_role(user_id, "ADMIN")
        self.assertIn("ADMIN", updated["roles"])

        req = Request(method="GET", path="/api/users")
        req.user = {"id": user_id, "email": "mgr@example.com", "roles": updated["roles"]}

        # Should pass because user has ADMIN role
        self.assertTrue(require_roles(req, ["ADMIN"]))

        # Non-admin check
        req_customer = Request(method="GET", path="/api/users")
        req_customer.user = {"id": 99, "email": "cust@example.com", "roles": ["CUSTOMER"]}
        with self.assertRaises(ForbiddenException):
            require_roles(req_customer, ["ADMIN"])
