# Week 2 Report – Agent Core Development

## 1. 本周目标

根据项目计划，本周主要完成 Data Agent 核心 Agent 框架开发，包括：

1. StateGraph 设计
2. SQL Agent 实现
3. Memory 模块设计
4. Tool Calling 机制实现

---

## 2. 本周完成内容

### 2.1 StateGraph 工作流搭建

基于 LangGraph 实现 Agent 工作流。

当前工作流如下：

User Question
↓
Intent Node
↓
SQL Node
↓
Execute SQL Node
↓
Response Node
↓
Final Answer

完成内容：

* 创建 AgentState
* 创建 Graph 结构
* 定义节点之间的执行顺序
* 实现 Graph 编译与运行

---

### 2.2 SQL Agent 实现

完成 SQL Agent 初版实现。

实现内容：

* 根据用户问题生成 SQL
* 支持 GMV 查询
* 支持订单数量查询
* 支持基于上下文的 SQL 生成

示例：

用户问题：

最近7天GMV是多少？

生成 SQL：

SELECT SUM(order_amount)
FROM orders
WHERE paid_at >= CURRENT_DATE - INTERVAL '7 days';

---

### 2.3 Tool Calling 实现

完成 Tool 模块设计。

新增：

src/tools/sql_tool.py

实现：

* generate_sql()

Agent Node 可以通过 Tool 调用 SQL 生成功能。

实现 Agent 与 Tool 解耦。

---

### 2.4 Memory 模块实现

完成多轮对话 Memory 设计。

新增：

src/memory/memory.py

实现：

* 保存用户消息
* 保存 Agent 回复
* 保存历史上下文

当前结构：

messages = [
{
"role": "user",
"content": "最近7天GMV是多少？"
},
{
"role": "assistant",
"content": "最近7天GMV为125430元。"
}
]

---

### 2.5 多轮对话测试

完成两轮对话验证。

第一轮：

最近7天GMV是多少？

返回：

最近7天GMV为125430元。

第二轮：

那和上周相比呢？

系统能够读取历史上下文并生成对应 SQL。

返回：

本周GMV为125430元，
上周GMV为118200元，
增长6.12%。

---

## 3. 遇到的问题


### Memory 未正确传递

现象：

第二轮问题返回：

-- need context

原因：

messages 未正确传递给 SQL Tool。

解决方案：

在 sql_node 中传递：

generate_sql(
question,
state.get("messages", [])
)

修复后多轮对话正常工作。

---

## 4. 当前项目进度

完成情况：

* StateGraph：100%
* SQL Agent：100%
* Memory：100%
* Tool Calling：100%

总体完成度：

Week2 目标完成。

---

## 5. 下周计划

Week3 计划：

1. 接入 PostgreSQL
2. 实现真实 SQL 查询
3. 实现 SQL 安全校验
4. 开发 FastAPI 接口
5. 打通 Agent 到数据库完整链路
