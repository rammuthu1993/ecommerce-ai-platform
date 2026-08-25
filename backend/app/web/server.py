from http.server import HTTPServer, BaseHTTPRequestHandler

from app.config.settings import settings
from app.web.middleware import MiddlewareManager
from app.web.router import Router
from app.web.request import Request
from app.web.response import Response

from app.middleware.cors import cors_middleware
from app.middleware.logging import logging_middleware
from app.middleware.security import security_headers_middleware, content_type_middleware
from app.middleware.rate_limit import rate_limit_middleware
from app.middleware.auth import auth_middleware, require_auth, require_roles

from app.core.exceptions import (
    AppException,
    InvalidProductException,
    PayloadTooLargeException
)

from app.utils.validators import validate_product, parse_pagination, validate_sorting

# Domain Services
from app.auth.auth_service import register_user, login_user, change_password
from app.users.service import get_users, get_user, assign_user_role, change_user_status, delete_user_account
from app.web.health import health_check_handler
from app.docs.api_docs import api_docs_handler

# Phase 3 Analytics Services
from app.analytics.numpy_analytics import calculate_sales_statistics, benchmark_numpy_vs_python
from app.analytics.pandas_analytics import get_sales_by_groupby, get_sales_time_series, calculate_customer_rfm_segmentation
from app.analytics.scipy_analytics import perform_ab_test_ttest, optimize_optimal_price, optimize_economic_order_quantity
from app.analytics.kpi_service import get_executive_kpis
from app.analytics.export_service import generate_export_dataset

# Phase 4 AI, RAG & Agent Services
from app.ai.provider import get_llm_provider
from app.ai.token_tracker import token_tracker
from app.rag.rag_service import answer_rag_query
from app.rag.document_processor import build_knowledge_chunks
from app.agent.agent_service import run_business_agent
from app.agent.memory import agent_memory
from app.agent.metrics import agent_metrics

from app.products.service import (
    get_products,
    create_product,
    get_product,
    update_product,
    delete_product
)
from app.categories.service import (
    get_categories,
    create_category,
    get_category,
    update_category_service,
    delete_category_service
)
from app.inventory.service import (
    get_all_inventory,
    adjust_stock,
    get_low_stock,
    get_out_of_stock
)
from app.suppliers.service import (
    get_suppliers,
    create_supplier,
    get_supplier,
    update_supplier_service,
    delete_supplier_service
)
from app.purchases.service import (
    get_purchases,
    create_purchase,
    get_purchase,
    receive_purchase
)
from app.customers.service import (
    get_customers,
    create_customer,
    get_customer,
    update_customer_service,
    delete_customer_service,
    add_customer_address,
    get_customer_addresses
)
from app.cart.service import (
    get_customer_cart,
    add_to_cart,
    update_cart_item,
    remove_from_cart,
    clear_customer_cart
)
from app.orders.service import (
    checkout_order,
    get_orders,
    get_order,
    update_order_status_service
)
from app.payments.service import (
    record_payment,
    get_payments_for_order
)
from app.invoices.service import (
    get_invoice_by_order
)
from app.discounts.service import (
    get_discounts,
    create_discount
)
from app.reporting.service import (
    get_sales_report,
    get_purchase_report,
    get_inventory_report,
    get_customer_report,
    get_top_products_report
)
from app.audit.service import (
    get_audit_trail,
    log_audit
)


# ============================================================
# Handlers
# ============================================================

def home(request):
    return Response(data={"message": "Ecommerce AI Platform API is running"}, status_code=200)

# --- Phase 4 AI, RAG & Agent Handlers ---
def ai_chat_handler(request):
    payload = request.json()
    prompt = payload.get("prompt", "")
    provider = get_llm_provider()
    reply = provider.generate(prompt)
    return Response(data={"prompt": prompt, "reply": reply}, status_code=200)

def ai_rag_handler(request):
    payload = request.json()
    query = payload.get("query", "")
    res = answer_rag_query(query=query)
    return Response(data=res, status_code=200)

