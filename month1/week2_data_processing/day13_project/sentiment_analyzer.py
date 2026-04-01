"""
Day 13: 情绪分析模块

核心知识点应用：
- NumPy：情绪分数计算、词频矩阵、统计运算
- 向量化计算：避免循环，提升效率

情绪分析方法：
- 基于关键词词典的简易情绪分析（不用 LLM）
- 正面词 +1 权重，负面词 -1 权重
- 计算每条新闻的情绪分数

作者：AI Agent 工程师学习者
日期：2026-04-01
"""

import numpy as np
from typing import List, Dict, Tuple
import re

from config import POSITIVE_WORDS, NEGATIVE_WORDS


# ============================================================
# 情绪词典
# ============================================================

class SentimentDictionary:
    """
    情绪词典类

    功能：
    - 存储正面/负面关键词
    - 支持扩展词典
    """

    def __init__(self):
        self.positive_words = set(POSITIVE_WORDS)
        self.negative_words = set(NEGATIVE_WORDS)
        self._build_weight_dict()

    def _build_weight_dict(self):
        """
        构建权重字典

        强度分级：
        - 强正面词：+1.5
        - 一般正面词：+1.0
        - 强负面词：-1.5
        - 一般负面词：-1.0
        """
        # 强正面词（更强的正面情绪）
        strong_positive = ['surge', 'boom', 'record', 'all-time', 'unprecedented', 'rally']
        # 强负面词（更强的负面情绪）
        strong_negative = ['crash', 'plunge', 'crisis', 'recession', 'sell-off', 'collapse']

        self.weights = {}

        # 正面词权重
        for word in self.positive_words:
            self.weights[word] = 1.5 if word in strong_positive else 1.0

        # 负面词权重
        for word in self.negative_words:
            self.weights[word] = -1.5 if word in strong_negative else -1.0

    def add_word(self, word: str, sentiment: float):
        """
        添加自定义词汇

        Args:
            word: 词汇
            sentiment: 情绪分数（正数=正面，负数=负面）
        """
        self.weights[word] = sentiment
        if sentiment > 0:
            self.positive_words.add(word)
        else:
            self.negative_words.add(word)

    def get_weight(self, word: str) -> float:
        """
        获取词汇权重
        """
        return self.weights.get(word, 0.0)


# ============================================================
# NumPy 情绪分析
# ============================================================

class SentimentAnalyzer:
    """
    情绪分析器 - 基于 NumPy 向量化计算
    """

    def __init__(self):
        self.dictionary = SentimentDictionary()

    def analyze_text(self, text: str) -> Dict:
        """
        分析单条文本的情绪

        Args:
            text: 文本内容

        Returns:
            情绪分析结果字典
        """
        if not text:
            return {'score': 0.0, 'positive_count': 0, 'negative_count': 0, 'keywords': []}

        # 文本预处理
        text_lower = text.lower()
        words = re.findall(r'\b[a-z]+\b', text_lower)

        # 统计关键词
        positive_matches = []
        negative_matches = []

        for word in words:
            if word in self.dictionary.positive_words:
                positive_matches.append(word)
            elif word in self.dictionary.negative_words:
                negative_matches.append(word)

        # 计算情绪分数
        pos_score = sum(self.dictionary.get_weight(w) for w in positive_matches)
        neg_score = sum(abs(self.dictionary.get_weight(w)) for w in negative_matches)

        total_keywords = len(positive_matches) + len(negative_matches)
        if total_keywords == 0:
            score = 0.0
        else:
            # 分数范围 [-1, 1]
            score = (pos_score - neg_score) / (pos_score + neg_score + 1)

        return {
            'score': score,
            'positive_count': len(positive_matches),
            'negative_count': len(negative_matches),
            'keywords': positive_matches + negative_matches,
            'positive_words': positive_matches,
            'negative_words': negative_matches,
        }

    def analyze_batch_numpy(self, texts: List[str]) -> np.ndarray:
        """
        批量分析文本情绪（NumPy 向量化）

        Args:
            texts: 文本列表

        Returns:
            情绪分数数组
        """
        n = len(texts)
        scores = np.zeros(n)

        for i, text in enumerate(texts):
            result = self.analyze_text(text)
            scores[i] = result['score']

        return scores

    def analyze_batch_fast(self, texts: List[str]) -> np.ndarray:
        """
        快速批量分析（更高效的 NumPy 实现）

        使用 NumPy 数组存储中间结果，减少 Python 循环

        Args:
            texts: 文本列表

        Returns:
            情绪分数数组
        """
        n = len(texts)

        # 使用 NumPy 数组存储结果
        positive_counts = np.zeros(n)
        negative_counts = np.zeros(n)
        positive_weights = np.zeros(n)
        negative_weights = np.zeros(n)

        # 构建词汇权重矩阵（优化版）
        # 这里为了演示 NumPy 用法，使用向量化思想
        pos_words = list(self.dictionary.positive_words)
        neg_words = list(self.dictionary.negative_words)

        for i, text in enumerate(texts):
            text_lower = text.lower()
            words = set(re.findall(r'\b[a-z]+\b', text_lower))

            # 统计正面词
            pos_found = [w for w in words if w in pos_words]
            positive_counts[i] = len(pos_found)
            positive_weights[i] = sum(self.dictionary.get_weight(w) for w in pos_found)

            # 统计负面词
            neg_found = [w for w in words if w in neg_words]
            negative_counts[i] = len(neg_found)
            negative_weights[i] = sum(abs(self.dictionary.get_weight(w)) for w in neg_found)

        # NumPy 向量化计算最终分数
        total = positive_weights + negative_weights
        # 避免除零
        total_safe = np.where(total == 0, 1, total)
        scores = (positive_weights - negative_weights) / total_safe

        # 处理无关键词的情况
        scores = np.where(total == 0, 0.0, scores)

        return scores

    def get_statistics(self, scores: np.ndarray) -> Dict:
        """
        统计情绪分数分布（NumPy 统计函数）

        Args:
            scores: 情绪分数数组

        Returns:
            统计结果字典
        """
        return {
            'mean': np.mean(scores),
            'median': np.median(scores),
            'std': np.std(scores),
            'min': np.min(scores),
            'max': np.max(scores),
            'positive_ratio': np.sum(scores > 0.1) / len(scores),
            'negative_ratio': np.sum(scores < -0.1) / len(scores),
            'neutral_ratio': np.sum((scores >= -0.1) & (scores <= 0.1)) / len(scores),
        }


