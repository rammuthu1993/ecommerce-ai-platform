import time
import numpy as np

def calculate_sales_statistics(prices: list, quantities: list) -> dict:
    if not prices or not quantities or len(prices) != len(quantities):
        return {
            "count": 0,
            "total_revenue": 0.0,
            "mean_order_revenue": 0.0,
            "median_order_revenue": 0.0,
            "min_order_revenue": 0.0,
            "max_order_revenue": 0.0,
            "std_order_revenue": 0.0,
            "percentiles": {"p25": 0.0, "p50": 0.0, "p75": 0.0, "p90": 0.0}
        }

    prices_arr = np.array(prices, dtype=np.float64)
    quantities_arr = np.array(quantities, dtype=np.float64)

    # Vectorized item totals calculation
    line_totals = prices_arr * quantities_arr
    total_revenue = float(np.sum(line_totals))

    mean_rev = float(np.mean(line_totals))
    median_rev = float(np.median(line_totals))
    min_rev = float(np.min(line_totals))
    max_rev = float(np.max(line_totals))
    std_rev = float(np.std(line_totals))

    p25, p50, p75, p90 = np.percentile(line_totals, [25, 50, 75, 90])

    return {
        "count": int(len(line_totals)),
        "total_revenue": round(total_revenue, 2),
        "mean_order_revenue": round(mean_rev, 2),
        "median_order_revenue": round(median_rev, 2),
        "min_order_revenue": round(min_rev, 2),
        "max_order_revenue": round(max_rev, 2),
        "std_order_revenue": round(std_rev, 2),
        "percentiles": {
            "p25": round(float(p25), 2),
            "p50": round(float(p50), 2),
            "p75": round(float(p75), 2),
            "p90": round(float(p90), 2)
        }
    }

def benchmark_numpy_vs_python(num_items: int = 100000) -> dict:
    prices = list(range(1, num_items + 1))
    quantities = [2] * num_items

    # Pure Python loop time
    t0 = time.perf_counter()
    python_totals = [p * q for p, q in zip(prices, quantities)]
    python_sum = sum(python_totals)
    t1 = time.perf_counter()
    python_time = t1 - t0

    # NumPy vectorized operation time
    t2 = time.perf_counter()
    np_prices = np.array(prices, dtype=np.float64)
    np_quantities = np.array(quantities, dtype=np.float64)
    np_totals = np_prices * np_quantities
    np_sum = float(np.sum(np_totals))
    t3 = time.perf_counter()
    numpy_time = t3 - t2

    speedup = python_time / numpy_time if numpy_time > 0 else 1.0

    return {
        "num_items": num_items,
        "python_loop_seconds": round(python_time, 5),
        "numpy_vectorized_seconds": round(numpy_time, 5),
        "speedup_factor": round(speedup, 2)
    }
