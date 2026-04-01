"""
Day 13: 综合项目 - 股票新闻情绪分析系统

项目目标：
1. 综合运用 Week 1 + Week 2 所有知识点
2. 实现新闻采集、情绪分析、数据处理、可视化报告

知识点融合：
- Week 1: 装饰器、生成器、上下文管理器、异步编程
- Week 2: NumPy、Pandas 数据处理

项目结构：
├── config.py              # 配置文件
├── news_fetcher.py        # 异步新闻采集
├── sentiment_analyzer.py  # 情绪分析
├── data_processor.py      # 数据处理
├── report_generator.py    # 报告生成
└── news_sentiment_system.py # 主程序（本文件）

作者：AI Agent 工程师学习者
日期：2026-04-01
"""

import asyncio
import os
import sys
from datetime import datetime

# 导入项目模块
from config import OUTPUT_FILES, USE_REAL_API
from news_fetcher import NewsFetcher
from sentiment_analyzer import SentimentAnalyzer, WordFrequencyAnalyzer
from data_processor import NewsDataCleaner, TimeSeriesAnalyzer, NewsStatisticsAnalyzer
from report_generator import SentimentChartGenerator, save_report_to_file


# ============================================================
# 主系统类
# ============================================================

class NewsSentimentSystem:
    """
    新闻情绪分析系统 - 整合所有模块
    """

    def __init__(self):
        self.fetcher = NewsFetcher()
        self.cleaner = NewsDataCleaner()
        self.ts_analyzer = TimeSeriesAnalyzer()
        self.stats_analyzer = NewsStatisticsAnalyzer()
        self.chart_generator = SentimentChartGenerator()
        self.word_analyzer = WordFrequencyAnalyzer()

        self.news_df = None
        self.daily_df = None
        self.raw_news = None

    async def run(self):
        """
        运行完整分析流程
        """
        print("\n" + "=" * 60)
        print("股票新闻情绪分析系统")
        print("=" * 60)
        print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"数据源模式: {'真实API' if USE_REAL_API else '模拟数据'}")
        print("=" * 60)

        # Step 1: 采集新闻
        await self.fetch_news()

        # Step 2: 清洗数据
        self.clean_data()

        # Step 3: 情绪分析
        self.analyze_sentiment()

        # Step 4: 时间序列分析
        self.analyze_time_series()

        # Step 5: 词频分析
        self.analyze_word_frequency()

        # Step 6: 统计分析
        self.generate_statistics()

        # Step 7: 生成可视化
        self.generate_charts()

        # Step 8: 生成报告
        self.generate_report()

        # 完成
        self.print_summary()

    async def fetch_news(self):
        """
        Step 1: 采集新闻数据
        """
        print("\n" + "-" * 40)
        print("Step 1: 新闻采集")
        print("-" * 40)

        self.raw_news = await self.fetcher.fetch_all()
        print(f"采集完成: {len(self.raw_news)} 条新闻")

    def clean_data(self):
        """
        Step 2: 清洗数据
        """
        print("\n" + "-" * 40)
        print("Step 2: 数据清洗")
        print("-" * 40)

        self.news_df = self.cleaner.clean(self.raw_news)
        print(f"清洗完成: {len(self.news_df)} 条有效新闻")

        # 保存清洗后的数据
        self._save_news_csv()

    def _save_news_csv(self):
        """
        保存新闻数据到 CSV
        """
        csv_path = OUTPUT_FILES['news_csv']

        # 确保 data 目录存在
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)

        # 保存 CSV
        columns_to_save = ['title', 'source', 'published_at', 'sentiment']
        if 'description' in self.news_df.columns:
            columns_to_save.insert(2, 'description')

        self.news_df[columns_to_save].to_csv(csv_path, index=False, encoding='utf-8')
        print(f"数据已保存: {csv_path}")

    def analyze_sentiment(self):
        """
        Step 3: 情绪分析
        """
        print("\n" + "-" * 40)
        print("Step 3: 情绪分析")
        print("-" * 40)

        if self.news_df is None or len(self.news_df) == 0:
            print("无数据可分析")
            return

        sentiments = self.news_df['sentiment']

        print(f"平均情绪分数: {sentiments.mean():.3f}")
        print(f"情绪波动(标准差): {sentiments.std():.3f}")
        print(f"正面新闻: {(sentiments > 0.1).sum()} 条")
        print(f"负面新闻: {(sentiments < -0.1).sum()} 条")
        print(f"中性新闻: {((sentiments >= -0.1) & (sentiments <= 0.1)).sum()} 条")

    def analyze_time_series(self):
        """
        Step 4: 时间序列分析
        """
        print("\n" + "-" * 40)
        print("Step 4: 时间序列分析")
        print("-" * 40)

        if self.news_df is None or len(self.news_df) == 0:
            print("无数据可分析")
            return

        # 按日期聚合
        self.daily_df = self.ts_analyzer.aggregate_by_date(self.news_df)

        if self.daily_df is not None and len(self.daily_df) > 0:
            print(f"分析天数: {len(self.daily_df)}")

            # 计算移动平均
            self.daily_df = self.ts_analyzer.calculate_moving_average(self.daily_df, window=7)

            # 检测趋势
            trend = self.ts_analyzer.detect_sentiment_trend(self.daily_df)
            print(f"情绪趋势: {trend['trend']}")
            if trend['trend'] != 'unknown':
                print(f"  前半期均值: {trend['first_half_mean']:.3f}")
                print(f"  后半期均值: {trend['second_half_mean']:.3f}")

    def analyze_word_frequency(self):
        """
        Step 5: 词频分析
        """
        print("\n" + "-" * 40)
        print("Step 5: 词频分析")
        print("-" * 40)

        if self.news_df is None or len(self.news_df) == 0:
            print("无数据可分析")
            return

        # 合并标题和描述作为分析文本
        texts = self.news_df['title'].tolist()
        if 'description' in self.news_df.columns:
            texts = [t + ' ' + d for t, d in zip(self.news_df['title'], self.news_df['description'])]

        # 获取高频词
        top_words = self.word_analyzer.get_top_words(texts, top_n=10)

        print("Top 10 高频词:")
        for i, (word, count) in enumerate(top_words, 1):
            print(f"  {i}. {word}: {count}")

    def generate_statistics(self):
        """
        Step 6: 统计分析
        """
        print("\n" + "-" * 40)
        print("Step 6: 统计分析")
        print("-" * 40)

        if self.news_df is None:
            print("无数据可统计")
            return

        overview = self.stats_analyzer.get_overview(self.news_df)

        print("数据概览:")
        for key, value in overview.items():
            if isinstance(value, dict):
                print(f"  {key}:")
                for k, v in value.items():
                    print(f"    {k}: {v}")
            else:
                print(f"  {key}: {value}")

        # 按来源分析
        if 'source' in self.news_df.columns:
            source_stats = self.stats_analyzer.analyze_by_source(self.news_df)
            print("\n按来源统计:")
            for _, row in source_stats.head(5).iterrows():
                print(f"  {row['source']}: {row['news_count']} 条, 平均情绪 {row['avg_sentiment']:.3f}")

    def generate_charts(self):
        """
        Step 7: 生成可视化图表
        """
        print("\n" + "-" * 40)
        print("Step 7: 可视化图表")
        print("-" * 40)

        chart_path = OUTPUT_FILES['chart_png']

        # 确保 data 目录存在
        os.makedirs(os.path.dirname(chart_path), exist_ok=True)

        # 生成综合图表
        self.chart_generator.plot_comprehensive_report(
            self.news_df,
            self.daily_df,
            chart_path
        )

    def generate_report(self):
        """
        Step 8: 生成分析报告
        """
        print("\n" + "-" * 40)
        print("Step 8: 分析报告")
        print("-" * 40)

        report_path = OUTPUT_FILES['report_txt']

        # 确保 data 目录存在
        os.makedirs(os.path.dirname(report_path), exist_ok=True)

        # 保存报告
        save_report_to_file(self.news_df, self.daily_df, report_path)

    def print_summary(self):
        """
        打印完成摘要
        """
        print("\n" + "=" * 60)
        print("[完成] 分析完成！")
        print("=" * 60)
        print(f"\n输出文件:")
        for name, path in OUTPUT_FILES.items():
            if os.path.exists(path):
                print(f"  {name}: {path}")
            else:
                print(f"  {name}: (未生成)")

        print("\n" + "-" * 40)
        print("知识点应用总结:")
        print("-" * 40)
        print("""
Week 1 知识点：
[OK] 装饰器：@timer 计时、@retry 重试、@cache 缓存、@rate_limit 限速
[OK] 上下文管理器：APISessionManager、fetch_stats_context
     异步编程：asyncio.gather 并发、aiohttp 异步 HTTP
[OK] 生成器：流式处理新闻、分批输出报告

Week 2 知识点：
[OK] NumPy：情绪分数计算、统计运算、布尔索引
[OK] Pandas：数据清洗、时间序列、分组聚合
     可视化：折线图、饼图、条形图、直方图
        """)


# ============================================================
# 主程序入口
# ============================================================

async def main():
    """
    主程序入口
    """
    # 创建系统实例
    system = NewsSentimentSystem()

    # 运行完整分析
    await system.run()


if __name__ == "__main__":
    # 运行主程序
    asyncio.run(main())