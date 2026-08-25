from app.database.connection import get_connection
from app.users.repository import find_user_by_email, save_user, assign_role_to_user
from app.auth.password_hasher import hash_password
from app.categories.repository import save_category, find_category_by_name
from app.database.repository import save as save_product, find_all as find_all_products
from app.inventory.service import get_or_create_inventory

def seed_database(connection=None):
    close_conn = False
    if connection is None:
        connection = get_connection()
        close_conn = True

    try:
        # Seed Roles & Permissions
        roles = [("ADMIN", "System Administrator"), ("MANAGER", "Store Manager"), ("CUSTOMER", "Registered Customer")]
        for r_name, r_desc in roles:
            connection.execute("INSERT OR IGNORE INTO roles (name, description) VALUES (?, ?)", (r_name, r_desc))

        permissions = [
            ("manage_users", "Manage User Accounts"),
            ("manage_catalog", "Manage Categories & Products"),
            ("manage_inventory", "Manage Stock Adjustments"),
            ("manage_orders", "Manage Customer Orders"),
            ("view_reports", "Access System Reports")
        ]
        for p_name, p_desc in permissions:
            connection.execute("INSERT OR IGNORE INTO permissions (name, description) VALUES (?, ?)", (p_name, p_desc))

        # Seed Default Admin Account
        admin_email = "admin@ecommerce.ai"
        if not find_user_by_email(admin_email, connection=connection):
            hash_hex, salt_hex = hash_password("AdminPass123!")
            admin_user = save_user(
                username="admin",
                email=admin_email,
                password_hash=hash_hex,
                salt=salt_hex,
                status="ACTIVE",
                connection=connection
            )
            assign_role_to_user(admin_user["id"], "ADMIN", connection=connection)

        # Seed Default Category & Product if empty
        cat = find_category_by_name("Electronics", connection=connection)
        if not cat:
            cat = save_category("Electronics", "Tech gadgets and hardware", connection=connection)

        prods = find_all_products(connection=connection)
        if not prods:
            prod = save_product({
                "category_id": cat["id"],
                "name": "Demo Pro Laptop",
                "price": 99999.0,
                "quantity": 10
            }, connection=connection)
            get_or_create_inventory(prod["id"], initial_stock=10, location="Warehouse A", connection=connection)

        if close_conn:
            connection.commit()

    finally:
        if close_conn:
            connection.close()
