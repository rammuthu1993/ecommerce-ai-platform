from app.discounts.repository import save_discount, find_discount_by_code, find_all_discounts
from app.core.exceptions import AppException

def create_discount(code, discount_type, value, min_purchase=0.0):
    if not code or not isinstance(code, str) or not code.strip():
        raise AppException("Discount code is required", 400, "INVALID_DISCOUNT")
    dtype = discount_type.upper()
    if dtype not in ["PERCENTAGE", "FIXED"]:
        raise AppException("Discount type must be PERCENTAGE or FIXED", 400, "INVALID_DISCOUNT")
    if not isinstance(value, (int, float)) or value <= 0:
        raise AppException("Discount value must be positive number", 400, "INVALID_DISCOUNT")
    if dtype == "PERCENTAGE" and value > 100:
        raise AppException("Percentage discount cannot exceed 100%", 400, "INVALID_DISCOUNT")

    if find_discount_by_code(code):
        raise AppException("Discount code already exists", 400, "DUPLICATE_DISCOUNT_CODE")

    return save_discount(code=code.strip(), discount_type=dtype, value=float(value), min_purchase=float(min_purchase))

def calculate_discount(code, subtotal):
    if not code:
        return 0.0
    disc = find_discount_by_code(code)
    if not disc or not disc["is_active"]:
        raise AppException("Invalid or inactive discount code", 400, "INVALID_DISCOUNT_CODE")
    if subtotal < disc["min_purchase"]:
        raise AppException(f"Subtotal of {subtotal} does not meet minimum purchase requirement of {disc['min_purchase']}", 400, "DISCOUNT_MIN_NOT_MET")

    if disc["type"] == "PERCENTAGE":
        discount_amount = (subtotal * disc["value"]) / 100.0
    else:
        discount_amount = disc["value"]

    return round(min(discount_amount, subtotal), 2)

def get_discounts():
    return find_all_discounts()
