from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    user_question: str
    intent: str
    metric_name: str
    time_range: str
    dimensions: list[str]
    filters: dict
    generated_sql: str
    query_result: Any
    final_answer: str
    messages: list[dict[str, str]]
    error: str
    trace_id: str
