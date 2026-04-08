# Day 48: 综合项目 - 股票研报检索系统

> **日期**: 2026-05-20（周二）  
> **周次**: Week 7 - 向量数据库  
> **预计耗时**: 6 小时

---

## 项目目标

创建一个股票研报检索系统，能够：

- [ ] 加载 PDF/TXT 研报文档
- [ ] 自动分块和向量化
- [ ] 语义检索相关研报
- [ ] 返回带来源的检索结果

---

## 项目架构

```
┌─────────────────────────────────────────────────────────┐
│              股票研报检索系统架构                        │
├─────────────────────────────────────────────────────────┤
│  文档层                                                  │
│  PDF研报 | TXT新闻 | Word报告 | HTML网页                 │
│       ↓                                                  │
│  处理层                                                  │
│  文档加载 → 文本分块 → Embedding 向量化                    │
│       ↓                                                  │
│  存储层                                                  │
│  Milvus 向量数据库 (向量 + 元数据)                        │
│       ↓                                                  │
│  检索层                                                  │
│  用户查询 → 向量化 → 相似度搜索 → 返回结果                │
│       ↓                                                  │
│  应用层                                                  │
│  CLI界面 | Web界面 | API接口                              │
└─────────────────────────────────────────────────────────┘
```

---

## 项目结构

```
day48_stock_report_search/
├── README.md                      # 本文件
├── main.py                        # 主程序入口
├── loader/
│   ├── pdf_loader.py              # PDF 文档加载
│   ├── txt_loader.py              # TXT 文档加载
│   └── document_loader.py         # 统一加载接口
├── chunking/
│   └── text_splitter.py           # 文本分块
├── vector_store/
│   ├── milvus_store.py            # Milvus 存储
│   └── embedding_model.py         # Embedding 配置
├── retrieval/
│   ├── retriever.py               # 检索器
│   └── reranker.py                # 重排序（可选）
└── data/
    └── sample_reports/            # 示例研报
```

---

## 实现步骤

### Step 1: 文档加载器

```python
# loader/document_loader.py

from langchain.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
    WebBaseLoader
)
import os

class StockReportLoader:
    """股票研报加载器"""
    
    @staticmethod
    def load_pdf(file_path: str):
        """加载 PDF 文档"""
        loader = PyPDFLoader(file_path)
        return loader.load()
    
    @staticmethod
    def load_txt(file_path: str):
        """加载 TXT 文档"""
        loader = TextLoader(file_path, encoding='utf-8')
        return loader.load()
    
    @staticmethod
    def load_directory(dir_path: str, ext: str = ".txt"):
        """加载目录下所有文档"""
        from langchain.document_loaders import DirectoryLoader
        loader = DirectoryLoader(
            dir_path,
            glob=f"**/*{ext}",
            loader_cls=TextLoader,
            loader_kwargs={'encoding': 'utf-8'}
        )
        return loader.load()
```

### Step 2: 文本分块

```python
# chunking/text_splitter.py

from langchain.text_splitter import RecursiveCharacterTextSplitter

def create_text_splitter(
    chunk_size: int = 500,
    chunk_overlap: int = 50
):
    """
    创建文本分块器
    
    Args:
        chunk_size: 每块最大字符数
        chunk_overlap: 块之间重叠字符数
    """
    return RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", "！", "？", "；", " "],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False
    )

# 使用示例
splitter = create_text_splitter()
chunks = splitter.split_documents(documents)
```

### Step 3: VectorStore 创建

```python
# vector_store/milvus_store.py

from langchain.vectorstores import Milvus
from langchain.embeddings import OpenAIEmbeddings
from pymilvus import connections

class StockVectorStore:
    """股票向量存储"""
    
    def __init__(self, collection_name: str = "stock_reports"):
        self.collection_name = collection_name
        self.embeddings = self._create_embeddings()
        self.vectorstore = None
    
    def _create_embeddings(self):
        """创建 Embedding 模型"""
        return OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_base="https://api.deepseek.com",
            openai_api_key="sk-xxx"
        )
    
    def create_collection(self, documents):
        """从文档创建 Collection"""
        # 连接 Milvus
        connections.connect(host="localhost", port="19530")
        
        self.vectorstore = Milvus.from_documents(
            documents=documents,
            embedding=self.embeddings,
            connection_args={"host": "localhost", "port": "19530"},
            collection_name=self.collection_name,
            drop_old=True  # 如果已存在则删除重建
        )
        
        print(f"✅ Collection '{self.collection_name}' 创建成功")
        return self.vectorstore
    
    def load_collection(self):
        """加载现有 Collection"""
        connections.connect(host="localhost", port="19530")
        
        self.vectorstore = Milvus(
            embedding_function=self.embeddings,
            connection_args={"host": "localhost", "port": "19530"},
            collection_name=self.collection_name,
        )
        
        print(f"✅ Collection '{self.collection_name}' 加载成功")
        return self.vectorstore
    
    def get_retriever(self, k: int = 3):
        """获取检索器"""
        return self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        )
```

