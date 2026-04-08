# Month 2 学习计划：LangChain + Agent 基础

> **学习周期**：28 天（Day 29 - Day 56）
> **目标岗位**：AI Agent 工程师
> **前置要求**：完成 Month 1（Python 核心 + AI 基础）

---

## 本月学习目标

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

## Week 5: LangChain 基础

### 学习安排

| 天数 | 日期 | 主题 | 学习内容 | 产出 | 预计耗时 |
|------|------|------|---------|------|---------|
| Day 29 | 5/1 | LangChain 介绍 | 安装、核心概念、LLM 调用 | langchain_hello.py | 2h |
| Day 30 | 5/2 | Prompt 模板 | PromptTemplate、FewShot | prompt_template.py | 2h |
| Day 31 | 5/3 | Chain | SequentialChain、链式调用 | sequential_chain.py | 2h |
| Day 32 | 5/4 | OutputParser | 结构化输出解析 | output_parser.py | 2h |
| Day 33 | 5/5 | 复习/补进度 | 整理 Week 5 知识 | week5_review.md | 2h |
| Day 34 | 5/6 | 综合项目 | 股票分析助手（基础版） | stock_assistant_basic/ | 6h |
| Day 35 | 5/7 | 休息 | - | - | - |

### Week 5 详细任务

#### Day 29: LangChain 介绍

**学习内容**：
- [ ] LangChain 安装和配置
- [ ] 核心概念：Model、Prompt、Chain、Agent
- [ ] 第一个 LangChain 程序

**代码练习**：
```bash
# 安装 LangChain
pip install langchain langchain-community

# 运行示例
python month2/week5_langchain_basic/day29_langchain_hello/langchain_hello.py
```

**知识点**：
- LangChain 的核心模块
- LLM 封装和调用
- 简单对话实现

---

#### Day 30: Prompt 模板

**学习内容**：
- [ ] PromptTemplate 基础用法
- [ ] 变量替换
- [ ] FewShot Prompting（少样本提示）
- [ ] Prompt 设计技巧

**代码练习**：
```bash
python month2/week5_langchain_basic/day30_prompt_template/prompt_template.py
```

**知识点**：
- 动态 Prompt 生成
- FewShot 示例选择
- 股票场景 Prompt 设计

---

#### Day 31: Chain

**学习内容**：
- [ ] Chain 的概念和作用
- [ ] SequentialChain 顺序链
- [ ] TransformChain 数据转换
- [ ] 自定义 Chain

**代码练习**：
```bash
python month2/week5_langchain_basic/day31_chain/sequential_chain.py
```

**知识点**：
- 多步骤任务链式调用
- 输出传递和转换
- 股票分析 Chain 设计

---

#### Day 32: OutputParser

**学习内容**：
- [ ] OutputParser 的作用
- [ ] PydanticOutputParser
- [ ] CommaSeparatedListOutputParser
- [ ] 自定义解析器

**代码练习**：
```bash
python month2/week5_langchain_basic/day32_output_parser/output_parser.py
```

**知识点**：
- 结构化输出生成
- JSON 格式解析
- 股票数据格式化输出

---

#### Day 33: 复习/补进度

**任务**：
- [ ] 复习 Day 29-32 的内容
- [ ] 补做未完成的练习
- [ ] 整理 Week 5 知识笔记
- [ ] 代码提交 GitHub

**产出**：
- `month2/week5_langchain_basic/week5_review.md`

---

#### Day 34: 综合项目 - 股票分析助手（基础版）

**项目要求**：
- [ ] 使用 LangChain 搭建基础对话
- [ ] 集成股票数据查询功能
- [ ] 实现股票信息介绍
- [ ] 支持简单问答

**技术栈**：
- LangChain Core
- PromptTemplate
- Chain

**产出目录**：
```
month2/week5_langchain_basic/day34_project/
├── stock_assistant_basic.py
├── prompts/
│   └── stock_analysis_prompt.py
└── README.md
```

---

## Week 6: Agent + Tool 调用

### 学习安排

