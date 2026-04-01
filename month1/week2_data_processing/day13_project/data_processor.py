"""
Day 13: 数据处理模块

核心知识点应用：
- Pandas：数据清洗、时间序列处理、聚合统计
- 生成器：流式处理新闻数据

功能：
- 清洗新闻数据（去重、缺失值处理）
- 时间序列处理（日期解析、按日期聚合）
- 流式处理（生成器逐条返回）

作者：AI Agent 工程师学习者
日期：2026-04-01
"""

import pandas as pd
import numpy as np
from typing import Generator, List, Dict, Optional
from datetime import datetime

from sentiment_analyzer import SentimentAnalyzer


# ============================================================
# 数据清洗
# ============================================================

class NewsDataCleaner:
    """
    新闻数据清洗器
    """

    def clean(self, news_list: List[Dict]) -> pd.DataFrame:
        """
        清洗新闻数据

        Args:
            news_list: 新闻列表

        Returns:
            清洗后的 DataFrame
        """
        print(f"[Cleaner] 开始清洗 {len(news_list)} 条新闻")

        # 创建 DataFrame
        df = pd.DataFrame(news_list)

        # 1. 处理缺失值
        df = self._handle_missing_values(df)

        # 2. 去重
        df = self._remove_duplicates(df)

        # 3. 时间处理
        df = self._process_datetime(df)

        # 4. 添加情绪分数
        df = self._add_sentiment(df)

        print(f"[Cleaner] 清洗完成，保留 {len(df)} 条有效新闻")
        return df

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        处理缺失值
        """
        # 检查缺失值
        missing_before = df.isnull().sum().sum()

        # 删除标题或描述为空的记录
        df = df.dropna(subset=['title'])

        # 填充缺失的描述
        if 'description' in df.columns:
            df['description'] = df['description'].fillna(df['title'])

        # 填充缺失的来源
        if 'source' in df.columns:
            df['source'] = df['source'].fillna('Unknown')

        missing_after = df.isnull().sum().sum()
        print(f"[Cleaner] 缺失值处理: {missing_before} -> {missing_after}")

        return df

    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        去除重复记录
        """
        before_count = len(df)

        # 按标题去重
        df = df.drop_duplicates(subset=['title'], keep='first')

        after_count = len(df)
        print(f"[Cleaner] 去重: {before_count} -> {after_count} (删除 {before_count - after_count} 条)")

        return df

    def _process_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        处理日期时间
        """
        if 'published_at' not in df.columns:
            # 如果没有日期列，添加模拟日期
            df['published_at'] = pd.Timestamp.now()
            df['date'] = df['published_at'].dt.date
            return df

        # 转换日期格式
        df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce')

        # 删除无效日期
        df = df.dropna(subset=['published_at'])

        # 提取日期部分
        df['date'] = df['published_at'].dt.date

        # 提取时间特征
        df['hour'] = df['published_at'].dt.hour
        df['weekday'] = df['published_at'].dt.dayofweek

        return df

    def _add_sentiment(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        添加情绪分数
        """
        analyzer = SentimentAnalyzer()

        # 分析标题情绪
        titles = df['title'].tolist()
        title_scores = analyzer.analyze_batch_numpy(titles)
        df['title_sentiment'] = title_scores

        # 分析描述情绪（如果有）
        if 'description' in df.columns:
            descriptions = df['description'].tolist()
            desc_scores = analyzer.analyze_batch_numpy(descriptions)
            df['desc_sentiment'] = desc_scores

            # 综合情绪（标题 + 描述加权平均）
            df['sentiment'] = (df['title_sentiment'] * 0.6 + df['desc_sentiment'] * 0.4)
        else:
            df['sentiment'] = df['title_sentiment']

        # 对于模拟数据，如果有 sentiment_hint，使用它
        if 'sentiment_hint' in df.columns:
            df['sentiment'] = df['sentiment_hint']

        return df