def ai_agent_handler(request):
    payload = request.json()
    query = payload.get("query", "")
    session_id = payload.get("session_id")
    user_id = request.user["id"] if getattr(request, "user", None) else None
    user_roles = request.user["roles"] if getattr(request, "user", None) else ["CUSTOMER"]
    res = run_business_agent(query=query, user_id=user_id, user_roles=user_roles, session_id=session_id)
    return Response(data=res, status_code=200)

def ai_knowledge_handler(request):
    chunks = build_knowledge_chunks()
    return Response(data=chunks, status_code=200)

def ai_token_usage_handler(request):
    summary = token_tracker.get_summary()
    return Response(data=summary, status_code=200)

def ai_agent_metrics_handler(request):
    summary = agent_metrics.get_summary()
    return Response(data=summary, status_code=200)

def ai_agent_clear_memory_handler(request):
    session_id = request.params["session_id"]
    cleared = agent_memory.clear_session(session_id)
    return Response(data={"session_id": session_id, "cleared": cleared}, status_code=200)


# --- Phase 3 Analytics Handlers ---
def analytics_kpis_handler(request):
    kpis = get_executive_kpis()
    return Response(data=kpis, status_code=200)

def analytics_sales_trend_handler(request):
    freq = request.query_params.get("freq", "D").upper()
    trend = get_sales_time_series(freq=freq)
    return Response(data=trend, status_code=200)

def analytics_groupby_handler(request):
    field = request.query_params.get("by", "category").lower()
    res = get_sales_by_groupby(groupby_field=field)
    return Response(data=res, status_code=200)

def analytics_rfm_handler(request):
    rfm = calculate_customer_rfm_segmentation()
    return Response(data=rfm, status_code=200)

def analytics_numpy_benchmark_handler(request):
    num_items = int(request.query_params.get("items", 100000))
    res = benchmark_numpy_vs_python(num_items=num_items)
    return Response(data=res, status_code=200)

def analytics_demand_optimization_handler(request):
    base_price = float(request.query_params.get("base_price", 1000.0))
    res = optimize_optimal_price(base_price=base_price)
    return Response(data=res, status_code=200)

def analytics_export_handler(request):
    dataset_type = request.query_params.get("dataset", "sales")
    format_type = request.query_params.get("format", "csv")
    content, content_type = generate_export_dataset(dataset_type=dataset_type, format_type=format_type)

    if isinstance(content, bytes):
        resp_body = content
    else:
        resp_body = content.encode("utf-8")

    response = Response(status_code=200)
    response.headers["Content-Type"] = content_type
    response.headers["Content-Disposition"] = f'attachment; filename="{dataset_type}_export.{format_type}"'
    response.to_bytes = lambda: resp_body
    return response


# --- Authentication ---
def register_handler(request):
    payload = request.json()
    res = register_user(
        username=payload.get("username"),
        email=payload.get("email"),
        password=payload.get("password"),
        roles=payload.get("roles")
    )
    log_audit("REGISTER", "AUTH", "USER", entity_id=res["user"]["id"], details=f"User {res['user']['email']} registered")
    return Response(data=res, status_code=201, message="User registered successfully")

def login_handler(request):
    payload = request.json()
    res = login_user(email=payload.get("email"), password=payload.get("password"))
    log_audit("LOGIN", "AUTH", "USER", entity_id=res["user"]["id"], details=f"User {res['user']['email']} logged in")
    return Response(data=res, status_code=200, message="Login successful")

def me_handler(request):
    require_auth(request)
    try:
        user = get_user(request.user["id"])
        return Response(data=user, status_code=200)
    except Exception:
        email = request.user.get("email", "")
        return Response(data={
            "id": request.user["id"],
            "username": email.split("@")[0] if "@" in email else "User",
            "email": email,
            "status": "ACTIVE",
            "roles": request.user.get("roles", ["CUSTOMER"])
        }, status_code=200)

def change_password_handler(request):
    require_auth(request)
    payload = request.json()
    change_password(
        user_id=request.user["id"],
        old_password=payload.get("old_password"),
        new_password=payload.get("new_password")
    )
    return Response(data={"success": True}, status_code=200, message="Password updated successfully")

