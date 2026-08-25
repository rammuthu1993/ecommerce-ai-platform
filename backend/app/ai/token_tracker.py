import time

class TokenTracker:

    def __init__(self, cost_per_1k_input: float = 0.0005, cost_per_1k_output: float = 0.0015):
        self.cost_per_1k_input = cost_per_1k_input
        self.cost_per_1k_output = cost_per_1k_output
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_calls = 0

    def record_usage(self, prompt_tokens: int, completion_tokens: int):
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        self.total_calls += 1

    def get_summary(self) -> dict:
        total_tokens = self.total_prompt_tokens + self.total_completion_tokens
        input_cost = (self.total_prompt_tokens / 1000.0) * self.cost_per_1k_input
        output_cost = (self.total_completion_tokens / 1000.0) * self.cost_per_1k_output
        total_cost = input_cost + output_cost

        return {
            "total_calls": self.total_calls,
            "prompt_tokens": self.total_prompt_tokens,
            "completion_tokens": self.total_completion_tokens,
            "total_tokens": total_tokens,
            "estimated_cost_usd": round(total_cost, 6)
        }

    def reset(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_calls = 0

token_tracker = TokenTracker()