### Step 4: 检索器

```python
# retrieval/retriever.py

from typing import List
from langchain.schema import Document

class StockReportRetriever:
    """股票研报检索器"""
    
    def __init__(self, vectorstore):
        self.retriever = vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 5, "score_threshold": 0.5}
        )
    
    def search(self, query: str) -> List[Document]:
        """
        搜索相关研报
        
        Args:
            query: 查询语句
        
        Returns:
            相关文档列表
        """
        docs = self.retriever.invoke(query)
        
        print(f"🔍 找到 {len(docs)} 篇相关研报:")
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "未知")
            content = doc.page_content[:100] + "..."
            print(f"\n[{i}] 来源：{source}")
            print(f"    内容：{content}")
        
        return docs
```

### Step 5: 主程序

```python
# main.py

from loader.document_loader import StockReportLoader
from chunking.text_splitter import create_text_splitter
from vector_store.milvus_store import StockVectorStore
from retrieval.retriever import StockReportRetriever

def build_index(data_dir: str):
    """构建索引"""
    print("📚 加载文档...")
    documents = StockReportLoader.load_directory(data_dir)
    print(f"已加载 {len(documents)} 篇文档")
    
    print("\n✂️  文本分块...")
    splitter = create_text_splitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    print(f"分成 {len(chunks)} 个文本块")
    
    print("\n💾 创建向量索引...")
    vector_store = StockVectorStore(collection_name="stock_reports")
    vector_store.create_collection(chunks)
    
    print("\n✅ 索引构建完成！")
    return vector_store

def search_reports(query: str, retriever: StockReportRetriever):
    """搜索研报"""
    print(f"\n🔍 查询：{query}")
    print("=" * 60)
    results = retriever.search(query)
    return results

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--build":
        # 构建索引模式
        data_dir = "data/sample_reports"
        vector_store = build_index(data_dir)
    else:
        # 搜索模式
        vector_store = StockVectorStore()
        vector_store.load_collection()
        retriever = StockReportRetriever(vector_store.vectorstore)
        
        print("=" * 60)
        print("📈 股票研报检索系统")
        print("=" * 60)
        print("输入查询语句进行搜索（输入'退出'结束）\n")
        
        while True:
            query = input("🔍 请输入：").strip()
            if query.lower() in ["退出", "exit", "quit"]:
                print("👋 再见！")
                break
            if not query:
                continue
            search_reports(query, retriever)

if __name__ == "__main__":
    main()
```

---

## 运行测试

```bash
# 1. 构建索引
python main.py --build

# 2. 搜索研报
python main.py

# 示例查询：
# - "茅台的投资价值"
# - "新能源行业分析"
# - "白酒行业趋势"
```

---

## 项目检查清单

- [ ] 文档加载正常
- [ ] 文本分块合理
- [ ] 向量索引创建成功
- [ ] 检索结果相关
- [ ] 错误处理完善
- [ ] 代码已提交 GitHub

---

## 扩展功能

### 扩展 1: 添加来源引用
```python
# 在检索结果中显示具体来源页码
for doc in results:
    print(f"来源：{doc.metadata['source']}, 页码：{doc.metadata['page']}")
```

### 扩展 2: 多条件过滤
```python
# 按行业/时间过滤
retriever = vectorstore.as_retriever(
    search_kwargs={
        "filter": {"industry": "白酒", "year": 2024}
    }
)
```

### 扩展 3: Web 界面
```python
# 使用 Streamlit 创建 Web 界面
import streamlit as st
# ...
```

---

## 参考资源

- [LangChain Document Loaders](https://python.langchain.com/docs/integrations/document_loaders)
- [LangChain Text Splitters](https://python.langchain.com/docs/integrations/text_splitters)

---

## 下一步

- **Week 8**: RAG 系统
- **Day 50**: RAG 原理和基础实现

---

**🎉 恭喜完成 Week 7！你已掌握向量数据库的核心技能！**
