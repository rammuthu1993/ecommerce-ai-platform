import unittest
from app.analytics.numpy_analytics import calculate_sales_statistics, benchmark_numpy_vs_python

class TestNumPyAnalytics(unittest.TestCase):

    def test_calculate_sales_statistics(self):
        prices = [100.0, 200.0, 50.0, 300.0, 150.0]
        quantities = [2, 1, 4, 1, 2]

        stats = calculate_sales_statistics(prices, quantities)
        self.assertEqual(stats["count"], 5)
        # Line totals: [200, 200, 200, 300, 300] => sum = 1200
        self.assertEqual(stats["total_revenue"], 1200.0)
        self.assertEqual(stats["mean_order_revenue"], 240.0)
        self.assertEqual(stats["min_order_revenue"], 200.0)
        self.assertEqual(stats["max_order_revenue"], 300.0)
        self.assertIn("p50", stats["percentiles"])

    def test_empty_sales_statistics(self):
        stats = calculate_sales_statistics([], [])
        self.assertEqual(stats["count"], 0)
        self.assertEqual(stats["total_revenue"], 0.0)

    def test_benchmark_numpy_vs_python(self):
        res = benchmark_numpy_vs_python(num_items=1000)
        self.assertEqual(res["num_items"], 1000)
        self.assertIn("speedup_factor", res)
