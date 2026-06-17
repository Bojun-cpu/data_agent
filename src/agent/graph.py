from langgraph.graph import END, StateGraph

from agent.nodes import (
    execute_sql_node,
    intent_node,
    response_node,
    sql_node,
)
from agent.state import AgentState


builder = StateGraph(AgentState)

builder.add_node("intent", intent_node)
builder.add_node("sql", sql_node)
builder.add_node("execute_sql", execute_sql_node)
builder.add_node("response", response_node)

builder.set_entry_point("intent")

builder.add_edge("intent", "sql")
builder.add_edge("sql", "execute_sql")
builder.add_edge("execute_sql", "response")
builder.add_edge("response", END)

graph = builder.compile()


if __name__ == "__main__":
    state = {
        "user_question": "最近7天GMV是多少？",
        "generated_sql": None,
        "query_result": None,
        "final_answer": None,
        "messages": [],
    }

    result1 = graph.invoke(state)
    print("第一轮结果：")
    print(result1)

    state2 = {
        **result1,
        "user_question": "那和上周相比呢？",
        "generated_sql": None,
        "query_result": None,
        "final_answer": None,
    }

    result2 = graph.invoke(state2)
    print("\n第二轮结果：")
    print(result2)