| 天数 | 日期 | 主题 | 学习内容 | 产出 | 预计耗时 |
|------|------|------|---------|------|---------|
| Day 36 | 5/8 | Agent 基础 | ReAct 模式、Agent 类型 | agent_basic.py | 2h |
| Day 37 | 5/9 | Tool 定义 | 自定义工具、@tool 装饰器 | custom_tools.py | 2h |
| Day 38 | 5/10 | Function Calling | API 调用、外部工具集成 | function_calling.py | 2h |
| Day 39 | 5/11 | 记忆管理 | ConversationBufferMemory | agent_memory.py | 2h |
| Day 40 | 5/12 | 复习/补进度 | 整理 Week 6 知识 | week6_review.md | 2h |
| Day 41 | 5/13 | 综合项目 | 股票查询 Agent | stock_query_agent/ | 6h |
| Day 42 | 5/14 | 休息 | - | - | - |

### Week 6 详细任务

#### Day 36: Agent 基础

**学习内容**：
- [ ] Agent 的概念和作用
- [ ] ReAct 模式（Reasoning + Acting）
- [ ] LangChain Agent 类型
- [ ] Zero-shot Agent

**代码练习**：
```bash
python month2/week6_agent_tool/day36_agent_basic/agent_basic.py
```

**知识点**：
- Agent 决策过程
- Thought-Action-Observation 循环
- 股票场景 Agent 应用

---

#### Day 37: Tool 定义

**学习内容**：
- [ ] LangChain Tool 概念
- [ ] @tool 装饰器使用
- [ ] 自定义工具注册
- [ ] Tool 描述和参数

**代码练习**：
```bash
python month2/week6_agent_tool/day37_custom_tools/custom_tools.py
```

**知识点**：
- 股票查询工具定义
- 技术分析工具
- 基本面分析工具

---

#### Day 38: Function Calling

**学习内容**：
- [ ] Function Calling 原理
- [ ] 外部 API 集成
- [ ] 工具选择和调用
- [ ] 错误处理

**代码练习**：
```bash
python month2/week6_agent_tool/day38_function_calling/function_calling.py
```

**知识点**：
- API 调用封装
- 多工具协调
- 股票数据 API 集成

---

#### Day 39: 记忆管理

**学习内容**：
- [ ] 对话记忆的重要性
- [ ] ConversationBufferMemory
- [ ] ConversationSummaryMemory
- [ ] 记忆长度控制

**代码练习**：
```bash
python month2/week6_agent_tool/day39_agent_memory/agent_memory.py
```

**知识点**：
- 多轮对话上下文
- 记忆压缩和总结
- 股票分析对话历史

---

#### Day 40: 复习/补进度

**任务**：
- [ ] 复习 Day 36-39 的内容
- [ ] 补做未完成的练习
- [ ] 整理 Week 6 知识笔记
- [ ] 代码提交 GitHub

**产出**：
- `month2/week6_agent_tool/week6_review.md`

---

#### Day 41: 综合项目 - 股票查询 Agent

**项目要求**：
- [ ] 支持自然语言股票查询
- [ ] 集成多个股票数据 Tool
- [ ] 实现多轮对话记忆
- [ ] 返回结构化股票信息

**技术栈**：
- LangChain Agent
- Custom Tools
- Memory

**产出目录**：
```
month2/week6_agent_tool/day41_project/
├── stock_query_agent.py
├── tools/
│   ├── stock_price_tool.py
│   ├── stock_info_tool.py
│   └── stock_chart_tool.py
├── memory/
│   └── conversation_memory.py
└── README.md
```

---

## Week 7: 向量数据库

### 学习安排

| 天数 | 日期 | 主题 | 学习内容 | 产出 | 预计耗时 |
|------|------|------|---------|------|---------|
| Day 43 | 5/15 | 向量数据库概念 | Embedding、相似度计算 | embedding_basic.py | 2h |
| Day 44 | 5/16 | Milvus 安装 | Docker 部署、配置 | milvus_installed.txt | 2h |
| Day 45 | 5/17 | Milvus 操作 | Collection、CRUD | milvus_crud.py | 2h |
| Day 46 | 5/18 | LangChain 集成 | VectorStore、检索 | langchain_vectorstore.py | 2h |
| Day 47 | 5/19 | 复习/补进度 | 整理 Week 7 知识 | week7_review.md | 2h |
| Day 48 | 5/20 | 综合项目 | 股票研报检索系统 | stock_report_search/ | 6h |
| Day 49 | 5/21 | 休息 | - | - | - |

