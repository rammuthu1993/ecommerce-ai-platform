from app.database.transaction import db_transaction
from app.suppliers.service import get_supplier
from app.database.repository import find_by_id as find_product_by_id
from app.inventory.service import adjust_stock
from app.purchases.repository import (
    save_purchase,
    find_purchase_by_id,
    find_all_purchases,
    update_purchase_status
)
from app.core.exceptions import AppException, ProductNotFoundException

def create_purchase(supplier_id, items):
    get_supplier(supplier_id)
    if not items or not isinstance(items, list):
        raise AppException("Purchase items list cannot be empty", 400, "INVALID_PURCHASE")

    total_amount = 0.0
    validated_items = []

    for item in items:
        prod_id = item.get("product_id")
        qty = item.get("quantity")
        unit_cost = item.get("unit_cost")

        if not prod_id or not find_product_by_id(prod_id):
            raise ProductNotFoundException(prod_id)
        if not qty or not isinstance(qty, int) or qty <= 0:
            raise AppException("Item quantity must be positive integer", 400, "INVALID_PURCHASE")
        if unit_cost is None or not isinstance(unit_cost, (int, float)) or unit_cost < 0:
            raise AppException("Item unit_cost must be non-negative number", 400, "INVALID_PURCHASE")

        item_total = qty * float(unit_cost)
        total_amount += item_total
        validated_items.append({"product_id": prod_id, "quantity": qty, "unit_cost": float(unit_cost)})

    with db_transaction() as conn:
        return save_purchase(supplier_id=supplier_id, items=validated_items, total_amount=total_amount, connection=conn)

def get_purchase(purchase_id):
    p = find_purchase_by_id(purchase_id)
    if p is None:
        raise AppException(f"Purchase order with id {purchase_id} not found", 404, "PURCHASE_NOT_FOUND")
    return p

def get_purchases(page=1, limit=10, status=None):
    return find_all_purchases(page=page, limit=limit, status=status)

def receive_purchase(purchase_id):
    purchase = get_purchase(purchase_id)
    if purchase["status"] == "RECEIVED":
        raise AppException("Purchase order has already been received", 400, "PURCHASE_ALREADY_RECEIVED")
    if purchase["status"] == "CANCELLED":
        raise AppException("Cannot receive cancelled purchase order", 400, "PURCHASE_CANCELLED")

    with db_transaction() as conn:
        for item in purchase["items"]:
            adjust_stock(
                product_id=item["product_id"],
                quantity_delta=item["quantity"],
                tx_type="STOCK_IN",
                reference_type="PURCHASE",
                reference_id=purchase_id
            )
        update_purchase_status(purchase_id, "RECEIVED", connection=conn)

    return get_purchase(purchase_id)
