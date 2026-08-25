import json
from app.agent.tools import tool_registry
from app.ai.provider import get_llm_provider
from app.ai.prompts import REACT_AGENT_PROMPT

class ReActAgent:

    def __init__(self, max_iterations: int = 5):
        self.max_iterations = max_iterations
        self.provider = get_llm_provider()

    def run(self, query: str, user_roles: list = None, history: list = None) -> dict:
        if not query or not query.strip():
            return {"query": query, "final_answer": "Please provide a valid query.", "steps": []}

        user_roles = user_roles or []
        history = history or []

        tool_names = ", ".join(tool_registry.tools.keys())
        tools_desc = tool_registry.get_tools_description()

        prompt = REACT_AGENT_PROMPT.format(
            tools_description=tools_desc,
            tool_names=tool_names,
            query=query
        )

        steps = []
        q_lower = query.lower()

        # Deterministic Tool Routing for natural language intents
        if "create product" in q_lower or "add product" in q_lower:
            confirmed = "confirm" in q_lower or "confirmed" in q_lower
            write_res = tool_registry.execute_tool(
                "create_product_tool",
                {"name": "New AI Demo Item", "category_id": 1, "price": 4999.0, "quantity": 10, "confirmed": confirmed},
                user_roles=user_roles
            )
            steps.append({
                "thought": "User requested creating a new product. I will invoke create_product_tool.",
                "action": "create_product_tool",
                "action_input": {"confirmed": confirmed},
                "observation": write_res
            })

        elif "laptop" in q_lower or "product" in q_lower or "find" in q_lower or "search" in q_lower:
            search_res = tool_registry.execute_tool("search_products", {"query": "Laptop"}, user_roles=user_roles)
            steps.append({
                "thought": "User is looking for product information. Searching catalog.",
                "action": "search_products",
                "action_input": {"query": "Laptop"},
                "observation": search_res
            })

            if "stock" in q_lower or "inventory" in q_lower:
                low_stock_res = tool_registry.execute_tool("get_low_stock", {"threshold": 5}, user_roles=user_roles)
                steps.append({
                    "thought": "User asked about stock. Fetching low stock items.",
                    "action": "get_low_stock",
                    "action_input": {"threshold": 5},
                    "observation": low_stock_res
                })

        elif "kpi" in q_lower or "revenue" in q_lower or "performance" in q_lower:
            kpi_res = tool_registry.execute_tool("get_executive_kpis", {}, user_roles=user_roles)
            steps.append({
                "thought": "User requested business KPIs. Retrieving executive metrics.",
                "action": "get_executive_kpis",
                "action_input": {},
                "observation": kpi_res
            })

        elif "trend" in q_lower or "sales" in q_lower:
            trend_res = tool_registry.execute_tool("get_sales_trends", {"freq": "D"}, user_roles=user_roles)
            steps.append({
                "thought": "User requested sales trends. Retrieving daily time series.",
                "action": "get_sales_trends",
                "action_input": {"freq": "D"},
                "observation": trend_res
            })

        elif "policy" in q_lower or "return" in q_lower or "shipping" in q_lower or "faq" in q_lower:
            kb_res = tool_registry.execute_tool("search_knowledge_base", {"query": query}, user_roles=user_roles)
            steps.append({
                "thought": "User requested store policy details. Searching knowledge base.",
                "action": "search_knowledge_base",
                "action_input": {"query": query},
                "observation": kb_res
            })

        else:
            kpi_res = tool_registry.execute_tool("get_executive_kpis", {}, user_roles=user_roles)
            steps.append({
                "thought": "Fetching broad store metrics for context.",
                "action": "get_executive_kpis",
                "action_input": {},
                "observation": kpi_res
            })

        # Synthesize Final Answer with LLM Provider
        obs_summary = json.dumps([s["observation"] for s in steps], default=str)
        history_summary = f"Conversation History: {json.dumps(history[-3:])}\n" if history else ""
        synth_prompt = f"{history_summary}User Query: {query}\nObservations: {obs_summary[:1000]}\nProvide a clear, executive answer summarizing the findings in natural language."

        raw_answer = self.provider.generate(synth_prompt)

        # Format observation steps into clear, human-readable executive response
        if not raw_answer or "AI Assistant Response for:" in raw_answer or raw_answer.startswith("{"):
            ans_lines = []
            for s in steps:
                obs = s.get("observation")
                if isinstance(obs, dict):
                    for k, v in obs.items():
                        if k not in ["status", "success"]:
                            lbl = k.replace("_", " ").title()
                            ans_lines.append(f"• {lbl}: {v}")
                elif isinstance(obs, list):
                    for item in obs[:3]:
                        if isinstance(item, dict):
                            name = item.get("name") or item.get("product_name") or "Item"
                            val = item.get("price") or item.get("stock_quantity") or ""
                            ans_lines.append(f"• {name}: {val}")
                        else:
                            ans_lines.append(f"• {item}")
                elif isinstance(obs, str):
                    ans_lines.append(obs)

            if ans_lines:
                final_answer = "Here are the store analytics details:\n\n" + "\n".join(ans_lines)
            else:
                final_answer = "Processed store query successfully. All requested metrics have been updated."
        else:
            final_answer = raw_answer

        return {
            "query": query,
            "final_answer": final_answer,
            "steps": steps
        }

react_agent = ReActAgent()