# --- User Management (Admin Protected) ---
def users_list_handler(request):
    require_roles(request, ["ADMIN"])
    page, limit = parse_pagination(request)
    search = request.query_params.get("search")
    res = get_users(page=page, limit=limit, search=search)
    return Response(data=res["users"], pagination=res["pagination"])

def user_detail_handler(request):
    require_roles(request, ["ADMIN"])
    u_id = int(request.params["id"])
    user = get_user(u_id)
    return Response(data=user, status_code=200)

def user_status_handler(request):
    require_roles(request, ["ADMIN"])
    u_id = int(request.params["id"])
    payload = request.json()
    updated = change_user_status(u_id, payload.get("status"))
    return Response(data=updated, status_code=200)

def assign_role_handler(request):
    require_roles(request, ["ADMIN"])
    u_id = int(request.params["id"])
    payload = request.json()
    updated = assign_user_role(u_id, payload.get("role"))
    return Response(data=updated, status_code=200)


# --- Products ---
def products_handler(request):
    page, limit = parse_pagination(request)
    search = request.query_params.get("search")
    sort = request.query_params.get("sort", "id")
    order = request.query_params.get("order", "asc")
    category_id = int(request.query_params["category_id"]) if "category_id" in request.query_params else None
    min_price = float(request.query_params["min_price"]) if "min_price" in request.query_params else None
    max_price = float(request.query_params["max_price"]) if "max_price" in request.query_params else None
    in_stock = request.query_params.get("in_stock", "").lower() == "true" if "in_stock" in request.query_params else None

    validate_sorting(sort, order)

    result = get_products(
        page=page,
        limit=limit,
        search=search,
        sort=sort,
        order=order,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock
    )
    return Response(data=result["products"], pagination=result["pagination"])

def create_product_handler(request):
    payload = request.json()
    if not validate_product(payload):
        raise InvalidProductException(message="Invalid product data")

    product = create_product(payload)
    log_audit("CREATE", "PRODUCTS", "PRODUCT", entity_id=product["id"], details=f"Created product {product['name']}")
    return Response(data=product, status_code=201, message="Product created successfully")

def get_product_handler(request):
    product_id = int(request.params["id"])
    product = get_product(product_id)
    return Response(data=product, status_code=200, message="Product retrieved successfully")

def update_product_handler(request):
    product_id = int(request.params["id"])
    payload = request.json()
    if not validate_product(payload):
        raise InvalidProductException(message="Invalid product data")

    updated = update_product(product_id, payload)
    log_audit("UPDATE", "PRODUCTS", "PRODUCT", entity_id=product_id, details=f"Updated product {product_id}")
    return Response(data=updated, status_code=200, message="Product updated successfully")

def delete_product_handler(request):
    product_id = int(request.params["id"])
    delete_product(product_id)
    log_audit("DELETE", "PRODUCTS", "PRODUCT", entity_id=product_id, details=f"Deleted product {product_id}")
    return Response(data={"product_id": product_id}, status_code=200, message="Product successfully deleted")


# --- Categories ---
def categories_handler(request):
    page, limit = parse_pagination(request)
    search = request.query_params.get("search")
    res = get_categories(page=page, limit=limit, search=search)
    return Response(data=res["categories"], pagination=res["pagination"])

def create_category_handler(request):
    cat = create_category(request.json())
    log_audit("CREATE", "CATEGORIES", "CATEGORY", entity_id=cat["id"], details=f"Created category {cat['name']}")
    return Response(data=cat, status_code=201, message="Category created successfully")

def get_category_handler(request):
    cat = get_category(int(request.params["id"]))
    return Response(data=cat, status_code=200)

def update_category_handler(request):
    cat_id = int(request.params["id"])
    updated = update_category_service(cat_id, request.json())
    return Response(data=updated, status_code=200, message="Category updated successfully")

def delete_category_handler(request):
    cat_id = int(request.params["id"])
    delete_category_service(cat_id)
    return Response(data={"category_id": cat_id}, status_code=200, message="Category deleted successfully")


