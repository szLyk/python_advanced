# Day 52: 检索 + 生成（RAG 完整流程）

> **日期**: 2026-05-24（周六）  
> **周次**: Week 8 - RAG 系统  
> **预计耗时**: 2 小时

---

## 今日学习目标

- [ ] 掌握 Retriever 配置
- [ ] 理解相关性排序
- [ ] 学会上下文组装
- [ ] 实现完整 RAG 流程

---

## 学习内容

### 1. Retriever 配置

```python
from langchain.vectorstores import Milvus
from langchain.embeddings import OpenAIEmbeddings

# 基础 Retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",        # 相似度搜索
    search_kwargs={"k": 3}           # 返回 Top-3
)

# 带阈值的 Retriever（过滤低相似度）
retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 5, "score_threshold": 0.5}
)

# MMR（最大边界相关，减少冗余）
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 20, "lambda_mult": 0.5}
)
```

### 2. 搜索类型对比

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| similarity | 标准相似度搜索 | 通用 |
| similarity_score_threshold | 带阈值过滤 | 需要最低相关度 |
| mmr | 最大边界相关 | 减少结果冗余 |

### 3. 完整 RAG 链

```python
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

# 系统 Prompt
system_prompt = """你是股票分析助手。请根据以下上下文回答问题。

如果上下文中有答案，详细解释并引用来源。
如果上下文中没有相关信息，请直接说明"根据现有资料无法回答"。

上下文：
{context}

问题：{input}

请用中文专业但易懂的语言回答。"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# 创建文档处理链
combine_docs_chain = create_stuff_documents_chain(llm, prompt)

# 创建 RAG 链
rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

# 执行
response = rag_chain.invoke({"input": "茅台的投资价值如何？"})

print(f"答案：{response['answer']}")
print(f"引用文档：{len(response['context'])} 篇")
```

### 4. 自定义 Prompt 模板

```python
# 带来源引用的 Prompt
system_prompt = """请基于以下信息回答问题。回答时要引用具体来源。

【文档信息】
{context}

【问题】
{input}

【回答要求】
1. 先给出核心结论
2. 详细解释并标注来源（如"根据 XX 研报"）
3. 如有数据，请列出具体数值
4. 如果信息不足，请说明

请用中文回答。"""
```

### 5. 流式输出

```python
# 流式生成（用户体验更好）
for chunk in rag_chain.stream({"input": "问题..."}):
    print(chunk, end="", flush=True)
```

---

## 实践任务

### 任务 1: 完整 RAG 流程 ✅

```python
# rag_pipeline.py

from langchain.vectorstores import Milvus
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 1. 初始化
embeddings = OpenAIEmbeddings()
vectorstore = Milvus(..., embedding_function=embeddings)
llm = ChatOpenAI(model="gpt-3.5-turbo")

# 2. 创建 Retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 3. 创建 RAG 链
prompt = ChatPromptTemplate.from_messages([
    ("system", "根据上下文回答：{context}"),
    ("human", "{input}"),
])
rag_chain = create_retrieval_chain(retriever, create_stuff_documents_chain(llm, prompt))

# 4. 测试
questions = [
    "茅台的市盈率是多少？",
    "白酒行业发展趋势如何？",
    "新能源股票有哪些推荐？",
]

for q in questions:
    response = rag_chain.invoke({"input": q})
    print(f"\nQ: {q}")
    print(f"A: {response['answer'][:200]}...")
```

### 任务 2: 检索参数调优 ✅

```python
# 测试不同 k 值
for k in [1, 3, 5, 10]:
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    # 测试检索质量和回答质量
```

### 任务 3: RAG 系统评估 ✅

```python
# rag_evaluation.py

# 1. 准备测试集（10-20 个问题 + 标准答案）
# 2. 运行 RAG 系统
# 3. 对比答案质量
# 4. 统计准确率
```

---

## 知识点总结

### RAG 链组件

| 组件 | 作用 |
|------|------|
| Retriever | 检索相关文档 |
| create_stuff_documents_chain | 将文档注入 Prompt |
| create_retrieval_chain | 完整的 RAG 链 |

### 调优技巧

- **k 值**：太小漏信息，太大引入噪声（推荐 3-5）
- **阈值**：过滤低质量匹配（推荐 0.4-0.6）
- **temperature**：低一些更稳定（推荐 0.1-0.3）

---

## 常见问题

### Q1: 检索不到相关内容？
- 检查 Embedding 模型
- 调整 chunk_size
- 增加 k 值

### Q2: 回答太笼统？
- 优化 Prompt，要求更具体
- 增加上下文窗口
- 调整 temperature

### Q3: 如何提升 RAG 效果？
1. 优化文档质量
2. 调整分块策略
3. 使用更好的 Embedding
4. 添加重排序（Rerank）

---

## 代码文件

```
day52_rag_pipeline/
├── README.md
├── rag_pipeline.py            # 完整 RAG 流程
├── parameter_tuning.py        # 参数调优
└── rag_evaluation.py          # 效果评估
```

---

## 参考资源

- [LangChain RAG Chain](https://python.langchain.com/docs/tutorials/rag/)
- [create_retrieval_chain API](https://api.python.langchain.com/)

---

## 下一步

- **Day 53**: RAG 效果评估
- **明日任务**: 学习如何评估和优化 RAG 系统

---

**💡 今日格言**: "RAG 的核心是检索质量决定回答质量"
