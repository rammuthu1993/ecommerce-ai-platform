from app.agent.react_agent import react_agent
from app.agent.safety import sanitize_input, redact_sensitive_data
from app.agent.memory import agent_memory
from app.agent.metrics import agent_metrics
from app.audit.service import log_audit

def run_business_agent(query: str, user_id: int = None, user_roles: list = None, session_id: str = None) -> dict:
    agent_metrics.record_query()

    # Step 1: Prompt Safety & Injection Filter
    sanitized_query = sanitize_input(query)

    # Step 2: Fetch Multi-turn Conversation Memory if session_id provided
    history = agent_memory.get_history(session_id) if session_id else []

    # Step 3: Run ReAct Agent Reasoning Loop
    result = react_agent.run(sanitized_query, user_roles=user_roles, history=history)

    # Step 4: Redact Sensitive Output Data
    redacted_answer = redact_sensitive_data(result.get("final_answer", ""))
    result["final_answer"] = redacted_answer

    # Step 5: Save Turn in Session Memory
    if session_id:
        agent_memory.add_turn(session_id, sanitized_query, redacted_answer)

    # Step 6: Log Execution Audit Trail
    step_actions = [s["action"] for s in result.get("steps", [])]
    log_audit(
        action="AGENT_EXECUTE",
        module="AI_AGENT",
        entity="QUERY",
        entity_id=user_id or 0,
        details=f"Agent processed query: '{sanitized_query[:50]}...' Executed tools: {step_actions}"
    )

    return result
