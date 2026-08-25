from ..web.response import Response
from ..config.settings import settings


def cors_middleware(request, next_handler):
    print("cors")
    if request.method == "OPTIONS":

        response = Response(
            status_code=204
        )

    else:

        response = next_handler(request)

    response.headers[
        "Access-Control-Allow-Origin"
    ] = settings.cors_origins

    response.headers[
        "Access-Control-Allow-Methods"
    ] = "GET, POST, PUT, DELETE, OPTIONS"

    response.headers[
        "Access-Control-Allow-Headers"
    ] = "Content-Type, Authorization"

    return response