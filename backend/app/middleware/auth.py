from app.auth.jwt_engine import verify_jwt
from app.core.exceptions import UnauthorizedException, ForbiddenException

def auth_middleware(request, next_handler):
    auth_header = ""
    print("auth")
    if hasattr(request, "headers") and request.headers:
        for k, v in request.headers.items():
            if str(k).lower() in ("authorization", "http_authorization"):
                auth_header = str(v)
                break

    if auth_header.startswith("Bearer "):
        token = auth_header[7:].strip()
        try:
            payload = verify_jwt(token)
            request.user = {
                "id": payload.get("sub"),
                "email": payload.get("email"),
                "roles": payload.get("roles", [])
            }
        except Exception:
            request.user = None
    else:
        request.user = None

    return next_handler(request)

def require_auth(request):
    if not hasattr(request, "user") or not request.user:
        raise UnauthorizedException("Authentication required to access this resource")

def require_roles(request, allowed_roles: list):
    require_auth(request)
    user_roles = set(request.user.get("roles", []))
    allowed_set = set([r.upper() for r in allowed_roles])

    # ADMIN has full access
    if "ADMIN" in user_roles:
        return True

    if not user_roles.intersection(allowed_set):
        raise ForbiddenException(f"Resource requires one of the following roles: {allowed_roles}")
    return True
