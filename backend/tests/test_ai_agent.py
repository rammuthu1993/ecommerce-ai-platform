import os
import unittest

from app.config.settings import settings
from app.database.connection import initialize_database
from app.agent.tools import tool_registry
from app.agent.react_agent import ReActAgent
from app.agent.agent_service import run_business_agent


class TestAIAgent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        settings.database = "test_ecommerce.db"
        initialize_database()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("test_ecommerce.db"):
            try:
                os.remove("test_ecommerce.db")
            except OSError:
                pass

    def test_tool_registry_execution(self):
        tools = tool_registry.tools
        self.assertIn("search_products", tools)
        self.assertIn("get_executive_kpis", tools)

        kpis = tool_registry.execute_tool("get_executive_kpis", {})
        self.assertIn("total_revenue", kpis)

    def test_react_agent_execution_loop(self):
        agent = ReActAgent()
        res = agent.run("Find laptops and check inventory stock")

        self.assertIsNotNone(res["final_answer"])
        self.assertGreater(len(res["steps"]), 0)
        self.assertEqual(res["steps"][0]["action"], "search_products")

    def test_agent_service_audit_logging(self):
        res = run_business_agent("Explain our sales trends", user_id=1)
        self.assertIsNotNone(res["final_answer"])
        self.assertGreater(len(res["steps"]), 0)
