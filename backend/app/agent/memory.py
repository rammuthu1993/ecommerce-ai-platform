from collections import defaultdict

class AgentMemory:

    def __init__(self, max_history_per_session: int = 10):
        self.max_history = max_history_per_session
        self.sessions = defaultdict(list)

    def add_turn(self, session_id: str, user_query: str, agent_response: str):
        if not session_id:
            return

        turn = {
            "query": user_query,
            "response": agent_response
        }
        self.sessions[session_id].append(turn)

        # Enforce sliding window boundary
        if len(self.sessions[session_id]) > self.max_history:
            self.sessions[session_id] = self.sessions[session_id][-self.max_history:]

    def get_history(self, session_id: str) -> list:
        return self.sessions.get(session_id, [])

    def clear_session(self, session_id: str) -> bool:
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

agent_memory = AgentMemory()
