# Day 43: 向量数据库概念

> **日期**: 2026-05-15（周四）  
> **周次**: Week 7 - 向量数据库  
> **预计耗时**: 2 小时

---

## 今日学习目标

- [ ] 理解 Embedding 原理
- [ ] 掌握向量相似度计算
- [ ] 了解向量数据库的作用
- [ ] 对比常见向量数据库

---

## 学习内容

### 1. 什么是 Embedding？

**Embedding = 将任意事物映射为向量（一串数字）**

```
文本 → Embedding 模型 → 向量 [0.1, -0.5, 0.8, ...]

"国王" → [0.85, 0.23, -0.12, ...]
"王后" → [0.82, 0.25, -0.10, ...]
"男人" → [0.75, -0.45, 0.32, ...]
"女人" → [0.72, -0.48, 0.35, ...]
```

**关键特性**：语义相似的文本，向量也相似

```
"我喜欢股票"  → [0.1, 0.8, -0.3, ...]
"我想买股票"  → [0.15, 0.75, -0.28, ...]  ← 非常接近！

"今天天气不错" → [-0.5, -0.2, 0.9, ...]  ← 距离很远
```

### 2. 向量相似度计算

**余弦相似度（Cosine Similarity）**：
```python
import numpy as np

def cosine_similarity(v1, v2):
    """计算余弦相似度，结果范围 [-1, 1]"""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2)

# 示例
v1 = [0.1, 0.8, -0.3]
v2 = [0.15, 0.75, -0.28]
v3 = [-0.5, -0.2, 0.9]

print(cosine_similarity(v1, v2))  # 0.98 ← 非常相似
print(cosine_similarity(v1, v3))  # -0.85 ← 很不相似
```

**其他相似度指标**：
- **欧氏距离**：向量间的直线距离
- **内积**：向量点乘结果
- **汉明距离**：二进制向量使用

### 3. 向量数据库的作用

**传统数据库 vs 向量数据库**：

| 传统数据库 | 向量数据库 |
|------------|------------|
| 存储结构化数据 | 存储向量 |
| 精确匹配查询 | 相似度搜索 |
| `WHERE id = 1` | `最相似的 Top-K` |

**向量数据库的核心功能**：
```
1. 存储：高效存储大量向量
2. 索引：建立快速检索索引
3. 搜索：查找最相似的向量
4. 过滤：结合元数据过滤
```

### 4. 常见向量数据库对比

| 数据库 | 特点 | 适用场景 |
|--------|------|----------|
| **Milvus** | 开源、功能全、易部署 | 通用场景，推荐入门 |
| **Pinecone** | 托管服务、免运维 | 快速原型、小团队 |
| **Weaviate** | 内置 NLP、图数据库 | 知识图谱 |
| **Chroma** | 轻量、内存级 | 开发测试、小规模 |
| **FAISS** | Facebook 开源、速度最快 | 超大规模、离线场景 |

### 5. 向量搜索流程

```
┌─────────────────────────────────────────────────────────┐
│              向量搜索完整流程                            │
├─────────────────────────────────────────────────────────┤
│  1. 文档加载                                             │
│     "贵州茅台是白酒龙头企业..."                          │
│                          ↓                              │
│  2. 文本分块                                             │
│     ["贵州茅台...", "成立于 1999 年...", "主要产品..."]    │
│                          ↓                              │
│  3. Embedding 向量化                                      │
│     [[0.1,0.8,...], [0.3,0.5,...], ...]                 │
│                          ↓                              │
│  4. 存入向量数据库                                        │
│     向量 + 元数据（来源、时间等）                         │
│                          ↓                              │
│  5. 查询：用户问题向量化                                  │
│     "茅台是做什么的？" → [0.2, 0.7, ...]                │
│                          ↓                              │
│  6. 相似度搜索                                            │
│     找到最相似的 Top-K 向量                              │
│                          ↓                              │
│  7. 返回原始文本                                         │
│     "贵州茅台是白酒龙头企业..."                          │
└─────────────────────────────────────────────────────────┘
```

