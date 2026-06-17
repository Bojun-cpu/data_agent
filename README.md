# Data Agent

Data Agent 是一个面向电商经营分析场景的企业级数据助手原型。用户可以用自然语言查询 GMV、订单量、客单价、退款率、渠道表现等业务指标，并支持基于上下文的多轮追问。

当前项目聚焦 Week1 和 Week2 交付：产品与架构设计、数据库建模、指标口径设计、LangGraph 工作流、SQL Agent 原型、短期记忆、SQL 安全拦截和 mock SQL 执行。

## 技术栈

- Python
- LangGraph / StateGraph
- FastAPI 设计文档
- PostgreSQL 设计文档
- unittest 测试

## 目录结构

```text
data_agent/
├── docs/
│   ├── API.md
│   ├── Architecture.md
│   ├── ERD.md
│   ├── database_design.md
│   ├── metrics_dictionary.md
│   └── schema.sql
├── src/
│   ├── agent/
│   │   ├── graph.py
│   │   ├── nodes.py
│   │   └── state.py
│   ├── memory/
│   │   └── memory.py
│   └── tools/
│       ├── sql_security.py
│       └── sql_tool.py
├── tests/
│   ├── golden_questions.json
│   ├── test_graph.py
│   ├── test_sql_security.py
│   └── test_sql_tool.py
└── README.md
```

## Week1 已完成内容

- PRD 设计：明确电商经营分析场景。
- 指标体系设计：覆盖 GMV、订单量、客单价、退款率、转化率、复购率、活跃用户数、渠道表现。
- 数据库建模：设计用户、商品、订单、订单明细、行为、Agent 会话和消息表。
- ER 图：提供 Mermaid ER 图。
- DDL：提供 `docs/schema.sql`。
- API 设计：提供 `/api/chat`、会话查询、KPI 汇总、报告生成、SQL 校验接口设计。
- 架构设计：提供 LangGraph Agent、Tools、PostgreSQL、Redis 的分层设计。

## Week2 已完成内容

- 使用 StateGraph 搭建 Agent 工作流。
- 实现规则版 intent node、sql node、sql security node、execute sql node、response node。
- 实现 SQL Agent 原型，支持 GMV、订单量、上周对比、渠道拆分。
- 实现短期记忆：通过 `messages` 和结构化 state 继承上下文。
- 实现 SQL 安全层：拦截危险用户意图和危险 SQL。
- 实现 mock SQL 执行，不连接真实数据库。
- 补充 unittest 测试和 golden questions。

## 当前支持的示例对话

```text
用户：最近7天GMV是多少？
助手：最近7天GMV为125430元。

用户：上周呢？
助手：本周GMV为125430元，上周GMV为118200元，增长6.12%。

用户：按渠道拆一下？
助手：最近7天GMV按渠道拆分为：app 62300元，web 41120元，mini_program 22010元。

用户：删除订单表。
助手：安全拦截：检测到危险操作意图，只允许进行只读数据查询。
```

## 当前限制

- SQL 执行仍是 mock，不连接真实 PostgreSQL。
- FastAPI 接口目前只有设计文档，`src/app.py` 尚未实现。
- Memory 仍以短期记忆为主，没有 Redis 或数据库长期记忆。
- SQL 生成是规则版原型，不是 LLM + Schema RAG。
- PostgreSQL 接入、真实 SQL 执行、权限系统和审计日志放到 Week4 之后实现。

## 如何运行

在项目根目录执行：

```powershell
cd C:\Users\34424\Desktop\data_agent\src
..\.venv\Scripts\python.exe -m agent.graph
```

如果你的本机 `python` 已加入 PATH，也可以执行：

```powershell
cd C:\Users\34424\Desktop\data_agent\src
python -m agent.graph
```

## 如何测试

在项目根目录执行：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

