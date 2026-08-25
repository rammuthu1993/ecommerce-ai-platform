class AppException(Exception):

    def __init__(
        self,
        message,
        status_code=400,
        code="APPLICATION_ERROR"
    ):
        self.message = message
        self.status_code = status_code
        self.code = code
        super().__init__(message)


class ProductNotFoundException(AppException):

    def __init__(self, product_id):
        super().__init__(
            f"Product with id {product_id} is not found",
            404,
            "PRODUCT_NOT_FOUND"
        )


class CategoryNotFoundException(AppException):

    def __init__(self, category_id):
        super().__init__(
            f"Category with id {category_id} is not found",
            404,
            "CATEGORY_NOT_FOUND"
        )


class SupplierNotFoundException(AppException):

    def __init__(self, supplier_id):
        super().__init__(
            f"Supplier with id {supplier_id} is not found",
            404,
            "SUPPLIER_NOT_FOUND"
        )


class CustomerNotFoundException(AppException):

    def __init__(self, customer_id):
        super().__init__(
            f"Customer with id {customer_id} is not found",
            404,
            "CUSTOMER_NOT_FOUND"
        )


class AddressNotFoundException(AppException):

    def __init__(self, address_id):
        super().__init__(
            f"Address with id {address_id} is not found",
            404,
            "ADDRESS_NOT_FOUND"
        )


class OrderNotFoundException(AppException):

    def __init__(self, order_id):
        super().__init__(
            f"Order with id {order_id} is not found",
            404,
            "ORDER_NOT_FOUND"
        )


class CartNotFoundException(AppException):

    def __init__(self, cart_id):
        super().__init__(
            f"Cart with id {cart_id} is not found",
            404,
            "CART_NOT_FOUND"
        )


class InsufficientStockException(AppException):

    def __init__(self, product_id, requested, available):
        super().__init__(
            f"Insufficient stock for product {product_id}: requested {requested}, available {available}",
            400,
            "INSUFFICIENT_STOCK"
        )


class InvalidOrderTransitionException(AppException):

    def __init__(self, current_status, target_status):
        super().__init__(
            f"Cannot transition order from status '{current_status}' to '{target_status}'",
            400,
            "INVALID_ORDER_TRANSITION"
        )


class InvalidProductException(AppException):

    def __init__(
        self,
        message="Invalid product data"
    ):
        super().__init__(
            message,
            400,
            "INVALID_PRODUCT"
        )


class InvalidJsonException(AppException):

    def __init__(
        self,
        message="Invalid JSON"
    ):
        super().__init__(
            message,
            400,
            "INVALID_JSON"
        )


class InvalidProductIdException(AppException):

    def __init__(self, product_id):
        super().__init__(
            f"Invalid product id: {product_id}",
            400,
            "INVALID_PRODUCT_ID"
        )


class InvalidPaginationException(AppException):

    def __init__(
        self,
        message="Invalid pagination parameters"
    ):
        super().__init__(
            message,
            400,
            "INVALID_PAGINATION"
        )


class InvalidSortingException(AppException):

    def __init__(
        self,
        message="Invalid sorting parameters"
    ):
        super().__init__(
            message,
            400,
            "INVALID_SORTING"
        )


class PayloadTooLargeException(AppException):

    def __init__(
        self,
        message="Request payload exceeds max allowed size"
    ):
        super().__init__(
            message,
            413,
            "PAYLOAD_TOO_LARGE"
        )


class RateLimitExceededException(AppException):

    def __init__(
        self,
        message="Rate limit exceeded. Please try again later."
    ):
        super().__init__(
            message,
            429,
            "RATE_LIMIT_EXCEEDED"
        )


class UnauthorizedException(AppException):

    def __init__(
        self,
        message="Authentication credentials required"
    ):
        super().__init__(
            message,
            401,
            "UNAUTHORIZED"
        )


class ForbiddenException(AppException):

    def __init__(
        self,
        message="Permission denied"
    ):
        super().__init__(
            message,
            403,
            "FORBIDDEN"
        )


class InvalidTokenException(AppException):

    def __init__(
        self,
        message="Invalid authentication token"
    ):
        super().__init__(
            message,
            401,
            "INVALID_TOKEN"
        )


class TokenExpiredException(AppException):

    def __init__(
        self,
        message="Authentication token has expired"
    ):
        super().__init__(
            message,
            401,
            "TOKEN_EXPIRED"
        )


class UserNotFoundException(AppException):

    def __init__(self, identifier):
        super().__init__(
            f"User '{identifier}' not found",
            404,
            "USER_NOT_FOUND"
        )
