# Data Agent 数据库设计文档

## 1. 数据库说明

本项目数据库主要用于存储业务数据和 Agent 会话数据。

业务数据用于支持 GMV、订单数、转化率等指标分析。

Agent 会话数据用于保存用户与 Data Agent 的历史对话、SQL生成记录以及分析结果。

---

## 2. users 用户表

| 字段名 | 类型 | 说明 |
|---------|---------|---------|
| user_id | INT | 用户主键 |
| name | VARCHAR | 用户名称 |
| email | VARCHAR | 用户邮箱 |
| created_at | DATETIME | 创建时间 |

---

## 3. products 商品表

| 字段名 | 类型 | 说明 |
|---------|---------|---------|
| product_id | INT | 商品主键 |
| product_name | VARCHAR | 商品名称 |
| category | VARCHAR | 商品分类 |
| price | DECIMAL | 商品价格 |
| created_at | DATETIME | 创建时间 |

---

## 4. orders 订单表

| 字段名 | 类型 | 说明 |
|---------|---------|---------|
| order_id | INT | 订单主键 |
| user_id | INT | 用户ID |
| order_amount | DECIMAL | 订单金额 |
| order_status | VARCHAR | 订单状态 |
| paid_at | DATETIME | 支付时间 |

---

## 5. order_items 订单明细表

| 字段名 | 类型 | 说明 |
|---------|---------|---------|
| item_id | INT | 明细主键 |
| order_id | INT | 订单ID |
| product_id | INT | 商品ID |
| quantity | INT | 数量 |
| item_amount | DECIMAL | 明细金额 |

---

## 6. events 用户行为表

| 字段名 | 类型 | 说明 |
|---------|---------|---------|
| event_id | INT | 行为主键 |
| user_id | INT | 用户ID |
| product_id | INT | 商品ID |
| event_type | VARCHAR | 行为类型 |
| created_at | DATETIME | 发生时间 |

---

## 7. agent_sessions 会话表

| 字段名 | 类型 | 说明 |
|---------|---------|---------|
| session_id | INT | 会话主键 |
| user_id | INT | 用户ID |
| created_at | DATETIME | 创建时间 |

---

## 8. agent_messages 消息表

| 字段名 | 类型 | 说明 |
|---------|---------|---------|
| message_id | INT | 消息主键 |
| session_id | INT | 会话ID |
| role | VARCHAR | user 或 assistant |
| content | TEXT | 消息内容 |
| generated_sql | TEXT | 生成SQL |
| created_at | DATETIME | 创建时间 |

---

## 9. 数据库用途

该数据库设计用于支持：

1. 电商业务数据查询
2. KPI指标分析
3. SQL自动生成
4. Agent多轮对话
5. 数据分析报告生成