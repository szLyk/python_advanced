"""
Day 45: Milvus 基本操作

学习目标:
- 掌握 Collection 创建和管理
- 学会数据插入（Insert）
- 掌握向量搜索（Search）
- 了解索引构建
"""

import numpy as np

# 检查 Milvus 连接
try:
    from pymilvus import (
        connections,
        Collection,
        FieldSchema,
        CollectionSchema,
        DataType,
        utility
    )
    MILVUS_AVAILABLE = True
except ImportError:
    MILVUS_AVAILABLE = False
    print("⚠️  pymilvus 未安装，请运行：pip install pymilvus")


def connect_milvus():
    """连接 Milvus"""
    if not MILVUS_AVAILABLE:
        return None

    try:
        connections.connect(
            host="localhost",
            port="19530",
            timeout=5
        )
        print("✅ Milvus 连接成功")
        return True
    except Exception as e:
        print(f"❌ Milvus 连接失败：{e}")
        print("请确保 Milvus 已启动：docker-compose up -d")
        return None


def create_collection_demo():
    """创建 Collection 演示"""
    print("\n" + "=" * 50)
    print("创建 Collection 演示")
    print("=" * 50)

    if not connect_milvus():
        return

    try:
        # 删除已存在的 Collection
        if utility.has_collection("stock_demo"):
            utility.drop_collection("stock_demo")
            print("已删除已存在的 Collection")

        # 定义字段
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="stock_code", dtype=DataType.VARCHAR, max_length=20),
            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=2000),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=4),  # 简化演示，使用 4 维
        ]

        # 定义 Schema
        schema = CollectionSchema(fields, description="股票数据向量库")

        # 创建 Collection
        collection = Collection("stock_demo", schema)
        print(f"✅ Collection 'stock_demo' 创建成功")

        # 创建索引
        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "COSINE",
            "params": {"nlist": 64}
        }
        collection.create_index(field_name="embedding", index_params=index_params)
        print("✅ 索引创建成功")

        # 加载 Collection
        collection.load()
        print("✅ Collection 已加载到内存")

        return collection

    except Exception as e:
        print(f"❌ 错误：{e}")
        return None


def insert_demo(collection):
    """插入数据演示"""
    print("\n" + "=" * 50)
    print("插入数据演示")
    print("=" * 50)

    if not collection:
        return

    # 准备数据（使用随机向量模拟 Embedding）
    stock_data = [
        {"stock_code": "600519", "content": "贵州茅台是白酒龙头企业"},
        {"stock_code": "000858", "content": "五粮液是浓香型白酒代表"},
        {"stock_code": "300750", "content": "宁德时代是电池龙头"},
        {"stock_code": "AAPL", "content": "苹果公司是科技巨头"},
    ]

    # 添加随机 Embedding
    np.random.seed(42)
    entities = [
        {
            "stock_code": item["stock_code"],
            "content": item["content"],
            "embedding": np.random.rand(4).tolist()
        }
        for item in stock_data
    ]

    # 插入数据
    result = collection.insert(entities)
    print(f"✅ 插入 {result.insert_count} 条数据")

    # 刷新（使数据可搜索）
    collection.flush()
    print("✅ 数据已刷新")


def search_demo(collection):
    """搜索演示"""
    print("\n" + "=" * 50)
    print("向量搜索演示")
    print("=" * 50)

    if not collection:
        return

    # 搜索参数
    search_params = {
        "metric_type": "COSINE",
        "params": {"nprobe": 10}
    }

    # 模拟查询向量
    query_vector = np.random.rand(4).tolist()

    # 执行搜索
    results = collection.search(
        data=[query_vector],
        anns_field="embedding",
        search_params=search_params,
        limit=3,
        output_fields=["stock_code", "content"]
    )

    print("\n搜索结果:")
    for hits in results:
        for hit in hits:
            print(f"  相似度：{hit.score:.4f}, 代码：{hit.entity.get('stock_code')}, 内容：{hit.entity.get('content')}")


def query_demo(collection):
    """标量查询演示"""
    print("\n" + "=" * 50)
    print("标量查询演示")
    print("=" * 50)

    if not collection:
        return

    # 表达式查询
    expr = 'stock_code == "600519"'
    results = collection.query(expr, output_fields=["content"])

    print(f"\n查询条件：{expr}")
    for r in results:
        print(f"  内容：{r.get('content')}")


def cleanup_demo():
    """清理演示数据"""
    print("\n" + "=" * 50)
    print("清理演示数据")
    print("=" * 50)

    if not connect_milvus():
        return

    if utility.has_collection("stock_demo"):
        utility.drop_collection("stock_demo")
        print("✅ Collection 'stock_demo' 已删除")


def main():
    """主函数"""
    print("=" * 60)
    print("Day 45: Milvus 基本操作")
    print("=" * 60)

    if not MILVUS_AVAILABLE:
        print("\n❌ pymilvus 未安装")
        print("请运行：pip install pymilvus")
        return

    # 创建 Collection
    collection = create_collection_demo()

    if collection:
        # 插入数据
        insert_demo(collection)

        # 搜索演示
        search_demo(collection)

        # 标量查询演示
        query_demo(collection)

        # 清理
        # cleanup_demo()  # 可选：清理数据

    print("\n" + "=" * 60)
    print("✅ Day 45 学习完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
