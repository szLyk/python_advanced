"""
Day 43: Embedding 概念

学习目标:
- 理解 Embedding 原理
- 掌握向量相似度计算
- 了解向量数据库的作用
- 对比常见向量数据库
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def basic_embedding_concept():
    """基础 Embedding 概念演示"""
    print("=" * 50)
    print("Embedding 基础概念")
    print("=" * 50)

    # 模拟 Embedding（实际应由模型生成）
    # 每个词用 3 维向量表示
    embeddings = {
        "国王": [0.85, 0.23, -0.12],
        "王后": [0.82, 0.25, -0.10],
        "男人": [0.75, -0.45, 0.32],
        "女人": [0.72, -0.48, 0.35],
        "股票": [0.10, 0.80, -0.30],
        "投资": [0.15, 0.75, -0.28],
        "天气": [-0.50, -0.20, 0.90],
    }

    print("\n词向量示例:")
    for word, vec in embeddings.items():
        print(f"  '{word}': {vec}")

    # 计算相似度
    print("\n相似度计算（余弦相似度）:")

    pairs = [
        ("国王", "王后"),
        ("男人", "女人"),
        ("股票", "投资"),
        ("国王", "天气"),
    ]

    for word1, word2 in pairs:
        v1 = np.array(embeddings[word1]).reshape(1, -1)
        v2 = np.array(embeddings[word2]).reshape(1, -1)
        sim = cosine_similarity(v1, v2)[0][0]
        print(f"  '{word1}' vs '{word2}': {sim:.4f}")


def stock_similarity_demo():
    """股票文本相似度演示"""
    print("\n" + "=" * 50)
    print("股票文本相似度分析")
    print("=" * 50)

    # 模拟股票相关句子的 Embedding
    sentences = {
        "茅台是白酒龙头": [0.8, 0.6, -0.2, 0.3],
        "五粮液生产浓香白酒": [0.75, 0.65, -0.18, 0.25],
        "宁德时代是电池龙头": [0.7, 0.5, -0.1, 0.4],
        "今天天气很好": [-0.3, -0.5, 0.8, -0.2],
        "我想买股票": [0.78, 0.62, -0.22, 0.28],
        "白酒行业前景好": [0.82, 0.68, -0.15, 0.22],
    }

    print("\n句子向量（4 维）:")
    for sent in sentences.keys():
        print(f"  '{sent}'")

    # 计算两两相似度
    print("\n相似度矩阵:")
    sent_names = list(sentences.keys())
    sentence_vecs = [np.array(v).reshape(1, -1) for v in sentences.values()]

    print("\n         ", end="")
    for name in sent_names[:4]:
        print(f"{name[:4]:>8}", end=" ")
    print()

    for i, (name1, vec1) in enumerate(zip(sent_names, sentence_vecs)):
        print(f"{name1[:8]:<10}", end="")
        for j, vec2 in enumerate(sentence_vecs):
            if i == j:
                print(f"{'1.0000':>8}", end=" ")
            elif i < j:
                sim = cosine_similarity(vec1, vec2)[0][0]
                print(f"{sim:>8.4f}", end=" ")
            else:
                print(f"{'':>8}", end=" ")
        print()


def find_similar_texts():
    """查找最相似的文本"""
    print("\n" + "=" * 50)
    print("查找最相似文本")
    print("=" * 50)

    # 文档库
    documents = [
        ("贵州茅台是白酒龙头企业", "doc1"),
        ("五粮液是浓香型白酒代表", "doc2"),
        ("宁德时代生产动力电池", "doc3"),
        ("今天北京天气晴朗", "doc4"),
        ("白酒行业估值合理", "doc5"),
    ]

    # 模拟 Embedding
    doc_embeddings = {
        "doc1": [0.8, 0.6, -0.2, 0.3],
        "doc2": [0.75, 0.65, -0.18, 0.25],
        "doc3": [0.7, 0.5, -0.1, 0.4],
        "doc4": [-0.3, -0.5, 0.8, -0.2],
        "doc5": [0.82, 0.68, -0.15, 0.22],
    }

    # 查询
    query = "茅台相关"
    query_vec = np.array([0.78, 0.62, -0.22, 0.28]).reshape(1, -1)

    print(f"\n查询：'{query}'")
    print("\n相似度排名:")

    # 计算相似度并排序
    similarities = []
    for doc_id, doc_vec in doc_embeddings.items():
        vec = np.array(doc_vec).reshape(1, -1)
        sim = cosine_similarity(query_vec, vec)[0][0]
        similarities.append((doc_id, sim))

    # 按相似度排序
    similarities.sort(key=lambda x: x[1], reverse=True)

    for doc_id, sim in similarities:
        doc_text = next(d[0] for d in documents if d[1] == doc_id)
        print(f"  相似度 {sim:.4f}: {doc_text}")


def visualize_embedding():
    """Embedding 可视化演示"""
    print("\n" + "=" * 50)
    print("Embedding 可视化（简化版）")
    print("=" * 50)

    # 2D 向量可视化
    embeddings_2d = {
        "股票": [0.8, 0.6],
        "投资": [0.75, 0.65],
        "基金": [0.7, 0.5],
        "债券": [0.3, 0.4],
        "天气": [-0.5, -0.5],
        "体育": [-0.6, 0.3],
    }

    print("\n2D 向量分布（ASCII 可视化）:")
    print("Y")
    print("^")

    # 简单 ASCII 可视化
    grid = [[' ' for _ in range(20)] for _ in range(10)]

    for word, (x, y) in embeddings_2d.items():
        # 映射到网格坐标
        col = int((x + 1) * 9)  # [-1,1] -> [0,18]
        row = int((1 - y) * 4)  # [-1,1] -> [0,8]
        row = max(0, min(8, row))
        col = max(0, min(18, col))
        grid[row][col] = word[0]  # 取第一个字

    for row in grid:
        print("|" + "".join(row) + "|")
    print("-" * 22 + "> X")

    print("\n图例：每个字代表一个词的向量位置")


def main():
    """主函数"""
    basic_embedding_concept()
    stock_similarity_demo()
    find_similar_texts()
    visualize_embedding()

    print("\n" + "=" * 50)
    print("✅ Day 43 学习完成！")
    print("=" * 50)
    print("\n提示：实际使用时，应使用真实的 Embedding 模型")
    print("如 OpenAI Embedding、Sentence Transformers 等")


if __name__ == "__main__":
    main()
