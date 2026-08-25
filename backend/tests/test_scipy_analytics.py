import unittest
from app.analytics.scipy_analytics import (
    perform_ab_test_ttest,
    optimize_optimal_price,
    optimize_economic_order_quantity,
    interpolate_missing_sales_data
)

class TestSciPyAnalytics(unittest.TestCase):

    def test_ab_test_ttest(self):
        sample_a = [100.0, 105.0, 98.0, 102.0, 110.0]
        sample_b = [150.0, 145.0, 160.0, 155.0, 152.0]

        res = perform_ab_test_ttest(sample_a, sample_b)
        self.assertTrue(res["is_significant"])
        self.assertLess(res["p_value"], 0.05)

    def test_price_optimization(self):
        res = optimize_optimal_price(base_price=100.0, elasticity_slope=0.5, max_demand=100.0)
        self.assertTrue(res["optimization_success"])
        self.assertGreater(res["optimal_price"], 0.0)
        self.assertGreater(res["projected_max_revenue"], 0.0)

    def test_economic_order_quantity(self):
        res = optimize_economic_order_quantity(annual_demand=1000, ordering_cost=50, holding_cost_per_unit=2)
        self.assertAlmostEqual(res["optimal_order_quantity"], 223.61, delta=1.0)

    def test_missing_sales_interpolation(self):
        x_known = [0, 2, 4]
        y_known = [100.0, 200.0, 300.0]
        x_target = [0, 1, 2, 3, 4]

        interpolated = interpolate_missing_sales_data(x_known, y_known, x_target)
        self.assertEqual(interpolated, [100.0, 150.0, 200.0, 250.0, 300.0])
