def generate_sql(question: str, messages=None):
    messages = messages or []
    normalized_question = question.lower()

    if "gmv" in normalized_question:
        return """
        SELECT SUM(order_amount) AS recent_7_days_gmv
        FROM orders
        WHERE paid_at >= CURRENT_DATE - INTERVAL '7 days';
        """

    if "上周" in question:
        history = " ".join(
            str(message.get("content", ""))
            for message in messages
            if isinstance(message, dict)
        )

        if "gmv" in history.lower():
            return """
            SELECT
                current_week.gmv AS current_week,
                last_week.gmv AS last_week
            FROM current_week
            JOIN last_week ON 1 = 1;
            """

        return "-- need context"

    if "订单" in question:
        return """
        SELECT COUNT(*)
        FROM orders;
        """

    return "-- unsupported question"
