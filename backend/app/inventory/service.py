from app.database.transaction import db_transaction
from app.database.repository import find_by_id as find_product_by_id
from app.core.exceptions import ProductNotFoundException, InsufficientStockException, AppException
from app.inventory.repository import (
    save_inventory,
    find_inventory_by_product_id,
    update_inventory_stock,
    save_inventory_transaction,
    get_inventory_transactions,
    find_low_stock_inventory,
    find_out_of_stock_inventory,
    find_all_inventory
)

def get_or_create_inventory(product_id, initial_stock=0, location=None, connection=None):
    product = find_product_by_id(product_id, connection=connection)
    if product is None:
        raise ProductNotFoundException(product_id)

    inv = find_inventory_by_product_id(product_id, connection=connection)
    if inv is None:
        inv = save_inventory(product_id=product_id, stock_quantity=initial_stock, location=location, connection=connection)
    return inv

def adjust_stock(product_id, quantity_delta, tx_type="ADJUSTMENT", reference_type=None, reference_id=None, connection=None):
    product = find_product_by_id(product_id, connection=connection)
    if product is None:
        raise ProductNotFoundException(product_id)

    with db_transaction(connection=connection) as conn:
        inv = find_inventory_by_product_id(product_id, connection=conn)
        if inv is None:
            inv = save_inventory(product_id=product_id, stock_quantity=0, connection=conn)

        current_available = inv["available_quantity"]
        if quantity_delta < 0 and (current_available + quantity_delta) < 0:
            raise InsufficientStockException(product_id, abs(quantity_delta), current_available)

        update_inventory_stock(product_id=product_id, stock_change=quantity_delta, connection=conn)
        save_inventory_transaction(
            inventory_id=inv["id"],
            tx_type=tx_type,
            quantity=quantity_delta,
            reference_type=reference_type,
            reference_id=reference_id,
            connection=conn
        )
        return find_inventory_by_product_id(product_id, connection=conn)

def reserve_stock(product_id, quantity, reference_type="ORDER", reference_id=None, connection=None):
    product = find_product_by_id(product_id, connection=connection)
    if product is None:
        raise ProductNotFoundException(product_id)

    with db_transaction(connection=connection) as conn:
        inv = find_inventory_by_product_id(product_id, connection=conn)
        if inv is None:
            inv = save_inventory(product_id=product_id, stock_quantity=0, connection=conn)

        if inv["available_quantity"] < quantity:
            raise InsufficientStockException(product_id, quantity, inv["available_quantity"])

        update_inventory_stock(product_id=product_id, stock_change=0, reserved_change=quantity, connection=conn)
        save_inventory_transaction(
            inventory_id=inv["id"],
            tx_type="RESERVE",
            quantity=quantity,
            reference_type=reference_type,
            reference_id=reference_id,
            connection=conn
        )
        return True

def release_stock(product_id, quantity, reference_type="ORDER", reference_id=None, connection=None):
    with db_transaction(connection=connection) as conn:
        inv = find_inventory_by_product_id(product_id, connection=conn)
        if inv is None:
            return False

        release_qty = min(quantity, inv["reserved_quantity"])
        update_inventory_stock(product_id=product_id, stock_change=0, reserved_change=-release_qty, connection=conn)
        save_inventory_transaction(
            inventory_id=inv["id"],
            tx_type="RELEASE",
            quantity=-release_qty,
            reference_type=reference_type,
            reference_id=reference_id,
            connection=conn
        )
        return True

def get_inventory_by_product(product_id, connection=None):
    product = find_product_by_id(product_id, connection=connection)
    if product is None:
        raise ProductNotFoundException(product_id)

    inv = find_inventory_by_product_id(product_id, connection=connection)
    if inv is None:
        inv = save_inventory(product_id=product_id, stock_quantity=product["quantity"], connection=connection)
    return inv

def get_all_inventory(page=1, limit=10, connection=None):
    return find_all_inventory(page=page, limit=limit, connection=connection)

def get_low_stock(threshold=5, connection=None):
    return find_low_stock_inventory(threshold=threshold, connection=connection)

def get_out_of_stock(connection=None):
    return find_out_of_stock_inventory(connection=connection)

def get_transaction_history(product_id, connection=None):
    inv = get_inventory_by_product(product_id, connection=connection)
    return get_inventory_transactions(inv["id"], connection=connection)
