# Month 2: LangChain + Agent 基础

> **学习周期**: 28 天（Day 29 - Day 56）  
> **目标岗位**: AI Agent 工程师  
> **前置要求**: 完成 Month 1（Python 核心 + AI 基础）

---

## 本月目标

完成本月学习后，你将能够：

- [ ] 掌握 LangChain 核心组件和使用方法
- [ ] 理解 Agent 工作原理（ReAct 模式）
- [ ] 学会自定义 Tool 和 Function Calling
- [ ] 掌握向量数据库 Milvus 的部署和使用
- [ ] 独立开发 RAG（检索增强生成）系统
- [ ] 完成 4 个实战项目

---

## 周计划概览

| 周次 | 主题 | 重点内容 | 项目 | 天数 |
|------|------|---------|------|------|
| Week 5 | LangChain 基础 | Prompt、Chain、Parser | 股票分析助手（基础版） | Day 29-35 |
| Week 6 | Agent + Tool | ReAct、Function Calling | 股票查询 Agent | Day 36-42 |
| Week 7 | 向量数据库 | Milvus、VectorStore | 股票研报检索系统 | Day 43-49 |
| Week 8 | RAG 系统 | 检索增强生成流程 | 股票知识库 RAG 系统 | Day 50-56 |

---

## 目录结构

```
month2/
├── README.md                          # 本文件
├── month2_learning_plan.md            # 详细学习计划
├── week5_langchain_basic/             # Week 5: LangChain 基础
│   ├── day29_langchain_hello/         # Day 29: LangChain 介绍
│   ├── day30_prompt_template/         # Day 30: Prompt 模板
│   ├── day31_chain/                   # Day 31: Chain 链式调用
│   ├── day32_output_parser/           # Day 32: OutputParser 输出解析
│   ├── day33_review/                  # Day 33: 复习/补进度
│   ├── day34_stock_assistant/         # Day 34: 股票分析助手
│   └── README.md
│
├── week6_agent_tool/                  # Week 6: Agent + Tool
│   ├── day36_agent_basic/             # Day 36: Agent 基础
│   ├── day37_custom_tools/            # Day 37: Tool 定义
│   ├── day38_function_calling/        # Day 38: Function Calling
│   ├── day39_agent_memory/            # Day 39: 记忆管理
│   ├── day40_review/                  # Day 40: 复习/补进度
│   ├── day41_stock_query_agent/       # Day 41: 股票查询 Agent
│   └── README.md
│
├── week7_vector_db/                   # Week 7: 向量数据库
│   ├── day43_embedding_basic/         # Day 43: Embedding 概念
│   ├── day44_milvus_install/          # Day 44: Milvus 安装
│   ├── day45_milvus_crud/             # Day 45: Milvus CRUD
│   ├── day46_langchain_vectorstore/   # Day 46: LangChain 集成
│   ├── day47_review/                  # Day 47: 复习/补进度
│   ├── day48_stock_report_search/     # Day 48: 研报检索系统
│   └── README.md
│
└── week8_rag/                         # Week 8: RAG 系统
    ├── day50_rag_basic/               # Day 50: RAG 原理
    ├── day51_document_chunking/       # Day 51: 文档加载和分块
    ├── day52_rag_pipeline/            # Day 52: RAG 完整流程
    ├── day53_rag_evaluation/          # Day 53: 效果评估
    ├── day54_review/                  # Day 54: 复习/补进度
    ├── day55_stock_knowledge_rag/     # Day 55: 股票知识库 RAG
    └── README.md
```

---

## 必做项目清单

| # | 项目名称 | 周次 | 难度 | 状态 |
|---|---------|------|------|------|
| 1 | 股票分析助手（基础版） | Week 5 | ⭐⭐ | ⬜ |
| 2 | 股票查询 Agent | Week 6 | ⭐⭐⭐ | ⬜ |
| 3 | 股票研报检索系统 | Week 7 | ⭐⭐⭐ | ⬜ |
| 4 | 股票知识库 RAG 系统 | Week 8 | ⭐⭐⭐⭐ | ⬜ |

---

## 学习资源

### B 站课程
| 课程 | UP 主 | 优先级 | 预计时长 |
|------|------|--------|---------|
| LangChain 从入门到精通 | 卢菁博士 | ⭐⭐⭐⭐⭐ | 15h |
| LangChain Agent 实战 | 各种 AI 博主 | ⭐⭐⭐⭐ | 8h |
| Milvus 向量数据库入门 | Zilliz 官方 | ⭐⭐⭐⭐ | 4h |
| RAG 系统实战 | AI 工程师 | ⭐⭐⭐⭐ | 6h |

### 官方文档
- [LangChain](https://python.langchain.com/)
- [Milvus](https://milvus.io/docs)
- [LangChain RAG](https://python.langchain.com/docs/use_cases/question_answering/)

---

## 进度追踪

### 完成检查

#### Week 5: LangChain 基础
- [ ] Day 29: LangChain 介绍
- [ ] Day 30: Prompt 模板
- [ ] Day 31: Chain
- [ ] Day 32: OutputParser
- [ ] Day 33: 复习/补进度
- [ ] Day 34: 股票分析助手
- [ ] Day 35: 休息

#### Week 6: Agent + Tool
- [ ] Day 36: Agent 基础
- [ ] Day 37: Tool 定义
- [ ] Day 38: Function Calling
- [ ] Day 39: 记忆管理
- [ ] Day 40: 复习/补进度
- [ ] Day 41: 股票查询 Agent
- [ ] Day 42: 休息

#### Week 7: 向量数据库
- [ ] Day 43: Embedding 概念
- [ ] Day 44: Milvus 安装
- [ ] Day 45: Milvus CRUD
- [ ] Day 46: LangChain 集成
- [ ] Day 47: 复习/补进度
- [ ] Day 48: 研报检索系统
- [ ] Day 49: 休息

#### Week 8: RAG 系统
- [ ] Day 50: RAG 原理
- [ ] Day 51: 文档加载和分块
- [ ] Day 52: RAG 流程
- [ ] Day 53: 效果评估
- [ ] Day 54: 复习/补进度
- [ ] Day 55: 股票知识库 RAG
- [ ] Day 56: 休息

---

## 环境准备

### Python 环境
```bash
# 创建虚拟环境
python -m venv venv
source venv/Scripts/activate  # Windows

# 安装依赖
pip install langchain langchain-community langchain-openai
pip install pymilvus
pip install openai
```

### Docker 环境（Milvus）
```bash
# 安装 Docker Desktop
# https://www.docker.com/products/docker-desktop/

# 验证安装
docker --version
docker-compose --version
```

---

## 下一步

完成 Month 2 后，进入 **Month 3: Agent 进阶 + 项目实战**

- Week 9: AutoGen 多 Agent 协作
- Week 10: CrewAI 任务编排
- Week 11-12: 综合项目

---

**🎉 Month 2 结束后，你将具备 AI Agent 开发的基础能力！加油！**

*最后更新：2026-04-08*
*版本：v1.0*
