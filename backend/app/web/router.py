class Router:
    def __init__(self):
        self.routes = []

    def add_route(self, method, path, handler):
        self.routes.append({"method": method, "path": path, "handler": handler})

    def find_route(self, method, path):
        for route in self.routes:
            if route["method"] != method:
                continue

            router_parts = route["path"].strip("/").split("/")
            path_parts = path.strip("/").split("/")

            if len(router_parts) != len(path_parts):
                continue
            params = {}
            matched = True
            for route_part, path_part in zip(router_parts, path_parts):
                if route_part.startswith("{") and route_part.endswith("}"):
                     param_name = route_part[1:-1]
                     params[param_name] = path_part

                elif route_part != path_part: 
                    matched = False
                    break

            if matched:
                return route["handler"], params

        return None, {}