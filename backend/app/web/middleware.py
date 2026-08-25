class MiddlewareManager:
    def __init__(self):
        self.middlewares = []

    def add(self, middleware):
        self.middlewares.append(middleware)  

    def execute(self, request, handler):
        next_handler = handler

        for middleware in reversed(self.middlewares):
            current = middleware

            next_handler = (lambda request, current=current, 
                         next_handler=next_handler: current(request, next_handler))              
        return next_handler(request)