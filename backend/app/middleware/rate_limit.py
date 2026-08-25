import time
from app.config.settings import settings
from app.core.exceptions import RateLimitExceededException

class RateLimiter:

    def __init__(self, limit=120, window_seconds=60):
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests = {}

    def is_allowed(self, client_ip):
        now = time.time()
        client_requests = self.requests.get(client_ip, [])
        print(self.requests,"cr")
        # Filter requests older than window_seconds
        valid_requests = [ts for ts in client_requests if now - ts < self.window_seconds]
        if len(valid_requests) >= self.limit:
            return False

        valid_requests.append(now)
        self.requests[client_ip] = valid_requests
        return True

    def reset(self):
        self.requests.clear()

rate_limiter = RateLimiter(limit=settings.rate_limit_per_minute)

def rate_limit_middleware(request, next_handler):
    print("ratelimit")
    client_ip = request.headers.get("X-Forwarded-For", "127.0.0.1")
    if not rate_limiter.is_allowed(client_ip):
        raise RateLimitExceededException(

        )
    return next_handler(request)