### Week 7 详细任务

#### Day 43: 向量数据库概念

**学习内容**：
- [ ] Embedding 原理
- [ ] 向量相似度计算（余弦、欧氏距离）
- [ ] 向量数据库的作用
- [ ] 常见向量数据库对比

**代码练习**：
```bash
python month2/week7_vector_db/day43_embedding_basic/embedding_basic.py
```

**知识点**：
- 文本向量化
- 相似度搜索
- 股票文本语义匹配

---

#### Day 44: Milvus 安装

**学习内容**：
- [ ] Docker 安装 Milvus
- [ ] 配置文件说明
- [ ] 服务启动和验证
- [ ] 常见问题排查

**操作命令**：
```bash
# Docker 启动 Milvus
cd month2/week7_vector_db/milvus_docker
docker-compose up -d

# 验证安装
curl http://localhost:9091/healthz
```

**产出**：
- `milvus_installed.txt`（安装成功截图和配置）

---

#### Day 45: Milvus 操作

**学习内容**：
- [ ] Collection 创建和管理
- [ ] 数据插入（Insert）
- [ ] 向量搜索（Search）
- [ ] 索引构建

**代码练习**：
```bash
python month2/week7_vector_db/day45_milvus_crud/milvus_crud.py
```

**知识点**：
- Schema 定义
- 向量 + 标量混合查询
- 股票数据存入

---

#### Day 46: LangChain 集成

**学习内容**：
- [ ] LangChain VectorStore 接口
- [ ] Milvus 向量存储
- [ ] 相似度搜索
- [ ] 文本检索链

**代码练习**：
```bash
python month2/week7_vector_db/day46_langchain_vectorstore/langchain_vectorstore.py
```

**知识点**：
- Document 加载
- 向量存储和检索
- 研报语义搜索

---

#### Day 47: 复习/补进度

**任务**：
- [ ] 复习 Day 43-46 的内容
- [ ] 补做未完成的练习
- [ ] 整理 Week 7 知识笔记
- [ ] 代码提交 GitHub

**产出**：
- `month2/week7_vector_db/week7_review.md`

---

#### Day 48: 综合项目 - 股票研报检索系统

**项目要求**：
- [ ] 加载股票研报 PDF/文本
- [ ] 文档分块和向量化
- [ ] 语义检索查询
- [ ] 返回相关研报片段

**技术栈**：
- Milvus
- LangChain VectorStore
- Document Loader

**产出目录**：
```
month2/week7_vector_db/day48_project/
├── stock_report_search.py
├── document_loader/
│   └── pdf_loader.py
├── chunking/
│   └── text_splitter.py
├── vector_store/
│   └── milvus_store.py
└── README.md
```

---

## Week 8: RAG 系统

### 学习安排

| 天数 | 日期 | 主题 | 学习内容 | 产出 | 预计耗时 |
|------|------|------|---------|------|---------|
| Day 50 | 5/22 | RAG 原理 | 检索增强生成流程 | rag_basic.py | 2h |
| Day 51 | 5/23 | 文档加载 | DocumentLoader、分块 | document_chunking.py | 2h |
| Day 52 | 5/24 | 检索 + 生成 | RAG 完整流程 | rag_pipeline.py | 2h |
| Day 53 | 5/25 | 效果评估 | 准确率、召回率测试 | rag_evaluation.py | 2h |
| Day 54 | 5/26 | 复习/补进度 | 整理 Week 8 知识 | week8_review.md | 2h |
| Day 55 | 5/27 | 综合项目 | 股票知识库 RAG 系统 | stock_knowledge_rag/ | 6h |
| Day 56 | 5/28 | 休息 | - | - | - |

### Week 8 详细任务

#### Day 50: RAG 原理

