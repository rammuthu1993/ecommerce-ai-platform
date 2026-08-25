from app.web.response import Response

def get_api_documentation():
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "E-Commerce AI Platform API",
            "version": "2.0.0",
            "description": "Production REST API for E-Commerce AI Platform supporting Authentication, RBAC, Catalog, Inventory, Cart, Orders, Payments, Invoices, Reporting, and Audit Logs."
        },
        "endpoints": {
            "Health & Docs": [
                {"method": "GET", "path": "/health", "description": "System health and database check"},
                {"method": "GET", "path": "/api/docs", "description": "OpenAPI API documentation"}
            ],
            "Authentication": [
                {"method": "POST", "path": "/api/auth/register", "description": "Register new user account"},
                {"method": "POST", "path": "/api/auth/login", "description": "User login & JWT token retrieval"},
                {"method": "GET", "path": "/api/auth/me", "description": "Get current user profile (Protected)"},
                {"method": "PUT", "path": "/api/auth/password", "description": "Update user password (Protected)"}
            ],
            "User Management & RBAC": [
                {"method": "GET", "path": "/api/users", "description": "List users (Admin)"},
                {"method": "GET", "path": "/api/users/{id}", "description": "Get user details (Admin)"},
                {"method": "PUT", "path": "/api/users/{id}/status", "description": "Update user status (Admin)"},
                {"method": "POST", "path": "/api/users/{id}/roles", "description": "Assign role to user (Admin)"}
            ],
            "Products & Categories": [
                {"method": "GET", "path": "/api/products", "description": "List & search products with multi-filter"},
                {"method": "POST", "path": "/api/products", "description": "Create product (Admin/Manager)"},
                {"method": "GET", "path": "/api/products/{id}", "description": "Get product details"},
                {"method": "PUT", "path": "/api/products/{id}", "description": "Update product (Admin/Manager)"},
                {"method": "DELETE", "path": "/api/products/{id}", "description": "Delete product (Admin)"},
                {"method": "GET", "path": "/api/categories", "description": "List categories"},
                {"method": "POST", "path": "/api/categories", "description": "Create category (Admin/Manager)"}
            ],
            "Inventory & Purchases": [
                {"method": "GET", "path": "/api/inventory", "description": "Get stock levels"},
                {"method": "POST", "path": "/api/inventory/adjust", "description": "Stock adjustment (Admin/Manager)"},
                {"method": "GET", "path": "/api/inventory/low-stock", "description": "Low-stock alert products"},
                {"method": "GET", "path": "/api/suppliers", "description": "List suppliers"},
                {"method": "POST", "path": "/api/purchases", "description": "Create purchase order"},
                {"method": "POST", "path": "/api/purchases/{id}/receive", "description": "Receive purchase order & update stock"}
            ],
            "Cart, Orders & Payments": [
                {"method": "GET", "path": "/api/cart/{customer_id}", "description": "Get cart items"},
                {"method": "POST", "path": "/api/cart/{customer_id}/items", "description": "Add item to cart"},
                {"method": "POST", "path": "/api/orders/checkout", "description": "Cart-to-order checkout with stock lock"},
                {"method": "GET", "path": "/api/orders", "description": "List orders"},
                {"method": "PUT", "path": "/api/orders/{id}/status", "description": "Update order status"},
                {"method": "POST", "path": "/api/payments", "description": "Record payment & generate invoice"},
                {"method": "GET", "path": "/api/invoices/{order_id}", "description": "Get order invoice"}
            ],
            "Reporting & Audit": [
                {"method": "GET", "path": "/api/reports/sales", "description": "Sales KPI report"},
                {"method": "GET", "path": "/api/reports/inventory", "description": "Inventory valuation report"},
                {"method": "GET", "path": "/api/reports/top-products", "description": "Top-selling products"},
                {"method": "GET", "path": "/api/audit", "description": "Audit trail log (Admin)"}
            ]
        }
    }

def api_docs_handler(request):
    return Response(data=get_api_documentation(), status_code=200)
