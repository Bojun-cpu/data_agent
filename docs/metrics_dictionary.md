# Data Agent 指标字典

指标字典用于统一业务口径，并为 SQL Agent 提供默认过滤条件、时间字段和可分析维度。

## GMV

- 中文名：成交金额
- 英文名：gmv
- 业务定义：指定时间范围内已支付订单的成交金额总和。
- 计算公式：`SUM(order_amount)`
- 默认过滤条件：`order_status = 'paid'`
- 时间字段：`paid_at`
- 可分析维度：渠道、商品、品类、地区、用户类型
- 示例 SQL：

```sql
SELECT SUM(order_amount) AS gmv
FROM orders
WHERE order_status = 'paid'
  AND paid_at >= CURRENT_DATE - INTERVAL '7 days';
```

## 订单量

- 中文名：订单量
- 英文名：order_count
- 业务定义：指定时间范围内已支付订单数量。
- 计算公式：`COUNT(order_id)`
- 默认过滤条件：`order_status = 'paid'`
- 时间字段：`paid_at`
- 可分析维度：渠道、商品、品类、地区
- 示例 SQL：

```sql
SELECT COUNT(order_id) AS order_count
FROM orders
WHERE order_status = 'paid'
  AND paid_at >= CURRENT_DATE - INTERVAL '7 days';
```

## 客单价

- 中文名：客单价
- 英文名：aov
- 业务定义：指定时间范围内平均每笔已支付订单金额。
- 计算公式：`SUM(order_amount) / COUNT(order_id)`
- 默认过滤条件：`order_status = 'paid'`
- 时间字段：`paid_at`
- 可分析维度：渠道、地区、用户类型
- 示例 SQL：

```sql
SELECT SUM(order_amount) / NULLIF(COUNT(order_id), 0) AS aov
FROM orders
WHERE order_status = 'paid'
  AND paid_at >= CURRENT_DATE - INTERVAL '7 days';
```

## 退款率

- 中文名：退款率
- 英文名：refund_rate
- 业务定义：退款订单数占有效订单数的比例。
- 计算公式：`COUNT(refunded_orders) / COUNT(all_orders)`
- 默认过滤条件：有效订单，退款订单使用 `order_status = 'refunded'`
- 时间字段：`paid_at` / `refund_at`
- 可分析维度：渠道、商品、品类、地区
- 示例 SQL：

```sql
SELECT
    SUM(CASE WHEN order_status = 'refunded' THEN 1 ELSE 0 END)
    / NULLIF(COUNT(order_id), 0)::NUMERIC AS refund_rate
FROM orders
WHERE paid_at >= CURRENT_DATE - INTERVAL '7 days';
```

## 转化率

- 中文名：转化率
- 英文名：conversion_rate
- 业务定义：下单用户数占访问用户数的比例。
- 计算公式：`paying_users / visiting_users`
- 默认过滤条件：访问行为和支付行为在同一时间窗口内。
- 时间字段：`event_time` / `paid_at`
- 可分析维度：渠道、页面、商品
- 示例 SQL：

```sql
SELECT
    COUNT(DISTINCT o.user_id) / NULLIF(COUNT(DISTINCT e.user_id), 0)::NUMERIC AS conversion_rate
FROM events e
LEFT JOIN orders o
    ON e.user_id = o.user_id
   AND o.order_status = 'paid'
   AND o.paid_at >= CURRENT_DATE - INTERVAL '7 days'
WHERE e.event_type = 'visit'
  AND e.event_time >= CURRENT_DATE - INTERVAL '7 days';
```

## 复购率

- 中文名：复购率
- 英文名：repeat_purchase_rate
- 业务定义：二次及以上购买用户占购买用户的比例。
- 计算公式：`repeat_users / paying_users`
- 默认过滤条件：`order_status = 'paid'`
- 时间字段：`paid_at`
- 可分析维度：渠道、地区、用户类型
- 示例 SQL：

```sql
WITH user_orders AS (
    SELECT user_id, COUNT(order_id) AS order_count
    FROM orders
    WHERE order_status = 'paid'
      AND paid_at >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY user_id
)
SELECT
    SUM(CASE WHEN order_count >= 2 THEN 1 ELSE 0 END)
    / NULLIF(COUNT(user_id), 0)::NUMERIC AS repeat_purchase_rate
FROM user_orders;
```

## 活跃用户数

- 中文名：活跃用户数
- 英文名：active_users
- 业务定义：指定时间范围内发生访问或购买行为的去重用户数。
- 计算公式：`COUNT(DISTINCT user_id)`
- 默认过滤条件：有效访问或有效购买行为。
- 时间字段：`event_time` / `paid_at`
- 可分析维度：渠道、地区、用户类型
- 示例 SQL：

```sql
SELECT COUNT(DISTINCT user_id) AS active_users
FROM events
WHERE event_time >= CURRENT_DATE - INTERVAL '7 days';
```

## 渠道表现

- 中文名：渠道表现
- 英文名：channel_performance
- 业务定义：按渠道拆分核心经营指标，用于比较不同渠道贡献。
- 计算公式：按渠道聚合 GMV、订单量、客单价、转化率等。
- 默认过滤条件：核心交易指标默认只统计已支付订单。
- 时间字段：`paid_at` / `event_time`
- 可分析维度：渠道、商品、品类、地区
- 示例 SQL：

```sql
SELECT channel, SUM(order_amount) AS gmv, COUNT(order_id) AS order_count
FROM orders
WHERE order_status = 'paid'
  AND paid_at >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY channel
ORDER BY gmv DESC;
```