# --- Inventory ---
def inventory_handler(request):
    page, limit = parse_pagination(request)
    items = get_all_inventory(page=page, limit=limit)
    return Response(data=items, status_code=200)

def adjust_inventory_handler(request):
    payload = request.json()
    product_id = int(payload["product_id"])
    quantity_delta = int(payload["quantity_delta"])
    tx_type = payload.get("tx_type", "ADJUSTMENT")

    updated = adjust_stock(product_id, quantity_delta, tx_type=tx_type)
    return Response(data=updated, status_code=200, message="Inventory stock adjusted successfully")

def low_stock_handler(request):
    threshold = int(request.query_params.get("threshold", 5))
    items = get_low_stock(threshold=threshold)
    return Response(data=items, status_code=200)

def out_of_stock_handler(request):
    items = get_out_of_stock()
    return Response(data=items, status_code=200)


# --- Suppliers & Purchases ---
def suppliers_handler(request):
    page, limit = parse_pagination(request)
    search = request.query_params.get("search")
    res = get_suppliers(page=page, limit=limit, search=search)
    return Response(data=res["suppliers"], pagination=res["pagination"])

def create_supplier_handler(request):
    sup = create_supplier(request.json())
    return Response(data=sup, status_code=201, message="Supplier created successfully")

def get_supplier_handler(request):
    sup = get_supplier(int(request.params["id"]))
    return Response(data=sup, status_code=200)

def update_supplier_handler(request):
    updated = update_supplier_service(int(request.params["id"]), request.json())
    return Response(data=updated, status_code=200)

def delete_supplier_handler(request):
    sup_id = int(request.params["id"])
    delete_supplier_service(sup_id)
    return Response(data={"supplier_id": sup_id}, status_code=200)

def purchases_handler(request):
    page, limit = parse_pagination(request)
    status = request.query_params.get("status")
    items = get_purchases(page=page, limit=limit, status=status)
    return Response(data=items, status_code=200)

def create_purchase_handler(request):
    payload = request.json()
    po = create_purchase(supplier_id=int(payload["supplier_id"]), items=payload["items"])
    return Response(data=po, status_code=201, message="Purchase order created")

def get_purchase_handler(request):
    po = get_purchase(int(request.params["id"]))
    return Response(data=po, status_code=200)

def receive_purchase_handler(request):
    po_id = int(request.params["id"])
    received = receive_purchase(po_id)
    return Response(data=received, status_code=200, message="Purchase order received and stock added")


# --- Customers & Addresses ---
def customers_handler(request):
    page, limit = parse_pagination(request)
    search = request.query_params.get("search")
    res = get_customers(page=page, limit=limit, search=search)
    return Response(data=res["customers"], pagination=res["pagination"])

def create_customer_handler(request):
    c = create_customer(request.json())
    return Response(data=c, status_code=201, message="Customer created successfully")

def get_customer_handler(request):
    c = get_customer(int(request.params["id"]))
    return Response(data=c, status_code=200)

def update_customer_handler(request):
    updated = update_customer_service(int(request.params["id"]), request.json())
    return Response(data=updated, status_code=200)

def delete_customer_handler(request):
    c_id = int(request.params["id"])
    delete_customer_service(c_id)
    return Response(data={"customer_id": c_id}, status_code=200)

def get_addresses_handler(request):
    c_id = int(request.params["id"])
    addresses = get_customer_addresses(c_id)
    return Response(data=addresses, status_code=200)

def add_address_handler(request):
    c_id = int(request.params["id"])
    addr = add_customer_address(c_id, request.json())
    return Response(data=addr, status_code=201)


# --- Cart & Orders ---
def get_cart_handler(request):
    c_id = int(request.params["customer_id"])
    cart = get_customer_cart(c_id)
    return Response(data=cart, status_code=200)

def add_cart_item_handler(request):
    c_id = int(request.params["customer_id"])
    payload = request.json()
    cart = add_to_cart(c_id, int(payload["product_id"]), int(payload["quantity"]))
    return Response(data=cart, status_code=200)

