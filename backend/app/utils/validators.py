from app.core.exceptions import InvalidPaginationException, InvalidSortingException


def validate_product(data): 
    if not isinstance(data, dict):
        return False
    if "name" not in data or not isinstance(data["name"], str) or not data["name"].strip():
        return False
    if "price" not in data or not isinstance(data["price"], (int, float)) or data["price"] < 0:
        return False
    if "quantity" not in data or not isinstance(data["quantity"], int) or data["quantity"] < 0:
        return False
    return True

def parse_pagination(request):

    try:

        page = int(
            request.query_params.get(
                "page",
                1
            )
        )

        limit = int(
            request.query_params.get(
                "limit",
                10
            )
        )

    except ValueError:

        raise InvalidPaginationException()

    if page < 1:

        raise InvalidPaginationException(
            "Page must be greater than 0"
        )

    if limit < 1:

        raise InvalidPaginationException(
            "Limit must be greater than 0"
        )

    if limit > 100:

        raise InvalidPaginationException(
            "Limit cannot be greater than 100"
        )

    return page, limit

def validate_sorting(sort, order):

    allowed_fields = {
        "id",
        "name",
        "price",
        "quantity"
    }

    allowed_orders = {
        "asc",
        "desc"
    }

    if sort not in allowed_fields:
        raise InvalidSortingException(
            "Invalid sort field"
        )

    if order not in allowed_orders:
        raise InvalidSortingException(
            "Invalid sort order"
        )