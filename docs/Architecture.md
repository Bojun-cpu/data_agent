# Data Agent 系统架构设计文档

## 1. 架构说明

本项目是一个基于大语言模型的 Data Agent 系统。

用户通过自然语言提出业务数据问题，系统通过 FastAPI 接收请求，并调用 LangGraph Agent 工作流完成意图理解、SQL 生成、SQL 安全校验、数据库查询、结果分析和报告生成。

---

## 2. 系统整体架构

```text
用户
 ↓
前端页面 / API 调用
 ↓
FastAPI 后端服务
 ↓
LangGraph Agent 工作流
 ↓
工具层 Tools
 ├── SQL 生成工具
 ├── SQL 安全校验工具
 ├── 数据库查询工具
 ├── 数据分析工具
 └── 报告生成工具
 ↓
数据层
 ├── PostgreSQL 业务数据库
 └── Redis 会话缓存
```

---

## 3. 核心模块说明

| 模块 | 作用 |
|---|---|
| 用户层 | 用户通过自然语言提出数据分析问题 |
| 前端/API层 | 负责发送请求和展示结果 |
| FastAPI 后端 | 接收请求、返回结果、管理接口 |
| LangGraph Agent | 管理 Agent 工作流和状态流转 |
| SQL 生成模块 | 根据用户问题生成 SQL |
| SQL 校验模块 | 检查 SQL 是否安全 |
| 数据库查询模块 | 执行 SQL 并返回查询结果 |
| 数据分析模块 | 对查询结果进行解释 |
| 报告生成模块 | 生成结构化数据报告 |
| PostgreSQL | 存储业务数据 |
| Redis | 存储会话状态和缓存 |

---

## 4. Agent 工作流

```text
用户问题
 ↓
Intent Node：理解用户意图
 ↓
SQL Generator Node：生成 SQL
 ↓
SQL Validator Node：校验 SQL 安全性
 ↓
SQL Executor Node：执行数据库查询
 ↓
Analysis Node：分析查询结果
 ↓
Response Node：生成回答
 ↓
返回用户
```

---

## 5. 请求流程示例

用户输入：

```text
最近7天GMV是多少？
```

系统处理流程：

1. FastAPI 接收用户请求。
2. LangGraph 读取用户问题和历史上下文。
3. Intent Node 判断用户想查询 GMV。
4. SQL Generator Node 生成查询 SQL。
5. SQL Validator Node 判断 SQL 是否只包含 SELECT。
6. SQL Executor Node 查询 PostgreSQL。
7. Analysis Node 分析查询结果。
8. Response Node 返回自然语言解释。

系统返回：

```text
最近7天GMV为125430元，相比上周增长8.6%。
```

---

## 6. 技术栈

| 技术 | 作用 |
|---|---|
| Python | 后端开发语言 |
| FastAPI | 提供 HTTP API 接口 |
| LangGraph | 构建 Agent 工作流 |
| PostgreSQL | 存储业务数据 |
| Redis | 存储会话和缓存 |
| Docker | 项目部署 |
| GitHub | 代码和文档管理 |

---

## 7. 架构设计目标

1. 模块清晰，便于后续开发。
2. Agent 工作流可扩展。
3. SQL 查询具备安全校验。
4. 支持多轮对话和上下文记忆。
5. 支持后续扩展 RAG、图表生成和多 Agent 协作。