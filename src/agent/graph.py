from langgraph.graph import END, StateGraph

from agent.nodes import (
    execute_sql_node,
    intent_node,
    response_node,
    sql_node,
    sql_security_node,
)
from agent.state import AgentState


builder = StateGraph(AgentState)

builder.add_node("intent", intent_node)
builder.add_node("sql", sql_node)
builder.add_node("sql_security", sql_security_node)
builder.add_node("execute_sql", execute_sql_node)
builder.add_node("response", response_node)

builder.set_entry_point("intent")

builder.add_edge("intent", "sql")
builder.add_edge("sql", "sql_security")
builder.add_edge("sql_security", "execute_sql")
builder.add_edge("execute_sql", "response")
builder.add_edge("response", END)

graph = builder.compile()


def run_question(question, previous_state=None):
    state = {
        **(previous_state or {}),
        "user_question": question,
        "generated_sql": "",
        "query_result": None,
        "final_answer": "",
        "error": "",
    }
    state.setdefault("messages", [])
    state.setdefault("dimensions", [])
    state.setdefault("filters", {})
    return graph.invoke(state)


if __name__ == "__main__":
    result1 = run_question("最近7天GMV是多少？")
    print("第一轮结果：")
    print(result1)

    result2 = run_question("上周呢？", result1)
    print("\n第二轮结果：")
    print(result2)

    result3 = run_question("按渠道拆一下？", result1)
    print("\n第三轮结果：")
    print(result3)

    result4 = run_question("删除订单表。", result1)
    print("\n安全拦截结果：")
    print(result4)
