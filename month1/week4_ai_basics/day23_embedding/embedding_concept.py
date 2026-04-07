"""
Day 23: Embedding 词向量与句向量

学习目标：
1. 理解 Embedding 原理
2. 掌握向量相似度计算
3. 应用 Embedding 进行语义搜索
"""

import numpy as np
from typing import List, Tuple
import json


# ============================================
# 1. 向量相似度计算
# ============================================

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    余弦相似度（最常用）

    similarity = (a · b) / (|a| · |b|)
    范围: [-1, 1]，值越大越相似

    Args:
        a: 向量 a
        b: 向量 b

    Returns:
        相似度值
    """
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    """
    欧氏距离

    distance = sqrt(sum((a_i - b_i)^2))
    范围: [0, ∞]，值越小越相似
    """
    return np.linalg.norm(a - b)


def dot_product_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    点积相似度

    dot = a · b
    简单但受向量长度影响
    """
    return np.dot(a, b)


def manhattan_distance(a: np.ndarray, b: np.ndarray) -> float:
    """
    曼哈顿距离

    distance = sum(|a_i - b_i|)
    """
    return np.sum(np.abs(a - b))


# ============================================
# 2. One-Hot 编码（传统方法）
# ============================================

class OneHotEncoder:
    """简单的 One-Hot 编码器"""

    def __init__(self):
        self.vocab = []
        self.token_to_id = {}

    def fit(self, texts: List[str]):
        """构建词汇表"""
        all_tokens = set()
        for text in texts:
            tokens = text.split()
            all_tokens.update(tokens)

        self.vocab = sorted(list(all_tokens))
        self.token_to_id = {token: i for i, token in enumerate(self.vocab)}

    def encode(self, text: str) -> np.ndarray:
        """编码文本为 One-Hot 向量"""
        tokens = text.split()
        vector = np.zeros(len(self.vocab))

        for token in tokens:
            if token in self.token_to_id:
                vector[self.token_to_id[token]] = 1

        return vector

    def decode(self, vector: np.ndarray) -> List[str]:
        """解码向量为词列表"""
        indices = np.where(vector > 0)[0]
        return [self.vocab[i] for i in indices]


# ============================================
# 3. Word2Vec 模拟（简化版）
# ============================================

