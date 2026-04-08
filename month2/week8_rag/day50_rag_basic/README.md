# Day 50: RAG 原理

> **日期**: 2026-05-22（周四）  
> **周次**: Week 8 - RAG 系统  
> **预计耗时**: 2 小时

---

## 今日学习目标

- [ ] 理解 RAG（检索增强生成）概念
- [ ] 掌握 RAG 工作流程
- [ ] 了解 RAG vs 纯 LLM 的区别
- [ ] 学会 RAG 应用场景分析

---

## 学习内容

### 1. 什么是 RAG？

**RAG = Retrieval-Augmented Generation（检索增强生成）**

核心思想：**先检索相关知识，再让 LLM 基于知识生成答案**

```
┌─────────────────────────────────────────────────────────┐
│              RAG vs 纯 LLM 对比                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  纯 LLM:                                                │
│  用户问题 → [LLM] → 答案（仅靠训练记忆）                │
│  ❌ 可能过时、可能编造、无法引用来源                    │
│                                                         │
│  RAG:                                                   │
│  用户问题 → [检索] → 相关文档 → [LLM] → 答案            │
│  ✅ 基于最新数据、减少编造、可追溯来源                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 2. RAG 工作流程

```
┌─────────────────────────────────────────────────────────┐
│                RAG 完整流程                              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  【离线阶段】文档准备                                   │
│  1. 文档加载 → 2. 文本分块 → 3. 向量化 → 4. 存储        │
│                                                         │
│  【在线阶段】问答流程                                   │
│  1. 用户提问                                            │
│  2. 问题向量化                                          │
│  3. 相似度搜索（找到 Top-K 相关文档）                    │
│  4. 组装 Prompt（问题 + 上下文）                        │
│  5. LLM 生成答案                                          │
│  6. 返回答案（附带来源引用）                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 3. RAG 的核心组件

| 组件 | 作用 | 技术选型 |
|------|------|----------|
| **文档加载** | 读取各种格式文档 | LangChain Loaders |
| **文本分块** | 将长文档切分为片段 | RecursiveTextSplitter |
| **Embedding** | 文本→向量 | OpenAI Embedding、m3e |
| **向量数据库** | 存储和检索向量 | Milvus、Chroma |
| **检索器** | 查找相关文档 | VectorStore Retriever |
| **LLM** | 生成最终答案 | GPT-4、DeepSeek |

### 4. RAG 的应用场景

| 场景 | 说明 | 案例 |
|------|------|------|
| **知识库问答** | 企业内部知识检索 | 员工手册、技术文档 |
| **客服系统** | 产品问题自动回答 | 电商客服、技术支持 |
| **研究助手** | 论文/报告检索 | 学术文献、研报分析 |
| **法律助手** | 法条案例检索 | 合同审查、法律咨询 |
| **医疗咨询** | 医学文献检索 | 病症查询、用药建议 |

### 5. 基础 RAG 实现

```python
from langchain.vectorstores import Milvus
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 1. 初始化组件
embeddings = OpenAIEmbeddings()
vectorstore = Milvus(..., embedding_function=embeddings)
llm = ChatOpenAI(model="gpt-3.5-turbo")

# 2. 创建检索器
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 3. 定义 Prompt
system_prompt = """请根据以下上下文回答问题。

上下文：
{context}

问题：{input}

如果上下文中没有答案，请直接说明。"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# 4. 创建 RAG 链
qa_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, qa_chain)

# 5. 执行
response = rag_chain.invoke({"input": "茅台的市盈率是多少？"})
print(f"答案：{response['answer']}")
print(f"来源：{response['context']}")
```

---

## 实践任务

### 任务 1: RAG 流程理解 ✅

```python
# rag_basic.py

# 绘制 RAG 流程图（用文字或图形）
# 标注每个环节的作用和输入输出

# 示例：
# 输入："茅台 PE 多少？"
#   ↓
# 检索：找到 ["茅台 PE 约 30 倍", ...]
#   ↓
# 组装 Prompt: "根据以下信息回答：茅台 PE 约 30 倍。问题：茅台 PE 多少？"
#   ↓
# LLM 生成："茅台的市盈率约为 30 倍"
#   ↓
# 输出答案
```

### 任务 2: 对比实验 ✅

```python
# rag_vs_llm.py

# 1. 纯 LLM 回答
llm_answer = llm.invoke("2024 年白酒行业发展趋势如何？")

# 2. RAG 回答
rag_answer = rag_chain.invoke({"input": "2024 年白酒行业发展趋势如何？"})

# 对比两者差异：
# - 准确性
# - 时效性
# - 是否有来源引用
```

### 任务 3: 场景分析 ✅

```python
# rag_use_cases.md

# 分析你的项目中 RAG 可以应用的场景
# 列出：
# 1. 数据来源是什么？
# 2. 用户会问什么问题？
# 3. 期望的回答格式？
```

---

## 知识点总结

### RAG 的优势

| 优势 | 说明 |
|------|------|
| 减少幻觉 | 基于检索到的事实，减少编造 |
| 时效性强 | 可以检索最新文档 |
| 可追溯 | 能提供来源引用 |
| 成本低 | 无需微调 LLM |

### RAG 的挑战

| 挑战 | 解决思路 |
|------|----------|
| 检索质量 | 优化 Embedding 和分块策略 |
| 上下文长度 | 智能选择最相关的片段 |
| 多跳推理 | 迭代检索或 Agent RAG |

---

## 常见问题

### Q1: RAG 什么时候用？

- 需要最新知识
- 需要准确引用来源
- 领域专业知识问答
- LLM 训练数据覆盖不到

### Q2: RAG 什么时候不用？

- 通用知识问答（LLM 已知）
- 创意生成任务
- 简单查询（直接检索即可）

### Q3: 如何评估 RAG 效果？

- **检索质量**：召回率、准确率
- **生成质量**：答案准确性、流畅度
- **端到端**：用户满意度

---

## 代码文件

```
day50_rag_basic/
├── README.md                    # 本文件
├── rag_basic.py                 # 基础 RAG 实现
├── rag_vs_llm.py                # RAG vs LLM 对比
└── rag_use_cases.md             # 应用场景分析
```

---

## 参考资源

- [RAG 论文](https://arxiv.org/abs/2005.11401)
- [LangChain RAG 文档](https://python.langchain.com/docs/use_cases/question_answering)
- [RAG 实战指南](https://www.ragforum.io/)

---

## 下一步

- **Day 51**: 文档加载和分块策略
- **明日任务**: 学习文档处理技巧

---

**💡 今日格言**: "RAG 让 LLM 从'凭记忆'变成'查资料'"
