import re


DANGEROUS_QUESTION_KEYWORDS = [
    "删除",
    "删表",
    "修改",
    "更新",
    "清空",
    "插入",
    "建表",
    "创建表",
    "改表",
    "drop",
    "delete",
    "update",
    "insert",
    "alter",
    "truncate",
    "create",
]

DANGEROUS_SQL_KEYWORDS = [
    "drop",
    "delete",
    "update",
    "insert",
    "alter",
    "truncate",
    "create",
]


def validate_user_question(question: str) -> str | None:
    normalized_question = (question or "").lower()

    for keyword in DANGEROUS_QUESTION_KEYWORDS:
        if keyword in normalized_question:
            return "安全拦截：检测到危险操作意图，只允许进行只读数据查询。"

    return None


def validate_sql(sql: str) -> str | None:
    normalized_sql = (sql or "").strip().lower()

    if not normalized_sql:
        return "SQL安全校验失败：SQL为空。"

    if normalized_sql.startswith("--"):
        return None

    if not normalized_sql.startswith("select"):
        return "SQL安全校验失败：只允许执行 SELECT 查询。"

    statement_count = len([part for part in normalized_sql.split(";") if part.strip()])
    if statement_count > 1:
        return "SQL安全校验失败：禁止多语句执行。"

    for keyword in DANGEROUS_SQL_KEYWORDS:
        if re.search(rf"\b{keyword}\b", normalized_sql):
            return f"SQL安全校验失败：禁止执行 {keyword.upper()} 操作。"

    if re.search(r"\bselect\s+\*", normalized_sql):
        return "SQL安全校验失败：禁止 SELECT *，请显式选择字段。"

    return None
