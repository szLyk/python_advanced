# Day 46: LangChain 集成

> **日期**: 2026-05-18（周日）  
> **周次**: Week 7 - 向量数据库  
> **预计耗时**: 2 小时

---

## 今日学习目标

- [ ] 掌握 LangChain VectorStore 接口
- [ ] 学会 Milvus 向量存储
- [ ] 实现相似度搜索链
- [ ] 了解文档检索流程

---

## 学习内容

### 1. LangChain VectorStore 接口

VectorStore 是 LangChain 统一向量数据库操作的抽象层：

```python
from langchain.vectorstores import Milvus
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter

# 初始化 Embedding 模型
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 创建/加载 VectorStore
vectorstore = Milvus(
    embedding_function=embeddings,
    connection_args={"host": "localhost", "port": "19530"},
    collection_name="langchain_demo",
    auto_id=True,
)

# 添加文档
texts = ["股票投资基础知识", "如何分析公司财报", "技术分析入门"]
vectorstore.add_texts(texts)

# 相似度搜索
results = vectorstore.similarity_search("怎么学炒股", k=2)
print(results)
```

### 2. 从文档创建 VectorStore

```python
from langchain.schema import Document
from langchain.vectorstores import Milvus
from langchain.embeddings import OpenAIEmbeddings

# 准备文档
documents = [
    Document(
        page_content="贵州茅台是白酒龙头企业，成立于 1999 年",
        metadata={"stock_code": "600519", "category": "白酒"}
    ),
    Document(
        page_content="五粮液是浓香型白酒的代表产品",
        metadata={"stock_code": "000858", "category": "白酒"}
    ),
]

# 创建 VectorStore
embeddings = OpenAIEmbeddings()
vectorstore = Milvus.from_documents(
    documents=documents,
    embedding=embeddings,
    connection_args={"host": "localhost", "port": "19530"},
    collection_name="stock_knowledge",
)
```

### 3. Retriever（检索器）

Retriever 是 LangChain 的检索接口，可与 Chain/Agent 集成：

```python
# 获取 Retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",  # 相似度搜索
    search_kwargs={"k": 3}     # 返回 Top-3
)

# 检索相关文档
docs = retriever.invoke("茅台的相关信息")
for doc in docs:
    print(doc.page_content)
```

### 4. RAG 链（检索 + 生成）

```python
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# LLM
llm = ChatOpenAI(model="gpt-3.5-turbo")

# 系统 Prompt
system_prompt = """你是股票知识助手。请根据以下上下文回答问题。

上下文：{context}

问题：{input}

请用中文回答。"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# 创建文档处理链
question_answer_chain = create_stuff_documents_chain(llm, prompt)

# 创建 RAG 链
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# 执行
response = rag_chain.invoke({"input": "茅台是什么公司？"})
print(response["answer"])
```

### 5. 带过滤的检索

```python
# 按元数据过滤
retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 3,
        "filter": {"stock_code": "600519"}  # 只查茅台
    }
)

# 多条件过滤
retriever = vectorstore.as_retriever(
    search_kwargs={
        "filter": {"category": "白酒", "year": 2024}
    }
)
```

---

## 实践任务

### 任务 1: VectorStore 基础 ✅

```python
# langchain_vectorstore.py

from langchain.vectorstores import Milvus
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document

# 连接 Milvus
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key="xxx",
    openai_api_base="https://api.deepseek.com"
)

# 创建文档
docs = [
    Document(page_content="茅台是白酒龙头", metadata={"code": "600519"}),
    Document(page_content="五粮液是浓香白酒", metadata={"code": "000858"}),
]

# 存入 VectorStore
vectorstore = Milvus.from_documents(
    docs,
    embeddings,
    connection_args={"host": "localhost", "port": "19530"},
    collection_name="test",
    drop_old=True
)

# 搜索
results = vectorstore.similarity_search("白酒股票", k=2)
print(results[0].page_content)
```

### 任务 2: RAG 问答链 ✅

```python
# rag_chain.py

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")
retriever = vectorstore.as_retriever()

prompt = ChatPromptTemplate.from_messages([
    ("system", "根据上下文回答：{context}"),
    ("human", "{input}"),
])

chain = create_retrieval_chain(retriever, create_stuff_documents_chain(llm, prompt))
response = chain.invoke({"input": "茅台是做什么的？"})
print(response["answer"])
```

### 任务 3: 股票文档检索 ✅

```python
# stock_document_retriever.py

# 加载股票研报/新闻
# 创建 VectorStore
# 实现语义检索
# 测试不同查询
```

---

## 知识点总结

| 组件 | 作用 |
|------|------|
| VectorStore | 向量存储抽象层 |
| Embedding | 文本向量化 |
| Retriever | 检索接口 |
| create_retrieval_chain | RAG 链 |

---

## 代码文件

```
day46_langchain_vectorstore/
├── README.md
├── langchain_vectorstore.py
├── rag_chain.py
├── stock_retriever.py
└── requirements.txt
```

---

## 参考资源

- [LangChain VectorStore](https://python.langchain.com/docs/integrations/vectorstores/milvus)
- [LangChain RAG](https://python.langchain.com/docs/use_cases/question_answering)

---

## 下一步

- **Day 47**: 复习/补进度
- **Day 48**: 综合项目 - 股票研报检索系统

---

**💡 今日格言**: "LangChain 让向量检索变得简单"
