import json
import re
from app.core.exceptions import AppException

def parse_structured_json(text: str) -> dict:
    if not text or not isinstance(text, str):
        raise AppException("Input text is empty", 400, "INVALID_AI_RESPONSE")

    cleaned = text.strip()

    # Regex extract ```json ... ``` or ``` ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned, re.IGNORECASE)
    if match:
        cleaned = match.group(1).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback: Find first '{' and last '}'
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(cleaned[start:end+1])
            except json.JSONDecodeError:
                pass

        raise AppException("Failed to parse structured JSON response from AI model", 400, "INVALID_AI_RESPONSE")
