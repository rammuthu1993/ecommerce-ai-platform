from ..database.repository import (
    find_all,
    count_all,
    save,
    find_by_id,
    update,
    delete_product_by_id
)
from ..core.exceptions import ProductNotFoundException

def get_products(
    page=1,
    limit=10,
    search=None,
    sort="id",
    order="asc",
    category_id=None,
    min_price=None,
    max_price=None,
    in_stock=None
):
    products = find_all(
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

    total = count_all(
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock
    )

    total_pages = (total + limit - 1) // limit if total > 0 else 0

    return {
        "products": products,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1
        }
    }

def create_product(data):
    product = {
        "category_id": data.get("category_id"),
        "name": data["name"],
        "price": data["price"],
        "quantity": data["quantity"]
    }
    return save(product)

def get_product(product_id):
    product = find_by_id(product_id)
    if product is None:
        raise ProductNotFoundException(product_id)
    return product

def update_product(product_id, data):
    existing = find_by_id(product_id)
    if existing is None:
        raise ProductNotFoundException(product_id)

    product = {
        "category_id": data.get("category_id", existing.get("category_id")),
        "name": data["name"],
        "price": data["price"],
        "quantity": data["quantity"]
    }
    updated = update(product_id, product)
    if not updated:
        raise ProductNotFoundException(product_id)
    return {"id": product_id, **product}

def delete_product(product_id):
    existing = find_by_id(product_id)
    if existing is None:
        raise ProductNotFoundException(product_id)
    deleted = delete_product_by_id(product_id)
    if not deleted:
        raise ProductNotFoundException(product_id)
    return True
