# Data Agent API 文档

## 1. API 说明

本项目后端使用 FastAPI 提供接口，前端或用户通过 HTTP 请求与 Data Agent 系统交互。

API 主要用于支持自然语言查询、会话历史查询、KPI 查询和数据报告生成。

---

## 2. 智能问答接口

### 接口名称

智能问答接口

### 请求方式

POST

### 接口地址

/api/chat

### 功能说明

用户输入自然语言问题，系统调用 Data Agent 理解问题、生成 SQL、查询数据库，并返回分析结果。

### 请求参数

```json
{
  "user_id": "u001",
  "session_id": "s001",
  "message": "最近7天GMV是多少？"
}
```

### 返回结果

```json
{
  "answer": "最近7天GMV为125430元，相比上周增长8.6%。",
  "sql": "SELECT SUM(order_amount) FROM orders WHERE paid_at >= CURRENT_DATE - INTERVAL '7 days';",
  "chart_type": "line",
  "chart_data": []
}
```

---

## 3. 会话历史接口

### 请求方式

GET

### 接口地址

/api/sessions/{session_id}

### 功能说明

根据 session_id 查询用户与 Data Agent 的历史对话记录。

### 返回结果

```json
{
  "session_id": "s001",
  "messages": [
    {
      "role": "user",
      "content": "最近7天GMV是多少？"
    },
    {
      "role": "assistant",
      "content": "最近7天GMV为125430元。"
    }
  ]
}
```

---

## 4. KPI 汇总接口

### 请求方式

GET

### 接口地址

/api/kpi/summary

### 功能说明

查询核心业务指标汇总数据，例如 GMV、订单数、客单价、转化率等。

### 请求示例

/api/kpi/summary?start_date=2026-06-01&end_date=2026-06-07

### 返回结果

```json
{
  "gmv": 125430,
  "order_count": 3200,
  "average_order_value": 39.2,
  "conversion_rate": "5.6%"
}
```

---

## 5. 报告生成接口

### 请求方式

POST

### 接口地址

/api/report/generate

### 功能说明

根据用户指定的时间范围生成业务数据分析报告。

### 请求参数

```json
{
  "user_id": "u001",
  "start_date": "2026-06-01",
  "end_date": "2026-06-07",
  "report_type": "weekly"
}
```

### 返回结果

```json
{
  "report_title": "2026年6月第一周运营数据报告",
  "summary": "本周GMV为125430元，订单数为3200单，整体业务较上周增长8.6%。",
  "key_findings": [
    "GMV较上周增长8.6%",
    "手机配件品类贡献了主要增长",
    "转化率小幅下降，需要关注访问质量"
  ]
}
```

---

## 6. SQL 安全校验接口

### 请求方式

POST

### 接口地址

/api/sql/validate

### 功能说明

检查 Agent 生成的 SQL 是否安全。

系统只允许执行 SELECT 查询，禁止 DELETE、UPDATE、DROP、INSERT 等危险 SQL。

### 请求参数

```json
{
  "sql": "SELECT SUM(order_amount) FROM orders;"
}
```

### 返回结果

```json
{
  "is_safe": true,
  "reason": "SQL only contains SELECT operation."
}
```

---

## 7. 错误返回格式

当接口调用失败时，系统返回统一错误格式。

```json
{
  "error_code": "SQL_GENERATION_FAILED",
  "message": "系统未能生成有效SQL，请重新输入问题。"
}
```

---

## 8. API 设计说明

本 API 文档主要定义第一阶段 MVP 所需接口。

核心接口是 /api/chat，该接口负责连接用户问题、Agent 工作流、SQL 生成、数据库查询和结果分析。

后续可以继续扩展图表接口、权限接口、多数据库连接接口和 Agent 评估接口。