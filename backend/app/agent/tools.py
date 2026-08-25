import json
import time
from app.products.service import get_products, get_product, create_product, update_product
from app.inventory.service import get_all_inventory, get_low_stock, adjust_stock
from app.purchases.service import create_purchase
from app.reporting.service import get_top_products_report
from app.analytics.pandas_analytics import get_sales_time_series
from app.analytics.kpi_service import get_executive_kpis
from app.rag.vector_store import vector_store
from app.agent.safety import validate_tool_permissions
from app.agent.metrics import agent_metrics
from app.audit.service import log_audit


class ToolRegistry:

    def __init__(self):
        self.tools = {}
        self._register_default_tools()

    def register_tool(self, name: str, description: str, parameters: dict, func, is_mutation: bool = False):
        self.tools[name] = {
            "name": name,
            "description": description,
            "parameters": parameters,
            "func": func,
            "is_mutation": is_mutation
        }

    def _register_default_tools(self):
        # --- READ-ONLY TOOLS ---
        self.register_tool(
            name="search_products",
            description="Search products by query keyword, category, or price range.",
            parameters={"query": "string", "min_price": "float", "max_price": "float"},
            func=lambda kwargs: get_products(
                search=kwargs.get("query"),
                min_price=float(kwargs["min_price"]) if kwargs.get("min_price") is not None else None,
                max_price=float(kwargs["max_price"]) if kwargs.get("max_price") is not None else None
            )["products"]
        )

        self.register_tool(
            name="check_inventory",
            description="Check inventory stock details for a specific product ID.",
            parameters={"product_id": "int"},
            func=lambda kwargs: get_product(int(kwargs["product_id"]))
        )

        self.register_tool(
            name="get_low_stock",
            description="Get products with stock below threshold level.",
            parameters={"threshold": "int"},
            func=lambda kwargs: get_low_stock(threshold=int(kwargs.get("threshold", 5)))
        )

        self.register_tool(
            name="get_top_selling_products",
            description="Get top selling products by revenue.",
            parameters={"limit": "int"},
            func=lambda kwargs: get_top_products_report(limit=int(kwargs.get("limit", 5)))
        )

        self.register_tool(
            name="get_sales_trends",
            description="Get sales trends aggregated by daily (D) or monthly (M) frequency.",
            parameters={"freq": "string"},
            func=lambda kwargs: get_sales_time_series(freq=kwargs.get("freq", "D"))
        )

        self.register_tool(
            name="get_executive_kpis",
            description="Get overall business executive KPIs (Revenue, AOV, Gross Profit, Units Sold).",
            parameters={},
            func=lambda kwargs: get_executive_kpis()
        )

        self.register_tool(
            name="search_knowledge_base",
            description="Search e-commerce store policies, FAQs, and documentation.",
            parameters={"query": "string"},
            func=lambda kwargs: vector_store.search(kwargs.get("query", ""), top_k=2)
        )

        # --- CONTROLLED WRITE MUTATION TOOLS ---
        self.register_tool(
            name="create_product_tool",
            description="Create a new product in store catalog. Requires explicit confirmation (confirmed=true).",
            parameters={"name": "string", "category_id": "int", "price": "float", "quantity": "int", "confirmed": "bool"},
            func=self._controlled_create_product,
            is_mutation=True
        )

        self.register_tool(
            name="update_product_tool",
            description="Update an existing product. Requires explicit confirmation (confirmed=true).",
            parameters={"product_id": "int", "name": "string", "price": "float", "confirmed": "bool"},
            func=self._controlled_update_product,
            is_mutation=True
        )

        self.register_tool(
            name="create_purchase_tool",
            description="Create a purchase order with a supplier. Requires explicit confirmation (confirmed=true).",
            parameters={"supplier_id": "int", "items": "list", "confirmed": "bool"},
            func=self._controlled_create_purchase,
            is_mutation=True
        )

        self.register_tool(
            name="adjust_inventory_tool",
            description="Adjust product inventory stock. Requires explicit confirmation (confirmed=true).",
            parameters={"product_id": "int", "quantity_delta": "int", "confirmed": "bool"},
            func=self._controlled_adjust_inventory,
            is_mutation=True
        )

    # Controlled Mutation Handlers
    def _controlled_create_product(self, kwargs: dict):
        if not kwargs.get("confirmed"):
            return {
                "requires_confirmation": True,
                "tool": "create_product_tool",
                "details": kwargs,
                "message": "Creating a product will modify store catalog records. Please set confirmed=true to proceed."
            }

        payload = {
            "name": kwargs["name"],
            "category_id": int(kwargs["category_id"]),
            "price": float(kwargs["price"]),
            "quantity": int(kwargs.get("quantity", 0))
        }
        res = create_product(payload)
        log_audit("CREATE", "PRODUCTS", "PRODUCT", entity_id=res["id"], details=f"Agent created product {res['name']}")
        return res

    def _controlled_update_product(self, kwargs: dict):
        if not kwargs.get("confirmed"):
            return {
                "requires_confirmation": True,
                "tool": "update_product_tool",
                "details": kwargs,
                "message": "Updating a product will modify store catalog records. Please set confirmed=true to proceed."
            }

        p_id = int(kwargs["product_id"])
        existing = get_product(p_id)
        payload = {
            "name": kwargs.get("name", existing["name"]),
            "category_id": existing["category_id"],
            "price": float(kwargs.get("price", existing["price"])),
            "quantity": existing.get("quantity", 0)
        }
        res = update_product(p_id, payload)
        log_audit("UPDATE", "PRODUCTS", "PRODUCT", entity_id=p_id, details=f"Agent updated product {p_id}")
        return res

    def _controlled_create_purchase(self, kwargs: dict):
        if not kwargs.get("confirmed"):
            return {
                "requires_confirmation": True,
                "tool": "create_purchase_tool",
                "details": kwargs,
                "message": "Creating a purchase order will commit a purchase transaction. Please set confirmed=true to proceed."
            }

        po = create_purchase(supplier_id=int(kwargs["supplier_id"]), items=kwargs["items"])
        log_audit("CREATE", "PURCHASES", "PURCHASE_ORDER", entity_id=po["id"], details=f"Agent created PO {po['id']}")
        return po

    def _controlled_adjust_inventory(self, kwargs: dict):
        if not kwargs.get("confirmed"):
            return {
                "requires_confirmation": True,
                "tool": "adjust_inventory_tool",
                "details": kwargs,
                "message": "Adjusting inventory will modify stock levels. Please set confirmed=true to proceed."
            }

        p_id = int(kwargs["product_id"])
        q_delta = int(kwargs["quantity_delta"])
        res = adjust_stock(p_id, q_delta, tx_type="ADJUSTMENT")
        log_audit("ADJUST", "INVENTORY", "PRODUCT", entity_id=p_id, details=f"Agent adjusted stock by {q_delta}")
        return res

    def execute_tool(self, name: str, arguments: dict, user_roles: list = None):
        if name not in self.tools:
            return {"error": f"Tool '{name}' is not registered."}

        # Validate Permissions
        validate_tool_permissions(name, user_roles=user_roles)

        tool = self.tools[name]
        t0 = time.perf_counter()
        success = True
        try:
            res = tool["func"](arguments)
            return res
        except Exception as e:
            success = False
            return {"error": f"Error executing tool '{name}': {str(e)}"}
        finally:
            t1 = time.perf_counter()
            agent_metrics.record_tool_execution(name, duration_sec=(t1 - t0), success=success)

    def get_tools_description(self) -> str:
        desc_lines = []
        for t_name, t_info in self.tools.items():
            desc_lines.append(f"- {t_name}: {t_info['description']} Parameters: {json.dumps(t_info['parameters'])}")
        return "\n".join(desc_lines)


tool_registry = ToolRegistry()
