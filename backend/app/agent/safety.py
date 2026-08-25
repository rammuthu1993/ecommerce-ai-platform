import re
from app.core.exceptions import ForbiddenException

PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+previous\s+instructions",
    r"disregard\s+all\s+prior",
    r"forget\s+all\s+rules",
    r"you\s+are\s+now\s+dan",
    r"override\s+system\s+prompt"
]

SENSITIVE_PATTERNS = [
    (r'"password":\s*"[^"]+"', '"password": "[REDACTED]"'),
    (r'"salt":\s*"[^"]+"', '"salt": "[REDACTED]"'),
    (r'"secret":\s*"[^"]+"', '"secret": "[REDACTED]"'),
    (r'"token":\s*"[^"]+"', '"token": "[REDACTED]"'),
    (r'\b(?:\d[ -]*?){13,16}\b', '[REDACTED_CARD]')
]

READ_ONLY_TOOLS = {
    "search_products", "check_inventory", "get_low_stock",
    "get_top_selling_products", "get_sales_trends",
    "get_executive_kpis", "search_knowledge_base"
}

WRITE_MUTATION_TOOLS = {
    "create_product_tool", "update_product_tool",
    "create_purchase_tool", "adjust_inventory_tool"
}


def sanitize_input(prompt: str) -> str:
    if not prompt or not isinstance(prompt, str):
        return ""

    cleaned = prompt
    for pattern in PROMPT_INJECTION_PATTERNS:
        cleaned = re.sub(pattern, "[FILTERED_INJECTION]", cleaned, flags=re.IGNORECASE)
    return cleaned


def redact_sensitive_data(text: str) -> str:
    if not text or not isinstance(text, str):
        return text

    redacted = text
    for pattern, replacement in SENSITIVE_PATTERNS:
        redacted = re.sub(pattern, replacement, redacted, flags=re.IGNORECASE)
    return redacted


def validate_tool_permissions(tool_name: str, user_roles: list = None) -> bool:
    user_roles = user_roles or []

    if tool_name in WRITE_MUTATION_TOOLS:
        allowed = any(role.upper() in ["ADMIN", "MANAGER"] for role in user_roles)
        if not allowed:
            raise ForbiddenException(f"Role unauthorized to execute write tool '{tool_name}'")
    return True