# ============================================================
# 词频分析
# ============================================================

class WordFrequencyAnalyzer:
    """
    词频分析器 - NumPy 实现
    """

    def __init__(self):
        self.stop_words = set([
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'shall',
            'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in',
            'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
            'through', 'during', 'before', 'after', 'above', 'below',
            'between', 'under', 'again', 'further', 'then', 'once',
            'here', 'there', 'when', 'where', 'why', 'how', 'all',
            'each', 'few', 'more', 'most', 'other', 'some', 'such',
            'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
            'too', 'very', 'just', 'and', 'but', 'if', 'or', 'because',
            'until', 'while', 'about', 'against', 'between', 'into',
            'through', 'during', 'before', 'after', 'above', 'below',
            'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
            'over', 'under', 'again', 'further', 'then', 'once',
        ])

    def count_words(self, texts: List[str]) -> Dict[str, int]:
        """
        统计词频

        Args:
            texts: 文本列表

        Returns:
            词频字典
        """
        word_count = {}

        for text in texts:
            words = re.findall(r'\b[a-z]+\b', text.lower())
            for word in words:
                if word not in self.stop_words and len(word) > 2:
                    word_count[word] = word_count.get(word, 0) + 1

        return word_count

    def get_top_words(self, texts: List[str], top_n: int = 20) -> List[Tuple[str, int]]:
        """
        获取高频词 Top N

        Args:
            texts: 文本列表
            top_n: 返回数量

        Returns:
            (词汇, 频次) 列表
        """
        word_count = self.count_words(texts)

        # 使用 NumPy 排序
        words = np.array(list(word_count.keys()))
        counts = np.array(list(word_count.values()))

        # 按频次降序排序
        sorted_indices = np.argsort(counts)[::-1]

        top_words = []
        for i in sorted_indices[:top_n]:
            top_words.append((words[i], counts[i]))

        return top_words

    def get_word_frequency_matrix(self, texts: List[str], vocabulary: List[str] = None) -> np.ndarray:
        """
        构建词频矩阵（NumPy）

        Args:
            texts: 文本列表
            vocabulary: 词汇表（可选）

        Returns:
            词频矩阵（shape: [n_texts, n_words])
        """
        if vocabulary is None:
            # 从文本中提取词汇
            all_words = set()
            for text in texts:
                words = re.findall(r'\b[a-z]+\b', text.lower())
                all_words.update(w for w in words if w not in self.stop_words and len(w) > 2)
            vocabulary = list(all_words)[:100]  # 限制词汇表大小

        n_texts = len(texts)
        n_words = len(vocabulary)

        # 创建词频矩阵
        matrix = np.zeros((n_texts, n_words))

        word_to_idx = {word: idx for idx, word in enumerate(vocabulary)}

        for i, text in enumerate(texts):
            words = re.findall(r'\b[a-z]+\b', text.lower())
            for word in words:
                if word in word_to_idx:
                    matrix[i, word_to_idx[word]] += 1

        return matrix