def update_cart_item_handler(request):
    c_id = int(request.params["customer_id"])
    payload = request.json()
    cart = update_cart_item(c_id, int(payload["product_id"]), int(payload["quantity"]))
    return Response(data=cart, status_code=200)

def remove_cart_item_handler(request):
    c_id = int(request.params["customer_id"])
    p_id = int(request.params["product_id"])
    cart = remove_from_cart(c_id, p_id)
    return Response(data=cart, status_code=200)

def clear_cart_handler(request):
    c_id = int(request.params["customer_id"])
    cart = clear_customer_cart(c_id)
    return Response(data=cart, status_code=200)

def checkout_handler(request):
    payload = request.json()
    c_id = int(payload["customer_id"])
    shipping_address_id = payload.get("shipping_address_id")
    order = checkout_order(customer_id=c_id, shipping_address_id=shipping_address_id)
    log_audit("CREATE", "ORDERS", "ORDER", entity_id=order["id"], details=f"Placed order {order['order_number']}")
    return Response(data=order, status_code=201, message="Order created successfully")

def orders_handler(request):
    page, limit = parse_pagination(request)
    customer_id = int(request.query_params["customer_id"]) if "customer_id" in request.query_params else None
    status = request.query_params.get("status")
    res = get_orders(page=page, limit=limit, customer_id=customer_id, status=status)
    return Response(data=res["orders"], pagination=res["pagination"])

def get_order_handler(request):
    order = get_order(int(request.params["id"]))
    return Response(data=order, status_code=200)

def update_order_status_handler(request):
    order_id = int(request.params["id"])
    payload = request.json()
    updated = update_order_status_service(order_id, payload["status"])
    log_audit("UPDATE", "ORDERS", "ORDER", entity_id=order_id, details=f"Updated order status to {payload['status']}")
    return Response(data=updated, status_code=200)


# --- Payments & Invoices ---
def create_payment_handler(request):
    payload = request.json()
    res = record_payment(
        order_id=int(payload["order_id"]),
        payment_method=payload["payment_method"],
        amount=payload["amount"],
        transaction_reference=payload.get("transaction_reference")
    )
    log_audit("CREATE", "PAYMENTS", "PAYMENT", entity_id=res["payment"]["id"], details=f"Payment recorded for order {payload['order_id']}")
    return Response(data=res, status_code=201, message="Payment recorded successfully")

def get_payments_handler(request):
    order_id = int(request.params["order_id"])
    payments = get_payments_for_order(order_id)
    return Response(data=payments, status_code=200)

def get_invoice_handler(request):
    order_id = int(request.params["order_id"])
    inv = get_invoice_by_order(order_id)
    return Response(data=inv, status_code=200)


# --- Discounts ---
def discounts_handler(request):
    discounts = get_discounts()
    return Response(data=discounts, status_code=200)

def create_discount_handler(request):
    payload = request.json()
    disc = create_discount(
        code=payload["code"],
        discount_type=payload["type"],
        value=payload["value"],
        min_purchase=payload.get("min_purchase", 0.0)
    )
    return Response(data=disc, status_code=201)


# --- Reporting & Audit ---
def report_sales_handler(request):
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")
    return Response(data=get_sales_report(start_date=start_date, end_date=end_date), status_code=200)

def report_purchases_handler(request):
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")
    return Response(data=get_purchase_report(start_date=start_date, end_date=end_date), status_code=200)

def report_inventory_handler(request):
    return Response(data=get_inventory_report(), status_code=200)

def report_customers_handler(request):
    return Response(data=get_customer_report(), status_code=200)

def report_top_products_handler(request):
    limit = int(request.query_params.get("limit", 10))
    return Response(data=get_top_products_report(limit=limit), status_code=200)

def audit_logs_handler(request):
    page, limit = parse_pagination(request)
    module = request.query_params.get("module")
    entity = request.query_params.get("entity")
    logs = get_audit_trail(page=page, limit=limit, module=module, entity=entity)
    return Response(data=logs, status_code=200)


# ============================================================
# Router Registration
# ============================================================

router = Router()

router.add_route("GET", "/", home)