# ============================================================
# 生成器流式处理
# ============================================================

def process_news_stream(news_list: List[Dict]) -> Generator[Dict, None, None]:
    """
    生成器：流式处理新闻数据

    Args:
        news_list: 新闻列表

    Yields:
        处理后的新闻字典
    """
    analyzer = SentimentAnalyzer()

    for i, news in enumerate(news_list):
        # 分析情绪
        sentiment_result = analyzer.analyze_text(news.get('title', ''))

        # 构建处理后的数据
        processed_news = {
            'index': i,
            'title': news.get('title', ''),
            'source': news.get('source', ''),
            'date': news.get('published_at', ''),
            'sentiment': sentiment_result['score'],
            'keywords': sentiment_result['keywords'],
        }

        yield processed_news


def chunk_news_by_date(df: pd.DataFrame) -> Generator[pd.DataFrame, None, None]:
    """
    生成器：按日期分批返回数据

    Args:
        df: 新闻 DataFrame

    Yields:
        按日期分组的 DataFrame
    """
    if 'date' not in df.columns:
        yield df
        return

    for date in df['date'].unique():
        yield df[df['date'] == date]


def filter_news_by_sentiment(
    df: pd.DataFrame,
    sentiment_range: tuple = (-1.0, 1.0)
) -> Generator[pd.Series, None, None]:
    """
    生成器：按情绪筛选新闻

    Args:
        df: 新闻 DataFrame
        sentiment_range: 情绪范围 (min, max)

    Yields:
        符合条件的新闻行
    """
    min_sentiment, max_sentiment = sentiment_range

    for _, row in df.iterrows():
        sentiment = row.get('sentiment', 0)
        if min_sentiment <= sentiment <= max_sentiment:
            yield row


# ============================================================
# 时间序列分析
# ============================================================

