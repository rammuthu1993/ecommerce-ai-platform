import numpy as np
from scipy import stats, optimize, interpolate

def perform_ab_test_ttest(sample_a: list, sample_b: list) -> dict:
    """
    Performs a two-sample Independent T-Test (scipy.stats.ttest_ind) to determine
    if price or conversion differences between Group A and Group B are statistically significant.
    """
    if not sample_a or not sample_b or len(sample_a) < 2 or len(sample_b) < 2:
        return {
            "statistic": 0.0,
            "p_value": 1.0,
            "is_significant": False,
            "mean_a": round(float(np.mean(sample_a)), 2) if sample_a else 0.0,
            "mean_b": round(float(np.mean(sample_b)), 2) if sample_b else 0.0
        }

    arr_a = np.array(sample_a, dtype=np.float64)
    arr_b = np.array(sample_b, dtype=np.float64)

    t_stat, p_val = stats.ttest_ind(arr_a, arr_b, equal_var=False)

    return {
        "statistic": round(float(t_stat), 4),
        "p_value": round(float(p_val), 5),
        "is_significant": bool(p_val < 0.05),
        "mean_a": round(float(np.mean(arr_a)), 2),
        "mean_b": round(float(np.mean(arr_b)), 2)
    }

def optimize_optimal_price(base_price: float, elasticity_slope: float = 0.5, max_demand: float = 100.0) -> dict:
    """
    Uses scipy.optimize.minimize to find the optimal product price that maximizes total revenue.
    Demand model: Demand(P) = max_demand - elasticity_slope * P
    Revenue(P) = P * Demand(P) = P * (max_demand - elasticity_slope * P)
    Objective: Minimize -Revenue(P)
    """
    def negative_revenue(price):
        p = price[0]
        demand = max(0.0, max_demand - elasticity_slope * p)
        return -(p * demand)

    initial_guess = [base_price]
    bounds = [(1.0, max_demand / elasticity_slope)]

    res = optimize.minimize(negative_revenue, initial_guess, bounds=bounds, method="L-BFGS-B")

    optimal_price = float(res.x[0]) if res.success else base_price
    optimal_demand = max(0.0, max_demand - elasticity_slope * optimal_price)
    max_revenue = optimal_price * optimal_demand

    return {
        "base_price": round(base_price, 2),
        "optimal_price": round(optimal_price, 2),
        "expected_demand": round(optimal_demand, 2),
        "projected_max_revenue": round(max_revenue, 2),
        "optimization_success": bool(res.success)
    }

def optimize_economic_order_quantity(annual_demand: float, ordering_cost: float, holding_cost_per_unit: float) -> dict:
    """
    Economic Order Quantity (EOQ) optimization using scipy.optimize.minimize.
    Total Cost(Q) = (D / Q) * S + (Q / 2) * H
    """
    if annual_demand <= 0 or ordering_cost <= 0 or holding_cost_per_unit <= 0:
        return {"eoq": 0.0, "total_cost": 0.0}

    def total_inventory_cost(q_vec):
        q = q_vec[0]
        if q <= 0:
            return 1e9
        return (annual_demand / q) * ordering_cost + (q / 2.0) * holding_cost_per_unit

    initial_q = [np.sqrt(2 * annual_demand * ordering_cost / holding_cost_per_unit)]
    res = optimize.minimize(total_inventory_cost, initial_q, bounds=[(1.0, None)], method="L-BFGS-B")

    eoq = float(res.x[0])
    total_cost = float(res.fun)

    return {
        "annual_demand": annual_demand,
        "ordering_cost": ordering_cost,
        "holding_cost_per_unit": holding_cost_per_unit,
        "optimal_order_quantity": round(eoq, 2),
        "minimized_annual_cost": round(total_cost, 2)
    }

def interpolate_missing_sales_data(x_known: list, y_known: list, x_target: list) -> list:
    """
    Uses scipy.interpolate.interp1d to fill gaps or estimate missing metric values in time series data.
    """
    if not x_known or not y_known or len(x_known) < 2:
        return y_known

    f = interpolate.interp1d(x_known, y_known, kind="linear", fill_value="extrapolate")
    y_target = f(x_target)
    return [round(float(val), 2) for val in y_target]