# Health & Docs
router.add_route("GET", "/health", health_check_handler)
router.add_route("GET", "/api/docs", api_docs_handler)

# Phase 4 AI, RAG & Agent Routes
router.add_route("POST", "/api/ai/chat", ai_chat_handler)
router.add_route("POST", "/api/ai/rag/query", ai_rag_handler)
router.add_route("POST", "/api/ai/agent/query", ai_agent_handler)
router.add_route("GET", "/api/ai/knowledge", ai_knowledge_handler)
router.add_route("GET", "/api/ai/token-usage", ai_token_usage_handler)
router.add_route("GET", "/api/ai/agent/metrics", ai_agent_metrics_handler)
router.add_route("DELETE", "/api/ai/agent/memory/{session_id}", ai_agent_clear_memory_handler)

# Phase 3 Analytics
router.add_route("GET", "/api/analytics/kpis", analytics_kpis_handler)
router.add_route("GET", "/api/analytics/sales-trend", analytics_sales_trend_handler)
router.add_route("GET", "/api/analytics/groupby", analytics_groupby_handler)
router.add_route("GET", "/api/analytics/rfm-segmentation", analytics_rfm_handler)
router.add_route("GET", "/api/analytics/numpy-benchmark", analytics_numpy_benchmark_handler)
router.add_route("GET", "/api/analytics/demand-optimization", analytics_demand_optimization_handler)
router.add_route("GET", "/api/analytics/export", analytics_export_handler)

# Authentication
router.add_route("POST", "/api/auth/register", register_handler)
router.add_route("POST", "/api/auth/login", login_handler)
router.add_route("GET", "/api/auth/me", me_handler)
router.add_route("PUT", "/api/auth/password", change_password_handler)

# User Management & RBAC
router.add_route("GET", "/api/users", users_list_handler)
router.add_route("GET", "/api/users/{id}", user_detail_handler)
router.add_route("PUT", "/api/users/{id}/status", user_status_handler)
router.add_route("POST", "/api/users/{id}/roles", assign_role_handler)

# Products
router.add_route("GET", "/products", products_handler)
router.add_route("GET", "/api/products", products_handler)
router.add_route("POST", "/api/products", create_product_handler)
router.add_route("GET", "/api/products/{id}", get_product_handler)
router.add_route("PUT", "/api/products/{id}", update_product_handler)
router.add_route("DELETE", "/api/products/{id}", delete_product_handler)

# Categories
router.add_route("GET", "/api/categories", categories_handler)
router.add_route("POST", "/api/categories", create_category_handler)
router.add_route("GET", "/api/categories/{id}", get_category_handler)
router.add_route("PUT", "/api/categories/{id}", update_category_handler)
router.add_route("DELETE", "/api/categories/{id}", delete_category_handler)

# Inventory
router.add_route("GET", "/api/inventory", inventory_handler)
router.add_route("POST", "/api/inventory/adjust", adjust_inventory_handler)
router.add_route("GET", "/api/inventory/low-stock", low_stock_handler)
router.add_route("GET", "/api/inventory/out-of-stock", out_of_stock_handler)

# Suppliers & Purchases
router.add_route("GET", "/api/suppliers", suppliers_handler)
router.add_route("POST", "/api/suppliers", create_supplier_handler)
router.add_route("GET", "/api/suppliers/{id}", get_supplier_handler)
router.add_route("PUT", "/api/suppliers/{id}", update_supplier_handler)
router.add_route("DELETE", "/api/suppliers/{id}", delete_supplier_handler)

router.add_route("GET", "/api/purchases", purchases_handler)
router.add_route("POST", "/api/purchases", create_purchase_handler)
router.add_route("GET", "/api/purchases/{id}", get_purchase_handler)
router.add_route("POST", "/api/purchases/{id}/receive", receive_purchase_handler)

