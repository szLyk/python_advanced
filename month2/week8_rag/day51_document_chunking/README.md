# Day 51: 文档加载和分块

> **日期**: 2026-05-23（周五）  
> **周次**: Week 8 - RAG 系统  
> **预计耗时**: 2 小时

---

## 今日学习目标

- [ ] 掌握 DocumentLoader 类型
- [ ] 学会 PDF/Text/HTML 加载
- [ ] 理解文本分块策略
- [ ] 了解元数据管理

---

## 学习内容

### 1. DocumentLoader 类型

LangChain 支持多种文档加载器：

| Loader | 格式 | 用法 |
|--------|------|------|
| TextLoader | .txt | `TextLoader("file.txt")` |
| PyPDFLoader | .pdf | `PyPDFLoader("file.pdf")` |
| Docx2txtLoader | .docx | `Docx2txtLoader("file.docx")` |
| UnstructuredMarkdownLoader | .md | `UnstructuredMarkdownLoader("file.md")` |
| WebBaseLoader | 网页 | `WebBaseLoader("https://...")` |
| DirectoryLoader | 目录 | `DirectoryLoader("./docs/")` |

### 2. 文档加载示例

```python
from langchain.document_loaders import (
    TextLoader,
    PyPDFLoader,
    DirectoryLoader,
    WebBaseLoader
)

# 加载单个文件
loader = TextLoader("report.txt", encoding="utf-8")
documents = loader.load()

# 加载 PDF
pdf_loader = PyPDFLoader("annual_report.pdf")
pdf_docs = pdf_loader.load()

# 加载整个目录
dir_loader = DirectoryLoader(
    "./reports/",
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)
all_docs = dir_loader.load()

# 加载网页
web_loader = WebBaseLoader("https://example.com/article")
web_docs = web_loader.load()
```

### 3. 文本分块策略

**为什么需要分块？**
- LLM 上下文长度有限
- 检索时需要精确匹配片段
- 太大→包含噪声，太小→丢失上下文

**常见分块方法**：

```python
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    ChineseTextSplitter
)

# 方法 1: 字符分块（简单但粗糙）
splitter1 = CharacterTextSplitter(
    separator="\n",
    chunk_size=500,
    chunk_overlap=50
)

# 方法 2: 递归字符分块（推荐）
splitter2 = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。", "！", "？", " "],
    chunk_size=500,
    chunk_overlap=50,
    length_function=len
)

# 方法 3: 中文专用分块
splitter3 = ChineseTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
```

### 4. 分块参数调优

```python
# chunk_size: 每块最大字符数
# - 太小：丢失上下文，检索不准确
# - 太大：包含噪声，LLM 处理慢
# 推荐：300-800

# chunk_overlap: 块之间重叠
# - 保持上下文连贯性
# - 推荐：chunk_size 的 10%-20%

# 示例配置
config_map = {
    "短文档/新闻": {"chunk_size": 300, "chunk_overlap": 30},
    "研报/报告": {"chunk_size": 500, "chunk_overlap": 50},
    "书籍/长文": {"chunk_size": 800, "chunk_overlap": 100},
}
```

### 5. 元数据管理

```python
# 加载时自动添加元数据
documents = PyPDFLoader("report.pdf").load()
for doc in documents:
    print(doc.metadata)
    # {'source': 'report.pdf', 'page': 0, 'total_pages': 10}

# 自定义元数据
loader = TextLoader("file.txt", encoding="utf-8", metadata={"category": "news", "year": 2024})

# 分块后保留元数据
chunks = splitter.split_documents(documents)
# 每个 chunk 都继承原文档的 metadata
```

---

## 实践任务

### 任务 1: 文档加载练习 ✅

```python
# document_chunking.py

from langchain.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader

# 1. 加载 TXT
txt_docs = TextLoader("data/sample.txt", encoding="utf-8").load()
print(f"TXT: {len(txt_docs)} 个文档")

# 2. 加载 PDF
pdf_docs = PyPDFLoader("data/sample.pdf").load()
print(f"PDF: {len(pdf_docs)} 个页面")

# 3. 加载目录
dir_docs = DirectoryLoader(
    "data/reports/",
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
).load()
print(f"目录：{len(dir_docs)} 个文档")
```

### 任务 2: 文本分块对比 ✅

```python
# 测试不同分块策略
from langchain.text_splitter import RecursiveCharacterTextSplitter

text = "这是一篇很长的文章..." * 100

# 不同配置
configs = [
    {"chunk_size": 200, "chunk_overlap": 20},
    {"chunk_size": 500, "chunk_overlap": 50},
    {"chunk_size": 1000, "chunk_overlap": 100},
]

for config in configs:
    splitter = RecursiveCharacterTextSplitter(**config)
    chunks = splitter.split_text(text)
    print(f"{config}: {len(chunks)} 个块")
```

### 任务 3: 股票文档处理 ✅

```python
# stock_document_processing.py

# 1. 加载股票研报（PDF/TXT）
# 2. 使用合适的分块策略
# 3. 保留元数据（来源、行业、日期）
# 4. 输出统计信息
```

---

## 知识点总结

| 组件 | 推荐配置 |
|------|----------|
| 文档加载 | 根据格式选择 Loader |
| 分块方法 | RecursiveCharacterTextSplitter |
| chunk_size | 500（通用）、300（新闻）、800（报告） |
| chunk_overlap | chunk_size 的 10%-20% |
| 分隔符 | `["\n\n", "\n", "。", "！", "？"]` |

---

## 常见问题

### Q1: 分块后找不到内容？
- chunk_size 太小，信息被切散了
- 增大 chunk_size 或使用更智能的分隔符

### Q2: 检索效果差？
- 检查 Embedding 质量
- 调整 chunk_size
- 增加检索数量 k

### Q3: 中文乱码？
```python
# 指定编码
TextLoader("file.txt", encoding="utf-8")
```

---

## 代码文件

```
day51_document_chunking/
├── README.md
├── document_chunking.py       # 文档加载和分块
├── splitter_comparison.py     # 分块策略对比
└── stock_document_processing.py
```

---

## 参考资源

- [LangChain Document Loaders](https://python.langchain.com/docs/integrations/document_loaders)
- [LangChain Text Splitters](https://python.langchain.com/docs/integrations/text_splitters)

---

## 下一步

- **Day 52**: 检索 + 生成（完整 RAG 流程）
- **明日任务**: 实现端到端 RAG 系统

---

**💡 今日格言**: "好的分块 = 检索成功的一半"
