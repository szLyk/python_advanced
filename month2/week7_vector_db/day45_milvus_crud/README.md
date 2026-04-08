# Day 45: Milvus 基本操作

> **日期**: 2026-05-17（周六）  
> **周次**: Week 7 - 向量数据库  
> **预计耗时**: 2 小时

---

## 今日学习目标

- [ ] 掌握 Collection 创建和管理
- [ ] 学会数据插入（Insert）
- [ ] 掌握向量搜索（Search）
- [ ] 了解索引构建

---

## 学习内容

### 1. Collection 创建

Collection 是 Milvus 中存储数据的基本单位，类似关系数据库的表。

```python
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType

# 连接 Milvus
connections.connect(host="localhost", port="19530")

# 定义字段
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=500),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768),
]

# 定义 Schema
schema = CollectionSchema(fields, description="股票文档向量库")

# 创建 Collection
collection = Collection("stock_documents", schema)

print(f"✅ Collection 创建成功：{collection.name}")
```

### 2. 创建索引

索引加速向量搜索：

```python
# 定义索引参数
index_params = {
    "index_type": "IVF_FLAT",      # 索引类型
    "metric_type": "COSINE",       # 相似度度量（余弦）
    "params": {"nlist": 128},      # 聚类中心数量
}

# 创建索引
collection.create_index(
    field_name="embedding",
    index_params=index_params
)

print("✅ 索引创建成功")
```

### 3. 加载 Collection

搜索前需要加载到内存：

```python
collection.load()
print("✅ Collection 已加载到内存")
```

### 4. 插入数据

```python
import numpy as np

# 准备数据
titles = [
    "贵州茅台是白酒龙头企业",
    "五粮液发布新品",
    "新能源汽车行业发展趋势",
    "宁德时代电池技术突破",
]

# 模拟 Embedding（实际应使用模型生成）
embeddings = np.random.rand(len(titles), 768).tolist()

# 插入数据
entities = [
    {"title": title, "embedding": emb}
    for title, emb in zip(titles, embeddings)
]

result = collection.insert(entities)
print(f"✅ 插入 {result.insert_count} 条数据")
```

### 5. 向量搜索

```python
# 搜索参数
search_params = {
    "metric_type": "COSINE",
    "params": {"nprobe": 10}
}

# 搜索向量（模拟查询 Embedding）
query_vector = np.random.rand(768).tolist()

# 执行搜索
results = collection.search(
    data=[query_vector],
    anns_field="embedding",
    search_params=search_params,
    limit=3,  # 返回 Top-3
    output_fields=["title"]
)

# 处理结果
for hits in results:
    for hit in hits:
        print(f"标题：{hit.entity.get('title')}, 相似度：{hit.score:.4f}")
```

### 6. 数据查询（标量过滤）

```python
# 表达式查询
expr = 'title like "茅台%"'
results = collection.query(expr, output_fields=["id", "title"])

for r in results:
    print(r)
```

### 7. 删除数据

```python
# 删除指定 ID
collection.delete("id in [1, 2, 3]")

# 删除符合条件的数据
collection.delete('title like "旧新闻%"')
```

---

## 实践任务

### 任务 1: 创建 Collection ✅

```python
# milvus_crud.py

from pymilvus import connections, FieldSchema, CollectionSchema, Collection, DataType

connections.connect(host="localhost", port="19530")

# 创建股票数据 Collection
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="stock_code", dtype=DataType.VARCHAR, max_length=20),
    FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=2000),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
]

schema = CollectionSchema(fields, description="股票数据向量库")
collection = Collection("stock_data", schema)

# 创建索引
collection.create_index(
    field_name="embedding",
    index_params={
        "index_type": "IVF_FLAT",
        "metric_type": "COSINE",
        "params": {"nlist": 64}
    }
)

# 加载
collection.load()
print("✅ Collection 准备完成")
```

### 任务 2: 插入股票数据 ✅

```python
# 插入数据
stock_news = [
    {"stock_code": "600519", "content": "贵州茅台季度营收增长 20%", "embedding": [...]},
    {"stock_code": "000858", "content": "五粮液新品发布会", "embedding": [...]},
    {"stock_code": "300750", "content": "宁德时代新技术发布", "embedding": [...]},
]

result = collection.insert(stock_news)
print(f"插入 {result.insert_count} 条数据")
```

### 任务 3: 相似度搜索 ✅

```python
# 搜索"茅台相关新闻"
query = "贵州茅台 营收 增长"
query_vector = [...]  # 使用 Embedding 模型生成

results = collection.search(
    data=[query_vector],
    anns_field="embedding",
    limit=3,
    output_fields=["stock_code", "content"]
)

for hit in results[0]:
    print(f"相似度：{hit.score:.4f}, 内容：{hit.entity.get('content')}")
```

---

## 知识点总结

| 操作 | API | 说明 |
|------|-----|------|
| 创建 Collection | `Collection()` | 定义数据结构 |
| 创建索引 | `create_index()` | 加速搜索 |
| 加载 | `load()` | 加载到内存 |
| 插入 | `insert()` | 添加数据 |
| 搜索 | `search()` | 相似度搜索 |
| 查询 | `query()` | 标量过滤 |
| 删除 | `delete()` | 删除数据 |

---

## 常见问题

### Q1: Collection 已存在怎么办？
```python
from pymilvus import has_collection, drop_collection

if has_collection("stock_data"):
    drop_collection("stock_data")
```

### Q2: 搜索结果为空？
- 检查是否调用了 `load()`
- 检查是否有数据
- 检查向量维度是否匹配

### Q3: 如何清空数据？
```python
# 删除 Collection 重建
drop_collection("name")
# 或
collection.drop()
```

---

## 代码文件

```
day45_milvus_crud/
├── README.md                    # 本文件
├── milvus_crud.py               # CRUD 操作练习
├── stock_collection.py          # 股票数据集合
└── search_demo.py               # 搜索演示
```

---

## 参考资源

- [Milvus Python SDK](https://milvus.io/docs/reference/milvus/2.3.x/python/Overview.md)
- [Pymilvus API](https://pymilvus.readthedocs.io/en/latest/)

---

## 下一步

- **Day 46**: LangChain 集成（VectorStore）
- **明日任务**: 学习 LangChain 与 Milvus 的集成

---

**💡 今日格言**: "CRUD 是数据库的基本功"
