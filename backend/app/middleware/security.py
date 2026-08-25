from app.core.exceptions import AppException

def security_headers_middleware(request, next_handler):
    print("security")
    response = next_handler(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

def content_type_middleware(request, next_handler):
    print("content") 
    if request.method in ["POST", "PUT", "PATCH"] and request.body:
        content_type = request.headers.get("content-type", "").lower()
        if "application/json" not in content_type:
            raise AppException("Content-Type must be application/json", 415, "UNSUPPORTED_MEDIA_TYPE")
    return next_handler(request)
