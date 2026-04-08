# Day 55: 综合项目 - 股票知识库 RAG 系统

> **日期**: 2026-05-27（周二）  
> **周次**: Week 8 - RAG 系统  
> **预计耗时**: 6 小时

---

## 项目目标

创建一个完整的股票知识库 RAG 系统，能够：

- [ ] 加载多种来源的股票数据
- [ ] 构建向量索引
- [ ] 实现语义检索和问答
- [ ] 提供来源引用
- [ ] 支持多轮对话

---

## 项目架构

```
┌─────────────────────────────────────────────────────────┐
│            股票知识库 RAG 系统架构                       │
├─────────────────────────────────────────────────────────┤
│  数据源层                                                │
│  研报 PDF | 新闻 TXT | 百科数据 | 财经文章              │
│       ↓                                                  │
│  处理层                                                  │
│  文档加载 → 分块 → Embedding → 向量存储                 │
│       ↓                                                  │
│  检索层                                                  │
│  问题理解 → 向量化 → 相似度搜索 → 重排序                │
│       ↓                                                  │
│  生成层                                                  │
│  上下文组装 → Prompt 构建 → LLM 生成 → 答案输出            │
│       ↓                                                  │
│  应用层                                                  │
│  CLI 界面 | Web 界面 | API 接口                            │
└─────────────────────────────────────────────────────────┘
```

---

## 项目结构

```
day55_stock_knowledge_rag/
├── README.md                      # 本文件
├── main.py                        # 主程序入口
├── knowledge_base/
│   ├── stock_reports/             # 研报文件
│   ├── stock_wiki/                # 百科数据
│   └── stock_news/                # 新闻资讯
├── retrieval/
│   ├── retriever.py               # 检索器配置
│   └── reranker.py                # 重排序模块
├── generation/
│   ├── answer_generator.py        # 答案生成
│   └── prompt_templates.py        # Prompt 模板
├── vector_store/
│   ├── milvus_store.py            # Milvus 配置
│   └── embedding_model.py         # Embedding 模型
└── utils/
    ├── document_loader.py         # 文档加载
    └── text_splitter.py           # 文本分块
```

---

## 实现步骤

### Step 1: 知识库数据准备

```python
# knowledge_base/ 目录结构
knowledge_base/
├── stock_reports/           # 研报
│   ├── maotai_research.pdf
│   ├── wuliangye_analysis.pdf
│   └── baijiu_industry.pdf
├── stock_wiki/              # 百科
│   ├── pe_ratio.txt         # 市盈率解释
│   ├── pb_ratio.txt         # 市净率解释
│   └── roe.txt              # ROE 解释
└── stock_news/              # 新闻
    ├── 2024-05_news.txt
    └── ...
```

### Step 2: 文档加载和分块

```python
# utils/document_loader.py

from langchain.document_loaders import (
    PyPDFLoader,
    TextLoader,
    DirectoryLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_all_documents(data_dir: str):
    """加载所有文档"""
    all_docs = []
    
    # 加载研报
    pdf_loader = DirectoryLoader(
        f"{data_dir}/stock_reports/",
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )
    all_docs.extend(pdf_loader.load())
    
    # 加载百科
    txt_loader = DirectoryLoader(
        f"{data_dir}/stock_wiki/",
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    all_docs.extend(txt_loader.load())
    
    # 加载新闻
    news_loader = DirectoryLoader(
        f"{data_dir}/stock_news/",
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    all_docs.extend(news_loader.load())
    
    print(f"共加载 {len(all_docs)} 个文档")
    return all_docs

def split_documents(docs):
    """分块处理"""
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", "！", "？"],
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)
    print(f"分成 {len(chunks)} 个文本块")
    return chunks
```

### Step 3: VectorStore 创建

```python
# vector_store/milvus_store.py

from langchain.vectorstores import Milvus
from langchain.embeddings import OpenAIEmbeddings
from pymilvus import connections

def create_vector_store(documents, collection_name: str = "stock_knowledge"):
    """创建向量存储"""
    
    # Embedding 模型
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_base="https://api.deepseek.com",
        openai_api_key="sk-xxx"
    )
    
    # 连接 Milvus
    connections.connect(host="localhost", port="19530")
    
    # 创建 Collection
    vectorstore = Milvus.from_documents(
        documents=documents,
        embedding=embeddings,
        connection_args={"host": "localhost", "port": "19530"},
        collection_name=collection_name,
        drop_old=True
    )
    
    print(f"✅ VectorStore '{collection_name}' 创建成功")
    return vectorstore
```

### Step 4: 检索器配置

