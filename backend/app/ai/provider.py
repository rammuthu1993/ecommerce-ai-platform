import os
import json
import urllib.request
from app.ai.token_tracker import token_tracker
from app.ai.prompts import SYSTEM_ASSISTANT_PROMPT
from app.core.exceptions import AppException

class BaseLLMProvider:

    def generate(self, prompt: str, system_instruction: str = None) -> str:
        raise NotImplementedError

    def generate_json(self, prompt: str, schema: dict = None) -> dict:
        raise NotImplementedError


class MockLLMProvider(BaseLLMProvider):
    """
    Deterministic Mock LLM Provider for offline resilience and unit testing.
    """

    def generate(self, prompt: str, system_instruction: str = None) -> str:
        prompt_tokens = len(prompt.split()) + 10
        response_text = f"AI Assistant Response for: {prompt[:80]}..."
        completion_tokens = len(response_text.split())

        token_tracker.record_usage(prompt_tokens, completion_tokens)
        return response_text

    def generate_json(self, prompt: str, schema: dict = None) -> dict:
        prompt_tokens = len(prompt.split()) + 15
        mock_data = {
            "query": prompt,
            "status": "success",
            "message": "Processed successfully by AI Model Provider"
        }
        completion_tokens = 20
        token_tracker.record_usage(prompt_tokens, completion_tokens)
        return mock_data


class GeminiLLMProvider(BaseLLMProvider):
    """
    Gemini API Provider.
    """

    def __init__(self, api_key: str = None, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name

    def generate(self, prompt: str, system_instruction: str = None) -> str:
        if not self.api_key:
            # Fallback to MockLLMProvider if no API key is configured
            return MockLLMProvider().generate(prompt, system_instruction)

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"

        contents = []
        if system_instruction:
            contents.append({"role": "user", "parts": [{"text": f"System Instruction: {system_instruction}"}]})
            contents.append({"role": "model", "parts": [{"text": "Understood."}]})

        contents.append({"role": "user", "parts": [{"text": prompt}]})

        payload = {"contents": contents}
        data = json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req) as resp:
                res_body = json.loads(resp.read().decode("utf-8"))
                candidates = res_body.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    text = "".join(p.get("text", "") for p in parts)
                    prompt_tokens = len(prompt.split()) + 10
                    completion_tokens = len(text.split())
                    token_tracker.record_usage(prompt_tokens, completion_tokens)
                    return text
                raise AppException("Gemini API returned empty response", 500, "AI_PROVIDER_ERROR")
        except Exception as e:
            # Fallback to mock on network error
            return MockLLMProvider().generate(prompt, system_instruction)

    def generate_json(self, prompt: str, schema: dict = None) -> dict:
        text_resp = self.generate(prompt + "\nReturn response strictly formatted as valid JSON.")
        from app.ai.structured_parser import parse_structured_json
        return parse_structured_json(text_resp)


def get_llm_provider() -> BaseLLMProvider:
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return GeminiLLMProvider(api_key=api_key)
    return MockLLMProvider()
