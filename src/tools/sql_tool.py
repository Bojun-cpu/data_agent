from tools.sql_security import validate_user_question


def _history_text(messages):
    return " ".join(
        str(message.get("content", ""))
        for message in messages
        if isinstance(message, dict)
    )


def _infer_metric(question, messages, state):
    normalized_question = question.lower()

    if state and state.get("metric_name"):
        return state["metric_name"]
    if "gmv" in normalized_question:
        return "gmv"
    if "订单量" in question or "订单数" in question or "order_count" in normalized_question:
        return "order_count"
    if "客单价" in question or "aov" in normalized_question:
        return "aov"
    if "退款率" in question or "refund_rate" in normalized_question:
        return "refund_rate"

    history = _history_text(messages).lower()
    if "gmv" in history:
        return "gmv"

    return ""


def _infer_time_range(question, state):
    normalized_question = question.lower()

    if "最近7天" in question or "近7天" in question or "last 7" in normalized_question:
        return "last_7_days"
    if "上周" in question or "last week" in normalized_question:
        return "last_week"
    if "本周" in question or "this week" in normalized_question:
        return "this_week"

    if state and state.get("time_range"):
        return state["time_range"]

    return ""


def _infer_dimensions(question, state):
    normalized_question = question.lower()

    if "渠道" in question or "channel" in normalized_question:
        return ["channel"]
    if "商品" in question or "product" in normalized_question:
        return ["product"]
    if "品类" in question or "category" in normalized_question:
        return ["category"]

    if state:
        return state.get("dimensions", [])

    return []


def generate_sql(question: str, messages=None, state=None):
    messages = messages or []

    question_error = validate_user_question(question)
    if question_error:
        return "-- blocked: unsafe request"

    metric_name = _infer_metric(question, messages, state or {})
    time_range = _infer_time_range(question, state or {})
    dimensions = _infer_dimensions(question, state or {})

    if metric_name == "gmv" and "channel" in dimensions:
        if not time_range:
            return "-- need context"

        return """
        SELECT channel, SUM(order_amount) AS gmv
        FROM orders
        WHERE order_status = 'paid'
          AND paid_at >= CURRENT_DATE - INTERVAL '7 days'
        GROUP BY channel
        ORDER BY gmv DESC;
        """

    if metric_name == "gmv" and time_range == "last_week":
        return """
        SELECT
            current_week.gmv AS current_week,
            last_week.gmv AS last_week
        FROM current_week
        JOIN last_week ON 1 = 1;
        """

    if metric_name == "gmv":
        return """
        SELECT SUM(order_amount) AS recent_7_days_gmv
        FROM orders
        WHERE order_status = 'paid'
          AND paid_at >= CURRENT_DATE - INTERVAL '7 days';
        """

    if metric_name == "order_count":
        return """
        SELECT COUNT(order_id) AS order_count
        FROM orders
        WHERE order_status = 'paid';
        """

    if metric_name in {"aov", "refund_rate"}:
        return "-- unsupported question"

    return "-- unsupported question"