---

## 实践任务

### 任务 1: 计算文本相似度 ✅

```python
# embedding_basic.py

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 模拟 Embedding（实际应使用模型生成）
embeddings = {
    "股票投资": [0.8, 0.6, -0.2],
    "买股票": [0.75, 0.65, -0.18],
    "天气预报": [-0.3, -0.5, 0.8],
    "基金理财": [0.7, 0.5, -0.1],
}

# 计算相似度
v1 = embeddings["股票投资"]
v2 = embeddings["买股票"]
v3 = embeddings["天气预报"]

sim_12 = cosine_similarity([v1], [v2])[0][0]
sim_13 = cosine_similarity([v1], [v3])[0][0]

print(f"'股票投资' vs '买股票': {sim_12:.4f}")  # 应该很高
print(f"'股票投资' vs '天气预报': {sim_13:.4f}")  # 应该很低
```

### 任务 2: 使用真实 Embedding 模型 ✅

```python
# real_embedding.py

from sentence_transformers import SentenceTransformer

# 加载模型
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# 生成 Embedding
sentences = [
    "贵州茅台是白酒龙头企业",
    "五粮液生产浓香型白酒",
    "今天天气很好",
]
embeddings = model.encode(sentences)

# 计算相似度
sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
print(f"茅台 vs 五粮液：{sim:.4f}")  # 应该较高
```

### 任务 3: 股票文本相似度分析 ✅

```python
# stock_similarity.py

# 收集 10 条股票相关新闻/评论
# 计算两两相似度
# 找出最相似和最不相似的配对

# 输出：
# 最相似：新闻 A vs 新闻 B (0.92)
# 最不相似：新闻 C vs 新闻 D (0.15)
```

---

## 知识点总结

| 概念 | 说明 |
|------|------|
| Embedding | 将文本/图像等映射为向量 |
| 余弦相似度 | 衡量向量夹角的余弦值 |
| 向量搜索 | 查找最相似的 Top-K 结果 |
| 索引 | 加速相似度搜索的数据结构 |

### Embedding 模型推荐

| 模型 | 维度 | 速度 | 效果 |
|------|------|------|------|
| text-embedding-3-small | 1536 | 快 | 好 |
| text-embedding-3-large | 3072 | 中 | 最好 |
| paraphrase-MiniLM-L6-v2 | 384 | 最快 | 良好 |
| m3e-base | 768 | 快 | 中文友好 |

---

## 常见问题

### Q1: 为什么不用关键词匹配？

```
关键词匹配：
- "苹果股票" 匹配不到 "AAPL 股价"
- "PE 高吗" 匹配不到 "市盈率多少"

语义搜索（向量）：
- "苹果股票" ≈ "AAPL 股价" ✓
- "PE 高吗" ≈ "市盈率多少" ✓
```

### Q2: Embedding 模型怎么选？

- **中文场景**：m3e-base、text2vec
- **英文场景**：OpenAI Embedding、MiniLM
- **多语言**：m3e、multilingual-E5
- **速度优先**：MiniLM-L6-v2

### Q3: 向量维度越高越好吗？

- 维度高 → 表达能力强，但计算慢、存储大
- 推荐：384-768 维（平衡性能和效果）

---

## 代码文件

```
day43_embedding_basic/
├── README.md                    # 本文件
├── embedding_basic.py           # 基础相似度计算
├── real_embedding.py            # 真实模型生成
├── stock_similarity.py          # 股票文本分析
└── embedding_comparison.md      # 模型对比笔记
```

---

## 参考资源

- [Sentence Transformers](https://www.sbert.net/)
- [OpenAI Embedding](https://platform.openai.com/docs/guides/embeddings)
- [Milvus 向量数据库](https://milvus.io/docs)

---

## 下一步

- **Day 44**: Milvus 安装（Docker 部署）
- **明日任务**: 动手搭建向量数据库

---

**💡 今日格言**: "Embedding 让计算机理解语义，向量数据库让搜索更高效"
