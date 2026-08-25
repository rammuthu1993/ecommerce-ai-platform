import time
from collections import Counter

class AgentMetrics:

    def __init__(self):
        self.total_queries = 0
        self.tool_calls_counter = Counter()
        self.tool_failures_counter = Counter()
        self.tool_latencies = {}

    def record_query(self):
        self.total_queries += 1

    def record_tool_execution(self, tool_name: str, duration_sec: float, success: bool = True):
        self.tool_calls_counter[tool_name] += 1
        if not success:
            self.tool_failures_counter[tool_name] += 1

        if tool_name not in self.tool_latencies:
            self.tool_latencies[tool_name] = []
        self.tool_latencies[tool_name].append(round(duration_sec, 4))
        # Keep last 100 latency samples
        if len(self.tool_latencies[tool_name]) > 100:
            self.tool_latencies[tool_name] = self.tool_latencies[tool_name][-100:]

    def get_summary(self) -> dict:
        tool_stats = {}
        for tool_name, calls in self.tool_calls_counter.items():
            failures = self.tool_failures_counter.get(tool_name, 0)
            latencies = self.tool_latencies.get(tool_name, [0.0])
            avg_latency = sum(latencies) / len(latencies) if latencies else 0.0

            tool_stats[tool_name] = {
                "total_calls": calls,
                "failures": failures,
                "success_rate_pct": round(((calls - failures) / calls) * 100.0, 2) if calls > 0 else 100.0,
                "avg_latency_sec": round(avg_latency, 4)
            }

        return {
            "total_queries_processed": self.total_queries,
            "total_tool_executions": sum(self.tool_calls_counter.values()),
            "tools": tool_stats
        }

agent_metrics = AgentMetrics()
