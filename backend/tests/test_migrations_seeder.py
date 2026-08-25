import os
import unittest

from app.config.settings import settings
from app.database.connection import initialize_database, get_connection
from app.database.migrations.runner import migration_runner
from app.database.seed import seed_database
from app.users.repository import find_user_by_email


class TestMigrationsAndSeeder(unittest.TestCase):

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

    def test_migration_runner(self):
        migrations = [
            (1, "create_test_table", "CREATE TABLE IF NOT EXISTS migration_test (id INTEGER PRIMARY KEY);")
        ]
        migration_runner.run_migrations(migrations)

        conn = get_connection()
        applied = conn.execute("SELECT name FROM schema_migrations WHERE version = 1").fetchone()
        conn.close()
        self.assertIsNotNone(applied)
        self.assertEqual(applied["name"], "create_test_table")

    def test_database_seeder(self):
        seed_database()
        conn = get_connection()
        admin = find_user_by_email("admin@ecommerce.ai", connection=conn)
        conn.close()

        self.assertIsNotNone(admin)
        self.assertEqual(admin["username"], "admin")
        self.assertIn("ADMIN", admin["roles"])
