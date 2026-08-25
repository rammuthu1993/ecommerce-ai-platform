import os
import unittest

from app.config.settings import settings
from app.database.connection import initialize_database, get_connection
from app.web.request import Request
from app.web.server import (
    analytics_kpis_handler,
    analytics_sales_trend_handler,
    analytics_groupby_handler,
    analytics_rfm_handler,
    analytics_numpy_benchmark_handler,
    analytics_demand_optimization_handler,
    analytics_export_handler
)


class TestAnalyticsAPI(unittest.TestCase):

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

    def test_kpis_handler(self):
        req = Request(method="GET", path="/api/analytics/kpis")
        resp = analytics_kpis_handler(req)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("total_revenue", resp.body["data"])

    def test_sales_trend_handler(self):
        req = Request(method="GET", path="/api/analytics/sales-trend?freq=D")
        resp = analytics_sales_trend_handler(req)
        self.assertEqual(resp.status_code, 200)

    def test_groupby_handler(self):
        req = Request(method="GET", path="/api/analytics/groupby?by=category")
        resp = analytics_groupby_handler(req)
        self.assertEqual(resp.status_code, 200)

    def test_rfm_handler(self):
        req = Request(method="GET", path="/api/analytics/rfm-segmentation")
        resp = analytics_rfm_handler(req)
        self.assertEqual(resp.status_code, 200)

    def test_demand_optimization_handler(self):
        req = Request(method="GET", path="/api/analytics/demand-optimization?base_price=500")
        resp = analytics_demand_optimization_handler(req)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("optimal_price", resp.body["data"])

    def test_export_handler_csv(self):
        req = Request(method="GET", path="/api/analytics/export?dataset=sales&format=csv")
        resp = analytics_export_handler(req)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers["Content-Type"], "text/csv")
        self.assertIn("attachment", resp.headers["Content-Disposition"])
