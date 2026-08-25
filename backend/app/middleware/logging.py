import time

def logging_middleware(request, next_handler):
    print("logging")
    start_time = time.time()
    print(f"[REQUEST] {request.method, request.path}")
    response = next_handler(request)
    execution_time = (time.time() - start_time) * 1000
    print(f"[RESPONSE]", f"{response.status_code}", f"{execution_time:.2f}ms")
    return response