class SimpleWord2Vec:
    """简化的 Word2Vec 模型（演示原理）"""

    def __init__(self, embedding_dim: int = 50):
        self.embedding_dim = embedding_dim
        self.vocab = []
        self.token_to_id = {}
        self.embeddings = None

    def build_vocab(self, texts: List[str]):
        """构建词汇表"""
        all_tokens = set()
        for text in texts:
            tokens = text.lower().split()
            all_tokens.update(tokens)

        self.vocab = sorted(list(all_tokens))
        self.token_to_id = {token: i for i, token in enumerate(self.vocab)}

        # 随机初始化 Embedding（实际需要训练）
        np.random.seed(42)
        self.embeddings = np.random.randn(len(self.vocab), self.embedding_dim) * 0.1

    def get_embedding(self, word: str) -> np.ndarray:
        """获取词向量"""
        word = word.lower()
        if word in self.token_to_id:
            return self.embeddings[self.token_to_id[word]]
        return np.zeros(self.embedding_dim)

    def get_text_embedding(self, text: str) -> np.ndarray:
        """获取文本向量（平均池化）"""
        tokens = text.lower().split()
        if not tokens:
            return np.zeros(self.embedding_dim)

        word_vectors = [self.get_embedding(t) for t in tokens if t in self.token_to_id]
        if not word_vectors:
            return np.zeros(self.embedding_dim)

        return np.mean(word_vectors, axis=0)

    def most_similar(self, word: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """找最相似的词"""
        word_vec = self.get_embedding(word)
        if np.all(word_vec == 0):
            return []

        similarities = []
        for other_word in self.vocab:
            if other_word != word.lower():
                other_vec = self.get_embedding(other_word)
                sim = cosine_similarity(word_vec, other_vec)
                similarities.append((other_word, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]


# ============================================
# 4. 模拟 Embedding 模型
# ============================================

class MockEmbeddingModel:
    """
    模拟 Embedding 模型（用于演示，无实际语义）

    实际使用时替换为真实模型：
    - sentence-transformers
    - OpenAI API
    - 其他 Embedding 服务
    """

    def __init__(self, embedding_dim: int = 128):
        self.embedding_dim = embedding_dim
        # 使用固定种子生成"伪随机"向量，使相似文本有相似向量

    def encode(self, text: str) -> np.ndarray:
        """生成文本 Embedding"""
        # 基于文本内容生成伪向量（仅演示）
        # 实际模型会学习真实的语义表示

        seed = sum(ord(c) for c in text)
        np.random.seed(seed % 10000)
        base_vector = np.random.randn(self.embedding_dim)

        # 添加文本特征影响
        features = {
            'positive_words': ['上涨', '利好', '增长', '盈利', '新高', '大涨'],
            'negative_words': ['下跌', '利空', '亏损', '暴跌', '下滑'],
            'tech_words': ['科技', '苹果', '谷歌', '微软', 'AI', '芯片'],
            'finance_words': ['股票', '市值', '财报', '投资', '基金']
        }

        modifier = np.zeros(self.embedding_dim)
        for category, words in features.items():
            for word in words:
                if word in text:
                    np.random.seed(hash(category) % 10000)
                    modifier += np.random.randn(self.embedding_dim) * 0.5

        return base_vector + modifier

    def encode_batch(self, texts: List[str]) -> np.ndarray:
        """批量生成 Embedding"""
        return np.array([self.encode(t) for t in texts])


# ============================================
# 5. 语义搜索引擎
# ============================================

class SemanticSearchEngine:
    """简单的语义搜索引擎"""

    def __init__(self, embedding_model: MockEmbeddingModel):
        self.model = embedding_model
        self.documents = []
        self.embeddings = None

    def index(self, documents: List[str]):
        """索引文档"""
        self.documents = documents
        self.embeddings = self.model.encode_batch(documents)
        print(f"已索引 {len(documents)} 个文档")

    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """搜索最相似的文档"""
        query_embedding = self.model.encode(query)

        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            sim = cosine_similarity(query_embedding, doc_embedding)
            similarities.append((self.documents[i], sim, i))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    def search_by_id(self, doc_id: int, top_k: int = 5) -> List[Tuple[str, float]]:
        """基于文档ID搜索相似文档"""
        if doc_id >= len(self.embeddings):
            return []

        query_embedding = self.embeddings[doc_id]

        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            if i != doc_id:
                sim = cosine_similarity(query_embedding, doc_embedding)
                similarities.append((self.documents[i], sim, i))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]


# ============================================
# 6. 文本聚类
# ============================================

def simple_kmeans_clustering(
    embeddings: np.ndarray,
    n_clusters: int = 3,
    max_iterations: int = 100
) -> Tuple[np.ndarray, np.ndarray]:
    """
    简化的 K-Means 聚类

    Args:
        embeddings: 文本向量矩阵
        n_clusters: 聚类数量
        max_iterations: 最大迭代次数

    Returns:
        cluster_labels: 每个样本的聚类标签
        centroids: 聚类中心
    """
    n_samples = embeddings.shape[0]

    # 随机初始化聚类中心
    np.random.seed(42)
    indices = np.random.choice(n_samples, n_clusters, replace=False)
    centroids = embeddings[indices].copy()

    for _ in range(max_iterations):
        # 分配样本到最近的聚类
        distances = np.zeros((n_samples, n_clusters))
        for k in range(n_clusters):
            distances[:, k] = np.linalg.norm(embeddings - centroids[k], axis=1)

        labels = np.argmin(distances, axis=1)

        # 更新聚类中心
        new_centroids = np.zeros_like(centroids)
        for k in range(n_clusters):
            cluster_points = embeddings[labels == k]
            if len(cluster_points) > 0:
                new_centroids[k] = cluster_points.mean(axis=0)
            else:
                new_centroids[k] = centroids[k]

        # 检查收敛
        if np.allclose(centroids, new_centroids):
            break

        centroids = new_centroids

    return labels, centroids


# ============================================
# 7. 演示代码
# ============================================

def demo_similarity():
    """演示相似度计算"""
    print("\n=== 向量相似度计算 ===")

    # 创建示例向量
    vec_a = np.array([1, 2, 3, 4])
    vec_b = np.array([1, 2, 3, 4])  # 相同向量
    vec_c = np.array([-1, -2, -3, -4])  # 相反向量
    vec_d = np.array([4, 3, 2, 1])  # 不同向量

    print(f"向量 A: {vec_a}")
    print(f"向量 B: {vec_b} (相同)")
    print(f"向量 C: {vec_c} (相反)")
    print(f"向量 D: {vec_d} (不同)")

    print("\n余弦相似度:")
    print(f"  A vs B: {cosine_similarity(vec_a, vec_b):.3f} (应为1)")
    print(f"  A vs C: {cosine_similarity(vec_a, vec_c):.3f} (应为-1)")
    print(f"  A vs D: {cosine_similarity(vec_a, vec_d):.3f}")

    print("\n欧氏距离:")
    print(f"  A vs B: {euclidean_distance(vec_a, vec_b):.3f} (应为0)")
    print(f"  A vs C: {euclidean_distance(vec_a, vec_c):.3f}")
    print(f"  A vs D: {euclidean_distance(vec_a, vec_d):.3f}")


def demo_onehot():
    """演示 One-Hot 编码"""
    print("\n=== One-Hot 编码 ===")

    texts = ["股票 上涨", "股票 下跌", "科技 股票"]
    encoder = OneHotEncoder()
    encoder.fit(texts)

    print(f"词汇表: {encoder.vocab}")

    for text in texts:
        vector = encoder.encode(text)
        print(f"'{text}' → {vector}")
        print(f"  解码: {encoder.decode(vector)}")


def demo_word2vec():
    """演示 Word2Vec"""
    print("\n=== Word2Vec 模拟 ===")

    # 股票相关文本
    texts = [
        "苹果 股票 上涨",
        "谷歌 市值 增长",
        "特斯拉 股价 下跌",
        "科技 股票 利好",
        "股市 投资 分析"
    ]

    w2v = SimpleWord2Vec(embedding_dim=20)
    w2v.build_vocab(texts)

    print(f"词汇表大小: {len(w2v.vocab)}")
    print(f"Embedding 维度: {w2v.embedding_dim}")

    # 获取词向量
    word = "股票"
    vec = w2v.get_embedding(word)
    print(f"'{word}' 向量 (前10维): {vec[:10]}")

    # 文本向量
    text_vec = w2v.get_text_embedding("苹果 股票")
    print(f"'苹果 股票' 文本向量 (前10维): {text_vec[:10]}")

    # 相似词
    similar = w2v.most_similar("股票", top_k=3)
    print(f"与 '股票' 最相似的词: {similar}")


def demo_embedding_model():
    """演示 Embedding 模型"""
    print("\n=== Embedding 模型演示 ===")

    model = MockEmbeddingModel(embedding_dim=64)

    texts = [
        "苹果股票大涨",
        "特斯拉股价下跌",
        "科技股迎来利好",
        "股市整体下滑",
        "微软发布新产品"
    ]

    embeddings = model.encode_batch(texts)

    print(f"文本数量: {len(texts)}")
    print(f"向量维度: {embeddings.shape[1]}")

    # 计算相似度矩阵
    print("\n相似度矩阵:")
    for i, text1 in enumerate(texts):
        for j, text2 in enumerate(texts):
            if i < j:
                sim = cosine_similarity(embeddings[i], embeddings[j])
                print(f"  '{text1}' vs '{text2}': {sim:.3f}")


def demo_semantic_search():
    """演示语义搜索"""
    print("\n=== 语义搜索演示 ===")

    # 新闻库
    news_database = [
        "苹果公司股价今日大涨5%，市值突破新高",
        "特斯拉发布新车型，市场反应积极",
        "科技股整体下跌，投资者情绪悲观",
        "谷歌财报超预期，股价上涨3%",
        "微软云业务增长强劲，股价创新高",
        "芯片股受供应链影响，普遍下跌",
        "新能源汽车销量增长，相关股票上涨",
        "AI热潮推动科技股持续走高"
    ]

    model = MockEmbeddingModel(embedding_dim=64)
    search_engine = SemanticSearchEngine(model)
    search_engine.index(news_database)

    # 搜索查询
    queries = [
        "苹果股价表现如何",
        "科技股下跌",
        "新能源汽车股票"
    ]

    for query in queries:
        print(f"\n查询: '{query}'")
        results = search_engine.search(query, top_k=3)
        for doc, sim, idx in results:
            print(f"  [{sim:.3f}] {doc}")

    # 相似文档搜索
    print("\n--- 与第1条新闻相似的文档 ---")
    similar_docs = search_engine.search_by_id(0, top_k=3)
    for doc, sim, idx in similar_docs:
        print(f"  [{sim:.3f}] {doc}")


def demo_clustering():
    """演示文本聚类"""
    print("\n=== 文本聚类演示 ===")

    model = MockEmbeddingModel(embedding_dim=32)

    texts = [
        "苹果股票上涨",
        "谷歌市值增长",
        "微软股价创新高",
        "特斯拉股价下跌",
        "芯片股暴跌",
        "科技股下滑",
        "新能源汽车利好",
        "电动车销量增长",
        "绿色能源政策支持"
    ]

    embeddings = model.encode_batch(texts)
    labels, centroids = simple_kmeans_clustering(embeddings, n_clusters=3)

    print(f"聚类数量: 3")
    print("\n聚类结果:")

    clusters = {}
    for text, label in zip(texts, labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(text)

    for label, texts_in_cluster in clusters.items():
        print(f"\n聚类 {label}:")
        for text in texts_in_cluster:
            print(f"  - {text}")


def demo_embedding_best_practices():
    """演示 Embedding 最佳实践"""
    print("\n=== Embedding 最佳实践 ===")

    practices = """
    1. 文本预处理
       - 去除多余空格和换行
       - 统一大小写（视模型而定）
       - 处理特殊字符

    2. 批量处理
       - 使用 batch_encode 提高效率
       - 建议 batch_size: 100-1000

    3. 长文本处理
       - 分块处理（chunk_size: 500-1000）
       - 使用滑动窗口避免边界丢失

    4. 模型选择
       - 中文：BGE-large-zh (1024维)
       - 英文：text-embedding-ada-002 (1536维)
       - 多语言：E5-large-v2 (1024维)

    5. 存储优化
       - 向量维度高，注意存储空间
       - 使用向量数据库（Milvus, Pinecone）
       - 考虑向量压缩/量化

    6. 相似度度量
       - 余弦相似度：最常用
       - 欧氏距离：聚类场景
       - 点积：已归一化向量时可用
    """
    print(practices)


# ============================================
# 主程序
# ============================================

if __name__ == "__main__":
    print("Day 23: Embedding 词向量与句向量")
    print("=" * 60)

    demo_similarity()
    demo_onehot()
    demo_word2vec()
    demo_embedding_model()
    demo_semantic_search()
    demo_clustering()
    demo_embedding_best_practices()

    print("\n" + "=" * 60)
    print("学习要点:")
    print("1. Embedding 将文本转为数值向量")
    print("2. 相似文本有相似的向量")
    print("3. 余弦相似度是常用度量方式")
    print("4. Embedding 是语义搜索和RAG的基础")
    print("5. 选择合适的 Embedding 模型很重要")