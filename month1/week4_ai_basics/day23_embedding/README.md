# Day 23: Embedding 词向量与句向量

## 学习目标

理解 Embedding（嵌入）的概念和应用，为后续向量数据库和 RAG 系统打下基础。

## 知识点

### 1. Embedding 概念

Embedding 是将文本转换为数值向量的技术：

```
文本: "股票上涨"
    ↓
Embedding 模型
    ↓
向量: [0.12, -0.34, 0.56, ..., 0.78]  (通常 512-1536 维)

核心思想：
- 相似含义的词 → 相似的向量
- 向量之间的距离表示语义相似度
```

### 2. 词向量发展历程

```
传统方法（2013前）
├── One-Hot 编码（稀疏、无语义）
└── TF-IDF（词频统计）

Word2Vec（2013）
├── Skip-gram：预测上下文
└── CBOW：根据上下文预测词

GloVe（2014）
└── 基于全局词共现统计

FastText（2016）
└── 子词嵌入，支持未登录词

BERT（2018）
└── 上下文相关的动态嵌入

现代 Embedding 模型
├── OpenAI text-embedding-ada-002
├── Sentence-BERT
├── BGE (BAAI)
└── E5 (Microsoft)
```

### 3. Word2Vec 原理

```python
# Skip-gram 模型
# 给定中心词，预测周围词

输入: "我 爱 编 程"
中心词: "爱"
上下文窗口: 2（前后各2个词）
预测目标: "我", "编", "程"

# CBOW 模型
# 给定上下文，预测中心词

输入上下文: "我", "编", "程"
预测中心词: "爱"

# 训练后，每个词获得一个向量表示
```

### 4. 常用 Embedding 模型

| 模型 | 维度 | 特点 | 用途 |
|------|------|------|------|
| OpenAI ada-002 | 1536 | 高质量、API调用 | 通用 |
| BGE-large | 1024 | 中文优秀、开源 | 中文场景 |
| E5-large | 1024 | 多语言支持 | 国际化 |
| sentence-bert | 768 | sentence级别 | 语义搜索 |

### 5. 向量相似度计算

```python
import numpy as np

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    余弦相似度（最常用）

    similarity = (a · b) / (|a| · |b|)
    范围: [-1, 1]，越大越相似
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    """
    欧氏距离

    distance = sqrt(sum((a_i - b_i)^2))
    范围: [0, ∞]，越小越相似
    """
    return np.linalg.norm(a - b)

def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    """
    点积（简单但不够标准）

    dot = a · b
    """
    return np.dot(a, b)
```

### 6. Embedding 应用场景

```
1. 语义搜索
   - 用户查询 → 向量
   - 文档库 → 向量索引
   - 查找最相似的文档

2. 推荐系统
   - 用户兴趣 → 向量
   - 内容 → 向量
   - 匹配相似内容

3. 聚类分析
   - 文本 → 向量
   - K-means 聚类
   - 发现主题分组

4. 文本分类
   - 文本 → 向量
   - 训练分类器
   - 情感/主题分类

5. RAG 系统
   - 知识库 → 向量存储
   - 查询 → 向量检索
   - 检索结果 + LLM → 回答
```

### 7. 使用 OpenAI Embedding

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

def get_embedding(text: str) -> list:
    """获取文本的 Embedding"""
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding

# 示例
text = "苹果公司发布新产品"
embedding = get_embedding(text)
print(f"向量维度: {len(embedding)}")  # 1536
```

### 8. 使用本地 Embedding 模型

```python
from sentence_transformers import SentenceTransformer

# 加载模型
model = SentenceTransformer('BAAI/bge-large-zh-v1.5')

# 生成 Embedding
texts = ["股票上涨", "股市下跌", "苹果公司"]
embeddings = model.encode(texts)

print(f"向量形状: {embeddings.shape}")  # (3, 1024)

# 计算相似度
similarity = cosine_similarity(embeddings[0], embeddings[1])
print(f"'股票上涨' vs '股市下跌' 相似度: {similarity:.3f}")
```

### 9. Embedding 最佳实践

```python
# 文本预处理
def preprocess_text(text: str) -> str:
    """预处理文本以提高 Embedding 质量"""
    # 去除多余空格
    text = text.strip()
    # 统一大小写（视模型而定）
    text = text.lower()
    # 处理特殊字符
    text = text.replace('\n', ' ')
    return text

# 批量处理
def batch_encode(texts: list, batch_size: int = 100):
    """批量生成 Embedding"""
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        batch_embeddings = model.encode(batch)
        embeddings.extend(batch_embeddings)
    return embeddings

# 文本分块（长文档）
def chunk_text(text: str, max_length: int = 500):
    """将长文本分块"""
    chunks = []
    for i in range(0, len(text), max_length):
        chunks.append(text[i:i+max_length])
    return chunks
```

## 练习任务

1. 理解 Word2Vec 的 Skip-gram 和 CBOW
2. 实现余弦相似度计算
3. 使用本地模型生成 Embedding
4. 计算不同文本之间的相似度
5. 实现简单的语义搜索

## 股票场景应用

```python
# 新闻相似度分析
news = [
    "苹果公司股价大涨",
    "特斯拉市值创新高",
    "科技股普遍下跌",
    "汽车行业迎来利好"
]

embeddings = model.encode(news)

# 找最相似的新闻
for i, title1 in enumerate(news):
    for j, title2 in enumerate(news):
        if i < j:
            sim = cosine_similarity(embeddings[i], embeddings[j])
            print(f"{title1} vs {title2}: {sim:.3f}")
```

## 运行练习

```bash
# 安装依赖
pip install sentence-transformers numpy

# 运行
python embedding_concept.py
```

## 参考资料

- Word2Vec 论文：Efficient Estimation of Word Representations (2013)
- Sentence-BERT：https://www.sbert.net/
- BGE 模型：https://huggingface.co/BAAI/bge-large-zh-v1.5
- OpenAI Embedding：https://platform.openai.com/docs/guides/embeddings