**学习内容**：
- [ ] RAG（检索增强生成）概念
- [ ] RAG vs 纯 LLM
- [ ] RAG 工作流程
- [ ] 应用场景分析

**代码练习**：
```bash
python month2/week8_rag/day50_rag_basic/rag_basic.py
```

**知识点**：
- 检索阶段
- 生成阶段
- 股票问答 RAG 架构

---

#### Day 51: 文档加载

**学习内容**：
- [ ] DocumentLoader 类型
- [ ] PDF/Text/HTML 加载
- [ ] 文本分块策略
- [ ] 元数据管理

**代码练习**：
```bash
python month2/week8_rag/day51_document_chunking/document_chunking.py
```

**知识点**：
- 递归分块
- 固定大小分块
- 股票文档分块策略

---

#### Day 52: 检索 + 生成

**学习内容**：
- [ ] Retriever 配置
- [ ] 相关性排序
- [ ] 上下文组装
- [ ] LLM 生成答案

**代码练习**：
```bash
python month2/week8_rag/day52_rag_pipeline/rag_pipeline.py
```

**知识点**：
- 检索参数调优
- Top-K 选择
- 答案生成质量

---

#### Day 53: 效果评估

**学习内容**：
- [ ] RAG 评估指标
- [ ] 准确率测试
- [ ] 召回率测试
- [ ] 端到端评估

**代码练习**：
```bash
python month2/week8_rag/day53_rag_evaluation/rag_evaluation.py
```

**知识点**：
- 测试集构建
- 评估自动化
- 股票问答评估

---

#### Day 54: 复习/补进度

**任务**：
- [ ] 复习 Day 50-53 的内容
- [ ] 补做未完成的练习
- [ ] 整理 Week 8 知识笔记
- [ ] 代码提交 GitHub

**产出**：
- `month2/week8_rag/week8_review.md`

---

#### Day 55: 综合项目 - 股票知识库 RAG 系统

**项目要求**：
- [ ] 完整的 RAG 流程
- [ ] 股票知识库构建
- [ ] 自然语言问答
- [ ] 引用来源展示

**技术栈**：
- LangChain RAG
- Milvus VectorStore
- Document Loader
- LLM

**产出目录**：
```
month2/week8_rag/day55_project/
├── stock_knowledge_rag.py
├── knowledge_base/
│   ├── stock_reports/        # 研报文件
│   └── stock_wiki/           # 百科数据
├── retrieval/
│   ├── retriever.py
│   └── reranker.py
├── generation/
│   └── answer_generator.py
└── README.md
```

---

## 本月必做项目清单

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
- LangChain: https://python.langchain.com/
- LangChain Agent: https://python.langchain.com/docs/modules/agents/
- Milvus: https://milvus.io/docs
- LangChain RAG: https://python.langchain.com/docs/use_cases/question_answering/

### 参考书籍
- 《LangChain 实战》⭐⭐⭐
- 《检索增强生成 (RAG) 实战》⭐⭐⭐

---

## 学习建议

### ✅ 建议
1. **每天代码**：即使只看视频，也要跟着敲代码
2. **项目驱动**：每个周的项目一定要完成
3. **及时提问**：遇到问题超过 1 小时，及时寻求帮助
4. **建立知识库**：整理学习笔记和代码片段
5. **加入社区**：LangChain 中文网、AI 技术交流群

### ❌ 避免
1. 只看不练（一定要动手写代码）
2. 追求完美（先跑通再优化）
3. 死磕环境配置（环境问题及时搜索/提问）
4. 不写笔记（好记性不如烂笔头）

---

## 进度追踪

### 周度检查点

每周日复盘：
- [ ] 本周计划完成度
- [ ] 遇到的问题
- [ ] 下周调整计划
- [ ] 代码提交 GitHub

### 每日检查点

每天学习后打卡：
- [ ] 完成今日任务
- [ ] 代码已保存
- [ ] 笔记已整理
- [ ] 问题已记录

---

## 环境准备

### Python 环境
```bash
# 创建虚拟环境
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate  # Mac/Linux

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

**Month 2 结束后，你将具备 AI Agent 开发的基础能力！加油！**

*创建时间：2026-04-08*
*版本：v1.0*