class TimeSeriesAnalyzer:
    """
    时间序列分析器
    """

    def aggregate_by_date(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        按日期聚合情绪数据

        Args:
            df: 新闻 DataFrame

        Returns:
            每日聚合结果
        """
        if 'date' not in df.columns:
            print("[TimeSeries] 无日期列，无法聚合")
            return df

        # 按日期聚合
        daily_stats = df.groupby('date').agg({
            'sentiment': ['mean', 'std', 'count', 'min', 'max'],
            'title': 'count',
        })

        # 简化列名
        daily_stats.columns = [
            'sentiment_mean', 'sentiment_std', 'news_count',
            'sentiment_min', 'sentiment_max', 'title_count'
        ]

        # 重置索引
        daily_stats = daily_stats.reset_index()

        return daily_stats

    def calculate_moving_average(
        self,
        daily_df: pd.DataFrame,
        window: int = 7
    ) -> pd.DataFrame:
        """
        计算移动平均

        Args:
            daily_df: 每日数据 DataFrame
            window: 窗口大小

        Returns:
            带移动平均的 DataFrame
        """
        if 'sentiment_mean' not in daily_df.columns:
            return daily_df

        # 使用 Pandas rolling 计算移动平均
        daily_df['sentiment_ma'] = daily_df['sentiment_mean'].rolling(window=window).mean()

        # 使用 NumPy 计算累计均值
        daily_df['sentiment_cummean'] = np.cumsum(daily_df['sentiment_mean']) / np.arange(1, len(daily_df) + 1)

        return daily_df

    def detect_sentiment_trend(self, daily_df: pd.DataFrame) -> Dict:
        """
        检测情绪趋势

        Args:
            daily_df: 每日数据 DataFrame

        Returns:
            趋势分析结果
        """
        if len(daily_df) < 2:
            return {'trend': 'unknown'}

        sentiments = daily_df['sentiment_mean'].values

        # 使用 NumPy 计算趋势
        first_half = np.mean(sentiments[:len(sentiments)//2])
        second_half = np.mean(sentiments[len(sentiments)//2:])
        trend_diff = second_half - first_half

        # 判断趋势
        if trend_diff > 0.1:
            trend = 'improving'
        elif trend_diff < -0.1:
            trend = 'declining'
        else:
            trend = 'stable'

        return {
            'trend': trend,
            'trend_diff': trend_diff,
            'first_half_mean': first_half,
            'second_half_mean': second_half,
        }


# ============================================================
# 统计分析
# ============================================================

class NewsStatisticsAnalyzer:
    """
    新闻统计分析器
    """

    def get_overview(self, df: pd.DataFrame) -> Dict:
        """
        获取数据概览

        Args:
            df: 新闻 DataFrame

        Returns:
            统计概览字典
        """
        return {
            'total_news': len(df),
            'unique_sources': df['source'].nunique() if 'source' in df.columns else 0,
            'date_range': self._get_date_range(df),
            'sentiment_stats': self._get_sentiment_stats(df),
        }

    def _get_date_range(self, df: pd.DataFrame) -> Dict:
        """
        获取日期范围
        """
        if 'date' not in df.columns:
            return {'start': 'N/A', 'end': 'N/A', 'days': 0}

        dates = df['date']
        return {
            'start': str(dates.min()),
            'end': str(dates.max()),
            'days': len(dates.unique()),
        }

    def _get_sentiment_stats(self, df: pd.DataFrame) -> Dict:
        """
        获取情绪统计
        """
        if 'sentiment' not in df.columns:
            return {}

        sentiments = df['sentiment']

        return {
            'mean': sentiments.mean(),
            'median': sentiments.median(),
            'std': sentiments.std(),
            'min': sentiments.min(),
            'max': sentiments.max(),
            'positive_count': (sentiments > 0.1).sum(),
            'negative_count': (sentiments < -0.1).sum(),
            'neutral_count': ((sentiments >= -0.1) & (sentiments <= 0.1)).sum(),
        }

    def analyze_by_source(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        按来源分析
        """
        if 'source' not in df.columns:
            return pd.DataFrame()

        source_stats = df.groupby('source').agg({
            'sentiment': ['mean', 'count'],
            'title': 'count',
        })

        source_stats.columns = ['avg_sentiment', 'news_count', 'title_count']
        source_stats = source_stats.reset_index()
        source_stats = source_stats.sort_values('news_count', ascending=False)

        return source_stats


# ============================================================
# 测试用例
# ============================================================

def test_data_cleaner():
    """测试数据清洗"""
    print("\n" + "=" * 50)
    print("测试数据清洗")
    print("=" * 50)

    # 模拟数据
    test_news = [
        {'title': 'Stock prices surge', 'source': 'Reuters', 'published_at': '2026-04-01T10:00:00', 'sentiment_hint': 0.8},
        {'title': 'Market drops', 'source': 'Bloomberg', 'published_at': '2026-04-01T11:00:00', 'sentiment_hint': -0.6},
        {'title': None, 'source': 'Unknown', 'published_at': '2026-04-01T12:00:00'},  # 缺失标题
        {'title': 'Stock prices surge', 'source': 'CNBC', 'published_at': '2026-04-01T13:00:00', 'sentiment_hint': 0.7},  # 重复
        {'title': 'Tech rally', 'source': None, 'published_at': '2026-04-02T10:00:00', 'sentiment_hint': 0.5},
    ]

    cleaner = NewsDataCleaner()
    df = cleaner.clean(test_news)

    print(f"\n清洗后的 DataFrame:")
    print(df[['title', 'source', 'date', 'sentiment']])


def test_generator_stream():
    """测试生成器流式处理"""
    print("\n" + "=" * 50)
    print("测试生成器流式处理")
    print("=" * 50)

    test_news = [
        {'title': 'Stock prices surge', 'source': 'Reuters'},
        {'title': 'Market drops', 'source': 'Bloomberg'},
        {'title': 'Tech rally', 'source': 'CNBC'},
    ]

    print("\n流式处理输出:")
    for processed in process_news_stream(test_news):
        print(f"  {processed['title']}: sentiment={processed['sentiment']:.3f}")


def test_time_series():
    """测试时间序列分析"""
    print("\n" + "=" * 50)
    print("测试时间序列分析")
    print("=" * 50)

    # 创建测试 DataFrame
    test_news = [
        {'title': 'News 1', 'source': 'Reuters', 'published_at': '2026-04-01', 'sentiment_hint': 0.5},
        {'title': 'News 2', 'source': 'Bloomberg', 'published_at': '2026-04-01', 'sentiment_hint': 0.3},
        {'title': 'News 3', 'source': 'CNBC', 'published_at': '2026-04-02', 'sentiment_hint': -0.2},
        {'title': 'News 4', 'source': 'Reuters', 'published_at': '2026-04-02', 'sentiment_hint': 0.4},
        {'title': 'News 5', 'source': 'Bloomberg', 'published_at': '2026-04-03', 'sentiment_hint': 0.6},
    ]

    cleaner = NewsDataCleaner()
    df = cleaner.clean(test_news)

    # 时间序列分析
    ts_analyzer = TimeSeriesAnalyzer()
    daily_df = ts_analyzer.aggregate_by_date(df)

    print("\n每日聚合结果:")
    print(daily_df)

    # 移动平均
    daily_df = ts_analyzer.calculate_moving_average(daily_df, window=2)
    print("\n移动平均:")
    print(daily_df[['date', 'sentiment_mean', 'sentiment_ma']])

    # 趋势检测
    trend = ts_analyzer.detect_sentiment_trend(daily_df)
    print(f"\n趋势检测: {trend}")


def test_statistics():
    """测试统计分析"""
    print("\n" + "=" * 50)
    print("测试统计分析")
    print("=" * 50)

    # 创建测试 DataFrame
    test_news = [
        {'title': 'News 1', 'source': 'Reuters', 'published_at': '2026-04-01', 'sentiment_hint': 0.5},
        {'title': 'News 2', 'source': 'Bloomberg', 'published_at': '2026-04-01', 'sentiment_hint': -0.3},
        {'title': 'News 3', 'source': 'CNBC', 'published_at': '2026-04-02', 'sentiment_hint': 0.2},
        {'title': 'News 4', 'source': 'Reuters', 'published_at': '2026-04-02', 'sentiment_hint': 0.8},
        {'title': 'News 5', 'source': 'Bloomberg', 'published_at': '2026-04-03', 'sentiment_hint': -0.6},
    ]

    cleaner = NewsDataCleaner()
    df = cleaner.clean(test_news)

    # 统计分析
    stats_analyzer = NewsStatisticsAnalyzer()
    overview = stats_analyzer.get_overview(df)

    print("\n数据概览:")
    for key, value in overview.items():
        print(f"  {key}: {value}")

    # 按来源分析
    source_stats = stats_analyzer.analyze_by_source(df)
    print("\n按来源统计:")
    print(source_stats)


# ============================================================
# 主程序
# ============================================================

def main():
    """运行所有测试"""
    print("=" * 60)
    print("Day 13: data_processor.py 模块测试")
    print("=" * 60)

    test_data_cleaner()
    test_generator_stream()
    test_time_series()
    test_statistics()

    print("\n" + "=" * 60)
    print("✅ data_processor.py 模块测试完成！")
    print("=" * 60)
    print("""
知识点应用总结：
1. ✅ Pandas DataFrame：数据存储和操作
2. ✅ Pandas 数据清洗：dropna、fillna、drop_duplicates
3. ✅ Pandas 时间序列：to_datetime、groupby、rolling
4. ✅ NumPy 统计：cumsum、mean
5. ✅ 生成器：process_news_stream、chunk_news_by_date
    """)


if __name__ == "__main__":
    main()