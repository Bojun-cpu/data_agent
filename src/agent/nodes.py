from tools.sql_security import validate_sql, validate_user_question
from tools.sql_tool import generate_sql


def _history_text(messages):
    return " ".join(
        str(message.get("content", ""))
        for message in messages
        if isinstance(message, dict)
    )


def _infer_metric_from_history(messages):
    history = _history_text(messages).lower()
    if "gmv" in history:
        return "gmv"
    if "订单量" in history or "订单数" in history or "order_count" in history:
        return "order_count"
    if "客单价" in history or "aov" in history:
        return "aov"
    if "退款率" in history or "refund_rate" in history:
        return "refund_rate"
    return ""


def intent_node(state):
    question = state.get("user_question", "")
    messages = state.get("messages", [])

    question_error = validate_user_question(question)
    if question_error:
        return {
            **state,
            "intent": "blocked",
            "error": question_error,
        }

    normalized_question = question.lower()

    metric_name = state.get("metric_name") or _infer_metric_from_history(messages)
    if "gmv" in normalized_question:
        metric_name = "gmv"
    elif "订单量" in question or "订单数" in question or "order_count" in normalized_question:
        metric_name = "order_count"
    elif "客单价" in question or "aov" in normalized_question:
        metric_name = "aov"
    elif "退款率" in question or "refund_rate" in normalized_question:
        metric_name = "refund_rate"

    time_range = state.get("time_range", "")
    if "最近7天" in question or "近7天" in question or "last 7" in normalized_question:
        time_range = "last_7_days"
    elif "上周" in question or "last week" in normalized_question:
        time_range = "last_week"
    elif "本周" in question or "this week" in normalized_question:
        time_range = "this_week"

    dimensions = list(state.get("dimensions", []))
    if "渠道" in question or "channel" in normalized_question:
        dimensions = ["channel"]
    elif "商品" in question or "product" in normalized_question:
        dimensions = ["product"]
    elif "品类" in question or "category" in normalized_question:
        dimensions = ["category"]

    intent = "data_query" if metric_name else "unknown"

    return {
        **state,
        "intent": intent,
        "metric_name": metric_name,
        "time_range": time_range,
        "dimensions": dimensions,
    }


def sql_node(state):
    if state.get("error"):
        return state

    question = state["user_question"]
    messages = state.get("messages", [])

    sql = generate_sql(question, messages, state)

    return {
        **state,
        "generated_sql": sql,
    }


def sql_security_node(state):
    if state.get("error"):
        return state

    sql_error = validate_sql(state.get("generated_sql", ""))
    if sql_error:
        return {
            **state,
            "error": sql_error,
        }

    return state


def execute_sql_node(state):
    """Execute SQL with mocked results for the Week2 prototype."""
    if state.get("error"):
        return {
            **state,
            "query_result": None,
        }

    sql = state.get("generated_sql") or ""
    sql_lower = sql.lower()

    if "group by channel" in sql_lower:
        result = {
            "channels": [
                {"channel": "app", "gmv": 62300},
                {"channel": "web", "gmv": 41120},
                {"channel": "mini_program", "gmv": 22010},
            ]
        }
    elif "current_week" in sql_lower and "last_week" in sql_lower:
        result = {
            "current_week": 125430,
            "last_week": 118200,
        }
    elif "sum(order_amount)" in sql_lower or "sum(total_amount)" in sql_lower:
        result = {
            "gmv": 125430,
        }
    elif "count(" in sql_lower:
        result = {
            "order_count": 3200,
        }
    else:
        result = {
            "error": "当前问题暂不支持。"
        }

    return {
        **state,
        "query_result": result,
    }


def response_node(state):
    if state.get("error"):
        answer = state["error"]
    else:
        result = state.get("query_result")

        if isinstance(result, dict) and "channels" in result:
            channel_text = "，".join(
                f"{item['channel']} {item['gmv']}元"
                for item in result["channels"]
            )
            answer = f"最近7天GMV按渠道拆分为：{channel_text}。"
        elif isinstance(result, dict) and "current_week" in result and "last_week" in result:
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
        elif isinstance(result, dict) and "order_count" in result:
            answer = f"订单量为{result['order_count']}单。"
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