# Customers & Addresses
router.add_route("GET", "/api/customers", customers_handler)
router.add_route("POST", "/api/customers", create_customer_handler)
router.add_route("GET", "/api/customers/{id}", get_customer_handler)
router.add_route("PUT", "/api/customers/{id}", update_customer_handler)
router.add_route("DELETE", "/api/customers/{id}", delete_customer_handler)
router.add_route("GET", "/api/customers/{id}/addresses", get_addresses_handler)
router.add_route("POST", "/api/customers/{id}/addresses", add_address_handler)

# Cart & Orders
router.add_route("GET", "/api/cart/{customer_id}", get_cart_handler)
router.add_route("POST", "/api/cart/{customer_id}/items", add_cart_item_handler)
router.add_route("PUT", "/api/cart/{customer_id}/items", update_cart_item_handler)
router.add_route("DELETE", "/api/cart/{customer_id}/items/{product_id}", remove_cart_item_handler)
router.add_route("DELETE", "/api/cart/{customer_id}", clear_cart_handler)

router.add_route("POST", "/api/orders/checkout", checkout_handler)
router.add_route("GET", "/api/orders", orders_handler)
router.add_route("GET", "/api/orders/{id}", get_order_handler)
router.add_route("PUT", "/api/orders/{id}/status", update_order_status_handler)

# Payments, Invoices & Discounts
router.add_route("POST", "/api/payments", create_payment_handler)
router.add_route("GET", "/api/payments/{order_id}", get_payments_handler)
router.add_route("GET", "/api/invoices/{order_id}", get_invoice_handler)

router.add_route("GET", "/api/discounts", discounts_handler)
router.add_route("POST", "/api/discounts", create_discount_handler)

# Reporting & Audit
router.add_route("GET", "/api/reports/sales", report_sales_handler)
router.add_route("GET", "/api/reports/purchases", report_purchases_handler)
router.add_route("GET", "/api/reports/inventory", report_inventory_handler)
router.add_route("GET", "/api/reports/customers", report_customers_handler)
router.add_route("GET", "/api/reports/top-products", report_top_products_handler)
router.add_route("GET", "/api/audit", audit_logs_handler)


# ============================================================
# HTTP Request Handler & Middleware Manager Setup
# ============================================================

class EcommerceRequestHandler(BaseHTTPRequestHandler):

    middleware_manager = MiddlewareManager()
    middleware_manager.add(logging_middleware)
    middleware_manager.add(cors_middleware)
    middleware_manager.add(security_headers_middleware)
    middleware_manager.add(auth_middleware)
    middleware_manager.add(content_type_middleware)
    middleware_manager.add(rate_limit_middleware)

    def do_GET(self):
        self.handle_request("GET")

    def do_POST(self):
        body = self.read_request_body()
        self.handle_request("POST", body)

    def do_PUT(self):
        body = self.read_request_body()
        self.handle_request("PUT", body)

    def do_DELETE(self):
        self.handle_request("DELETE")

    def do_OPTIONS(self):
        response = Response(data=None, status_code=204)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        self.send_response_to_client(response)

    def read_request_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > settings.max_request_size:
            raise PayloadTooLargeException()

        body = self.rfile.read(content_length)
        return body.decode("utf-8")

    def handle_request(self, method, body=None):
        request = Request(
            method=method,
            path=self.path,
            headers=dict(self.headers),
            body=body
        )

        try:
            response = self.middleware_manager.execute(request, route_request)
        except AppException as error:
            response = Response(
                status_code=error.status_code,
                error={
                    "code": error.code,
                    "message": error.message
                }
            )
        except Exception as error:
            print("Unexpected server error:", error)
            response = Response(
                data={"error": "Internal Server Error"},
                status_code=500
            )

        self.send_response_to_client(response)

    def send_response_to_client(self, response):
        self.send_response(response.status_code)
        for name, value in response.headers.items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(response.to_bytes())


def route_request(request):
    handler, params = router.find_route(request.method, request.path)
    request.params = params

    if handler is None:
        return Response(data=None, status_code=404, error="Route is Not Found")

    return handler(request)


def start_server():
    server_address = (settings.host, settings.port)
    server = HTTPServer(server_address, EcommerceRequestHandler)
    print(f"Server is Running on http://{settings.host}:{settings.port}")
    server.serve_forever()
