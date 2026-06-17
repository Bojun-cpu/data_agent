from typing import TypedDict, Optional, Any, List, Dict


class AgentState(TypedDict):
    user_question: str
    generated_sql: Optional[str]
    query_result: Optional[Any]
    final_answer: Optional[str]
    messages: List[Dict[str, str]]