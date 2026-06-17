from tools.sql_tool import generate_sql


def intent_node(state):
    """Keep the original user question for the following nodes."""
    return state


def sql_node(state):
    question = state["user_question"]
    messages = state.get("messages", [])

    sql = generate_sql(question, messages)

    return {
        **state,
        "generated_sql": sql,
    }


def execute_sql_node(state):
    """Execute SQL with mocked results for the current demo."""
    sql = state.get("generated_sql") or ""
    sql_lower = sql.lower()

    if "current_week" in sql_lower and "last_week" in sql_lower:
        result = {
            "current_week": 125430,
            "last_week": 118200,
        }
    elif "sum(order_amount)" in sql_lower or "recent_7_days_gmv" in sql_lower:
        result = {
            "gmv": 125430,
        }
    else:
        result = {
            "error": sql,
        }

    return {
        **state,
        "query_result": result,
    }


def response_node(state):
    result = state.get("query_result")

    if isinstance(result, dict) and "current_week" in result and "last_week" in result:
        growth = round(
            (result["current_week"] - result["last_week"])
            / result["last_week"]
            * 100,
            2,
        )
        answer = (
            f"本周GMV为{result['current_week']}元，"
            f"上周GMV为{result['last_week']}元，"
            f"增长{growth:.2f}%。"
        )
    elif isinstance(result, dict) and "gmv" in result:
        answer = f"最近7天GMV为{result['gmv']}元。"
    else:
        answer = "暂时无法回答该问题。"

    messages = list(state.get("messages", []))
    messages.append({"role": "user", "content": state["user_question"]})
    messages.append({"role": "assistant", "content": answer})

    return {
        **state,
        "final_answer": answer,
        "messages": messages,
    }