# ============================================================
# 测试用例
# ============================================================

def test_sentiment_dictionary():
    """测试情绪词典"""
    print("\n" + "=" * 50)
    print("测试情绪词典")
    print("=" * 50)

    dict_obj = SentimentDictionary()
    print(f"正面词数量: {len(dict_obj.positive_words)}")
    print(f"负面词数量: {len(dict_obj.negative_words)}")
    print(f"示例正面词: {list(dict_obj.positive_words)[:10]}")
    print(f"示例负面词: {list(dict_obj.negative_words)[:10]}")


def test_single_text_analysis():
    """测试单文本分析"""
    print("\n" + "=" * 50)
    print("测试单文本情绪分析")
    print("=" * 50)

    analyzer = SentimentAnalyzer()

    test_texts = [
        "Stock prices surge amid positive earnings report",
        "Market drops as inflation concerns grow",
        "The company reported quarterly results",
    ]

    for text in test_texts:
        result = analyzer.analyze_text(text)
        print(f"\n文本: {text}")
        print(f"  情绪分数: {result['score']:.3f}")
        print(f"  正面词: {result['positive_words']}")
        print(f"  负面词: {result['negative_words']}")


def test_numpy_batch_analysis():
    """测试 NumPy 批量分析"""
    print("\n" + "=" * 50)
    print("测试 NumPy 批量分析")
    print("=" * 50)

    analyzer = SentimentAnalyzer()

    # 生成测试数据
    test_texts = [
        "Stock prices surge to record high amid strong earnings",
        "Market crashes as recession fears escalate",
        "Tech stocks rally on AI breakthrough announcement",
        "Investors worried about potential rate hike",
        "Company reports stable quarterly growth",
    ]

    # 批量分析
    scores = analyzer.analyze_batch_numpy(test_texts)

    print(f"\n情绪分数数组: {scores}")

    # 统计
    stats = analyzer.get_statistics(scores)
    print("\n统计结果:")
    for key, value in stats.items():
        print(f"  {key}: {value:.4f}")


def test_word_frequency():
    """测试词频分析"""
    print("\n" + "=" * 50)
    print("测试词频分析")
    print("=" * 50)

    analyzer = WordFrequencyAnalyzer()

    test_texts = [
        "Stock prices surge to record high amid strong earnings",
        "Market crashes as recession fears escalate",
        "Tech stocks rally on AI breakthrough announcement",
    ]

    # 词频统计
    word_count = analyzer.count_words(test_texts)
    print(f"\n词频统计: {dict(sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:10])}")

    # Top N 高频词
    top_words = analyzer.get_top_words(test_texts, top_n=10)
    print(f"\nTop 10 高频词: {top_words}")


def test_numpy_operations():
    """测试 NumPy 运算"""
    print("\n" + "=" * 50)
    print("测试 NumPy 运算演示")
    print("=" * 50)

    # 模拟情绪分数
    scores = np.array([0.8, -0.6, 0.7, -0.5, 0.3, -0.2, 0.5, 0.1, -0.4, 0.9])

    print(f"原始分数: {scores}")

    # NumPy 统计
    print(f"\nNumPy 统计:")
    print(f"  均值: {np.mean(scores):.3f}")
    print(f"  中位数: {np.median(scores):.3f}")
    print(f"  标准差: {np.std(scores):.3f}")
    print(f"  最大值: {np.max(scores):.3f}")
    print(f"  最小值: {np.min(scores):.3f}")

    # 布尔筛选
    print(f"\n布尔筛选:")
    print(f"  正面新闻 (>0.1): {scores[scores > 0.1]}")
    print(f"  负面新闻 (<-0.1): {scores[scores < -0.1]}")

    # 统计比例
    print(f"\n比例统计:")
    print(f"  正面比例: {np.sum(scores > 0.1) / len(scores):.2%}")
    print(f"  负面比例: {np.sum(scores < -0.1) / len(scores):.2%}")


# ============================================================
# 主程序
# ============================================================

def main():
    """运行所有测试"""
    print("=" * 60)
    print("Day 13: sentiment_analyzer.py 模块测试")
    print("=" * 60)

    test_sentiment_dictionary()
    test_single_text_analysis()
    test_numpy_batch_analysis()
    test_word_frequency()
    test_numpy_operations()

    print("\n" + "=" * 60)
    print("✅ sentiment_analyzer.py 模块测试完成！")
    print("=" * 60)
    print("""
知识点应用总结：
1. ✅ NumPy 数组：存储情绪分数、词频矩阵
2. ✅ NumPy 统计函数：mean、median、std、min、max
3. ✅ NumPy 布尔索引：筛选正面/负面新闻
4. ✅ NumPy 向量化计算：批量处理提升效率
    """)


if __name__ == "__main__":
    main()