```python
# retrieval/retriever.py

def create_retriever(vectorstore, k: int = 5, score_threshold: float = 0.5):
    """创建检索器"""
    
    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": k,
            "score_threshold": score_threshold
        }
    )
    
    return retriever
```

### Step 5: RAG 链创建

```python
# generation/answer_generator.py

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

def create_rag_chain(retriever):
    """创建完整 RAG 链"""
    
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.3
    )
    
    system_prompt = """你是股票知识助手 RAG 系统。请根据以下上下文回答问题。

【上下文信息】
{context}

【用户问题】
{input}

【回答要求】
1. 先给出核心结论（1-2 句话）
2. 详细解释并引用来源（如"根据 XX 研报"）
3. 如有数据请列出具体数值
4. 如果上下文中没有答案，请说明"资料不足"
5. 保持专业但易懂的风格

请用中文回答。"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # 创建文档处理链
    combine_chain = create_stuff_documents_chain(llm, prompt)
    
    # 创建 RAG 链
    rag_chain = create_retrieval_chain(retriever, combine_chain)
    
    return rag_chain
```

### Step 6: 主程序

```python
# main.py

import sys
from utils.document_loader import load_all_documents, split_documents
from vector_store.milvus_store import create_vector_store
from retrieval.retriever import create_retriever
from generation.answer_generator import create_rag_chain

def build_knowledge_base(data_dir: str = "knowledge_base"):
    """构建知识库"""
    print("📚 步骤 1: 加载文档...")
    docs = load_all_documents(data_dir)
    
    print("\n✂️  步骤 2: 文本分块...")
    chunks = split_documents(docs)
    
    print("\n💾 步骤 3: 创建向量索引...")
    vectorstore = create_vector_store(chunks)
    
    print("\n✅ 知识库构建完成！")
    return vectorstore

def run_qa(vectorstore):
    """运行问答系统"""
    print("\n🔍 创建检索器...")
    retriever = create_retriever(vectorstore)
    
    print("\n🤖 创建 RAG 链...")
    rag_chain = create_rag_chain(retriever)
    
    print("\n" + "=" * 60)
    print("📈 股票知识库 RAG 系统")
    print("=" * 60)
    print("输入问题开始问答（输入'退出'结束）\n")
    
    while True:
        query = input("🔍 请输入：").strip()
        if query.lower() in ["退出", "exit", "quit"]:
            print("👋 再见！")
            break
        if not query:
            continue
        
        try:
            response = rag_chain.invoke({"input": query})
            print(f"\n🤖 {response['answer']}")
            print(f"\n📚 参考来源：{len(response['context'])} 篇文档")
        except Exception as e:
            print(f"\n❌ 错误：{e}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--build":
        # 构建知识库
        build_knowledge_base()
    else:
        # 运行问答系统
        from vector_store.milvus_store import Milvus, OpenAIEmbeddings, connections
        
        embeddings = OpenAIEmbeddings()
        connections.connect(host="localhost", port="19530")
        
        vectorstore = Milvus(
            embedding_function=embeddings,
            connection_args={"host": "localhost", "port": "19530"},
            collection_name="stock_knowledge"
        )
        
        run_qa(vectorstore)

if __name__ == "__main__":
    main()
```

---

## 运行测试

```bash
# 1. 构建知识库
python main.py --build

# 2. 运行问答
python main.py

# 示例问题：
# - "市盈率是什么意思？"
# - "茅台的投资价值如何？"
# - "白酒行业 2024 年发展趋势？"
```

---

## 项目检查清单

- [ ] 知识库数据准备完成
- [ ] 文档加载正常
- [ ] 向量索引创建成功
- [ ] 检索结果相关
- [ ] 回答准确有来源
- [ ] 错误处理完善
- [ ] 代码已提交 GitHub

---

## 扩展功能

### 扩展 1: 对话历史
```python
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(...)
# 支持多轮对话
```

### 扩展 2: Web 界面
```python
# 使用 Streamlit
import streamlit as st
st.title("股票知识库 RAG 系统")
```

### 扩展 3: API 接口
```python
# 使用 FastAPI
from fastapi import FastAPI
app = FastAPI()
```

---

## 参考资源

- [LangChain RAG 教程](https://python.langchain.com/docs/tutorials/rag/)
- [Milvus 最佳实践](https://milvus.io/docs)

---

## 下一步

- **Week 9**: AutoGen 多 Agent 协作
- **Day 57**: AutoGen 基础

---

**🎉 恭喜完成 Month 2！你已掌握 LangChain + Agent + RAG 的核心能力！**
