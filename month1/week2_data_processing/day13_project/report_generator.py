"""
Day 13: 报告生成模块

核心知识点应用：
- Matplotlib：可视化图表
- 生成器：分批输出报告内容

功能：
- 情绪趋势折线图
- 情绪分布饼图
- 新闻热度条形图
- 文本报告生成
- 生成器流式输出

作者：AI Agent 工程师学习者
日期：2026-04-01
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from typing import Generator, Dict
from datetime import datetime
import os

from config import CHART_CONFIG, OUTPUT_FILES


# ============================================================
# 可视化图表
# ============================================================

class SentimentChartGenerator:
    """
    情绪图表生成器
    """

    def __init__(self):
        self.figsize = CHART_CONFIG['figure_size']
        self.dpi = CHART_CONFIG['dpi']
        self._setup_style()

    def _setup_style(self):
        """
        设置图表样式
        """
        try:
            plt.style.use('seaborn-v0_8-whitegrid')
        except:
            plt.style.use('ggplot')

        # 设置中文字体（如果支持）
        try:
            plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial']
            plt.rcParams['axes.unicode_minus'] = False
        except:
            pass

    def plot_sentiment_trend(self, daily_df: pd.DataFrame, save_path: str = None):
        """
        绘制情绪趋势图

        Args:
            daily_df: 每日情绪数据 DataFrame
            save_path: 保存路径（可选）
        """
        if 'sentiment_mean' not in daily_df.columns or len(daily_df) == 0:
            print("[Chart] 无数据可绘制")
            return

        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        # 转换日期
        dates = pd.to_datetime(daily_df['date'])
        sentiments = daily_df['sentiment_mean']

        # 绘制主线
        ax.plot(dates, sentiments, 'b-', linewidth=2, label='Daily Sentiment', marker='o', markersize=4)

        # 绘制移动平均线（如果有）
        if 'sentiment_ma' in daily_df.columns:
            ma = daily_df['sentiment_ma']
            ax.plot(dates, ma, 'r--', linewidth=2, label='7-Day MA', alpha=0.7)

        # 绘制零线
        ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)

        # 绘制正负区域
        ax.fill_between(dates, sentiments, 0,
                        where=(sentiments > 0),
                        color='green', alpha=0.2, label='Positive Zone')
        ax.fill_between(dates, sentiments, 0,
                        where=(sentiments < 0),
                        color='red', alpha=0.2, label='Negative Zone')

        # 设置标题和标签
        ax.set_title('Market Sentiment Trend', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Sentiment Score', fontsize=12)

        # 设置日期格式
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        plt.xticks(rotation=45)

        # 设置 Y 轴范围
        ax.set_ylim(-1, 1)

        # 图例
        ax.legend(loc='upper right')

        # 网格
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        # 保存图片
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"[Chart] 图片已保存: {save_path}")
        else:
            plt.show()

        plt.close()

    def plot_sentiment_distribution(self, df: pd.DataFrame, save_path: str = None):
        """
        绘制情绪分布饼图

        Args:
            df: 新闻 DataFrame
            save_path: 保存路径（可选）
        """
        if 'sentiment' not in df.columns:
            print("[Chart] 无情绪数据")
            return

        sentiments = df['sentiment']

        # 分类统计
        positive = (sentiments > 0.1).sum()
        negative = (sentiments < -0.1).sum()
        neutral = len(sentiments) - positive - negative

        # 创建饼图
        fig, ax = plt.subplots(figsize=(8, 8), dpi=self.dpi)

        sizes = [positive, neutral, negative]
        labels = ['Positive', 'Neutral', 'Negative']
        colors = ['#2ecc71', '#95a5a6', '#e74c3c']
        explode = (0.05, 0, 0.05)

        # 只绘制非零部分
        non_zero_sizes = [(s, l, c, e) for s, l, c, e in zip(sizes, labels, colors, explode) if s > 0]

        if non_zero_sizes:
            sizes_nz, labels_nz, colors_nz, explode_nz = zip(*non_zero_sizes)

            wedges, texts, autotexts = ax.pie(
                sizes_nz,
                labels=labels_nz,
                colors=colors_nz,
                explode=explode_nz,
                autopct='%1.1f%%',
                startangle=90,
                textprops={'fontsize': 12}
            )

            ax.set_title('Sentiment Distribution', fontsize=14, fontweight='bold')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"[Chart] 分布图已保存: {save_path}")
        else:
            plt.show()

        plt.close()

    def plot_news_count_by_date(self, daily_df: pd.DataFrame, save_path: str = None):
        """
        绘制每日新闻数量条形图

        Args:
            daily_df: 每日数据 DataFrame
            save_path: 保存路径（可选）
        """
        if 'news_count' not in daily_df.columns or len(daily_df) == 0:
            print("[Chart] 无新闻数据")
            return

        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        dates = pd.to_datetime(daily_df['date'])
        counts = daily_df['news_count']

        # 根据情绪设置颜色
        colors = []
        if 'sentiment_mean' in daily_df.columns:
            for s in daily_df['sentiment_mean']:
                if s > 0.1:
                    colors.append('#2ecc71')  # 绿色
                elif s < -0.1:
                    colors.append('#e74c3c')  # 红色
                else:
                    colors.append('#95a5a6')  # 灰色
        else:
            colors = ['#3498db'] * len(dates)

        ax.bar(dates, counts, color=colors, alpha=0.7, edgecolor='black')

        ax.set_title('Daily News Count', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('News Count', fontsize=12)

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)

        ax.grid(True, axis='y', alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"[Chart] 条形图已保存: {save_path}")
        else:
            plt.show()

        plt.close()

    def plot_comprehensive_report(self, df: pd.DataFrame, daily_df: pd.DataFrame, save_path: str = None):
        """
        绘制综合报告图表（多子图）

        Args:
            df: 新闻 DataFrame
            daily_df: 每日数据 DataFrame
            save_path: 保存路径（可选）
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=self.dpi)

        # 1. 情绪趋势（左上）
        ax1 = axes[0, 0]
        if 'sentiment_mean' in daily_df.columns and len(daily_df) > 0:
            dates = pd.to_datetime(daily_df['date'])
            sentiments = daily_df['sentiment_mean']
            ax1.plot(dates, sentiments, 'b-', linewidth=2, marker='o', markersize=4)
            ax1.fill_between(dates, sentiments, 0, where=(sentiments > 0), color='green', alpha=0.3)
            ax1.fill_between(dates, sentiments, 0, where=(sentiments < 0), color='red', alpha=0.3)
            ax1.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
            ax1.set_title('Sentiment Trend')
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Score')
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        else:
            ax1.text(0.5, 0.5, 'No Data', ha='center', va='center')
            ax1.set_title('Sentiment Trend')

        # 2. 情绪分布（右上）
        ax2 = axes[0, 1]
        if 'sentiment' in df.columns:
            sentiments = df['sentiment']
            positive = (sentiments > 0.1).sum()
            negative = (sentiments < -0.1).sum()
            neutral = len(sentiments) - positive - negative

            sizes = [positive, neutral, negative]
            labels = ['Positive', 'Neutral', 'Negative']
            colors = ['#2ecc71', '#95a5a6', '#e74c3c']

            non_zero = [(s, l, c) for s, l, c in zip(sizes, labels, colors) if s > 0]
            if non_zero:
                sizes_nz, labels_nz, colors_nz = zip(*non_zero)
                ax2.pie(sizes_nz, labels=labels_nz, colors=colors_nz, autopct='%1.1f%%', startangle=90)
            ax2.set_title('Sentiment Distribution')
        else:
            ax2.text(0.5, 0.5, 'No Data', ha='center', va='center')
            ax2.set_title('Sentiment Distribution')

        # 3. 新闻数量（左下）
        ax3 = axes[1, 0]
        if 'news_count' in daily_df.columns and len(daily_df) > 0:
            dates = pd.to_datetime(daily_df['date'])
            counts = daily_df['news_count']
            ax3.bar(dates, counts, color='#3498db', alpha=0.7)
            ax3.set_title('Daily News Count')
            ax3.set_xlabel('Date')
            ax3.set_ylabel('Count')
            ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
            plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
        else:
            ax3.text(0.5, 0.5, 'No Data', ha='center', va='center')
            ax3.set_title('Daily News Count')

        # 4. 情绪直方图（右下）
        ax4 = axes[1, 1]
        if 'sentiment' in df.columns:
            ax4.hist(df['sentiment'], bins=20, color='#9b59b6', alpha=0.7, edgecolor='black')
            ax4.axvline(x=0, color='red', linestyle='--', alpha=0.5)
            ax4.set_title('Sentiment Histogram')
            ax4.set_xlabel('Sentiment Score')
            ax4.set_ylabel('Frequency')
        else:
            ax4.text(0.5, 0.5, 'No Data', ha='center', va='center')
            ax4.set_title('Sentiment Histogram')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"[Chart] 综合图表已保存: {save_path}")
        else:
            plt.show()

        plt.close()


# ============================================================
# 文本报告生成
# ============================================================

def generate_report_sections(df: pd.DataFrame, daily_df: pd.DataFrame) -> Generator[str, None, None]:
    """
    生成器：分批输出报告内容

    Args:
        df: 新闻 DataFrame
        daily_df: 每日数据 DataFrame

    Yields:
        报告文本段落
    """
    # 标题
    yield "=" * 50
    yield "股票新闻情绪分析报告"
    yield "=" * 50
    yield f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    yield ""

    # 概要统计
    yield "一、数据概要"
    yield "-" * 40
    yield f"总新闻数: {len(df)}"
    if 'date' in df.columns:
        yield f"日期范围: {df['date'].min()} 至 {df['date'].max()}"
    if 'source' in df.columns:
        yield f"新闻来源: {df['source'].nunique()} 个"
    yield ""

    # 情绪统计
    yield "二、情绪统计"
    yield "-" * 40
    if 'sentiment' in df.columns:
        sentiments = df['sentiment']
        yield f"平均情绪分数: {sentiments.mean():.3f}"
        yield f"情绪标准差: {sentiments.std():.3f}"
        yield f"最高情绪分数: {sentiments.max():.3f}"
        yield f"最低情绪分数: {sentiments.min():.3f}"
        yield ""
        yield f"正面新闻数: {(sentiments > 0.1).sum()} ({(sentiments > 0.1).sum()/len(df)*100:.1f}%)"
        yield f"负面新闻数: {(sentiments < -0.1).sum()} ({(sentiments < -0.1).sum()/len(df)*100:.1f}%)"
        yield f"中性新闻数: {((sentiments >= -0.1) & (sentiments <= 0.1)).sum()}"
    yield ""

    # 趋势分析
    yield "三、趋势分析"
    yield "-" * 40
    if 'sentiment_mean' in daily_df.columns and len(daily_df) >= 2:
        sentiments_ts = daily_df['sentiment_mean'].values
        first_half = np.mean(sentiments_ts[:len(sentiments_ts)//2])
        second_half = np.mean(sentiments_ts[len(sentiments_ts)//2:])
        trend_diff = second_half - first_half

        if trend_diff > 0.1:
            yield f"情绪趋势: 改善 (后半期比前半期高 {trend_diff:.3f})"
        elif trend_diff < -0.1:
            yield f"情绪趋势: 下降 (后半期比前半期低 {abs(trend_diff):.3f})"
        else:
            yield f"情绪趋势: 稳定 (变化幅度 {abs(trend_diff):.3f})"
    else:
        yield "情绪趋势: 数据不足，无法分析"
    yield ""

    # 来源分析
    yield "四、来源分析"
    yield "-" * 40
    if 'source' in df.columns:
        source_counts = df['source'].value_counts().head(5)
        for source, count in source_counts.items():
            avg_sentiment = df[df['source'] == source]['sentiment'].mean()
            yield f"{source}: {count} 条新闻, 平均情绪 {avg_sentiment:.3f}"
    yield ""

    # 典型新闻
    yield "五、典型新闻"
    yield "-" * 40
    if 'sentiment' in df.columns and 'title' in df.columns:
        # 最正面新闻
        most_positive = df.nlargest(3, 'sentiment')
        yield "最正面新闻:"
        for _, row in most_positive.iterrows():
            yield f"  [{row['sentiment']:.3f}] {row['title']}"
        yield ""

        # 最负面新闻
        most_negative = df.nsmallest(3, 'sentiment')
        yield "最负面新闻:"
        for _, row in most_negative.iterrows():
            yield f"  [{row['sentiment']:.3f}] {row['title']}"
    yield ""

    # 结论
    yield "六、分析结论"
    yield "-" * 40
    if 'sentiment' in df.columns:
        avg_sentiment = df['sentiment'].mean()
        if avg_sentiment > 0.2:
            yield "整体市场情绪偏正面，投资者信心较强。"
        elif avg_sentiment < -0.2:
            yield "整体市场情绪偏负面，投资者较为悲观。"
        else:
            yield "整体市场情绪中性，投资者观望态度明显。"
    yield ""

    yield "=" * 50
    yield "报告结束"
    yield "=" * 50


def save_report_to_file(df: pd.DataFrame, daily_df: pd.DataFrame, filepath: str):
    """
    保存报告到文件

    Args:
        df: 新闻 DataFrame
        daily_df: 每日数据 DataFrame
        filepath: 文件路径
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        for section in generate_report_sections(df, daily_df):
            f.write(section + '\n')

    print(f"[Report] 报告已保存: {filepath}")


# ============================================================
# 测试用例
# ============================================================

def test_chart_generation():
    """测试图表生成"""
    print("\n" + "=" * 50)
    print("测试图表生成")
    print("=" * 50)

    # 创建测试数据
    test_news = [
        {'title': 'News 1', 'source': 'Reuters', 'published_at': '2026-04-01', 'sentiment_hint': 0.5},
        {'title': 'News 2', 'source': 'Bloomberg', 'published_at': '2026-04-01', 'sentiment_hint': -0.3},
        {'title': 'News 3', 'source': 'CNBC', 'published_at': '2026-04-02', 'sentiment_hint': 0.2},
        {'title': 'News 4', 'source': 'Reuters', 'published_at': '2026-04-02', 'sentiment_hint': 0.8},
        {'title': 'News 5', 'source': 'Bloomberg', 'published_at': '2026-04-03', 'sentiment_hint': -0.6},
    ]

    # 导入数据处理模块
    from data_processor import NewsDataCleaner, TimeSeriesAnalyzer

    cleaner = NewsDataCleaner()
    df = cleaner.clean(test_news)

    ts_analyzer = TimeSeriesAnalyzer()
    daily_df = ts_analyzer.aggregate_by_date(df)

    # 创建图表目录
    os.makedirs('data', exist_ok=True)

    # 生成图表
    chart_gen = SentimentChartGenerator()
    chart_gen.plot_sentiment_trend(daily_df, 'data/test_trend.png')
    chart_gen.plot_sentiment_distribution(df, 'data/test_distribution.png')
    chart_gen.plot_news_count_by_date(daily_df, 'data/test_count.png')
    chart_gen.plot_comprehensive_report(df, daily_df, 'data/test_comprehensive.png')

    print("\n图表生成测试完成")


def test_report_generation():
    """测试报告生成"""
    print("\n" + "=" * 50)
    print("测试报告生成")
    print("=" * 50)

    # 创建测试数据
    test_news = [
        {'title': 'Stock prices surge to record high', 'source': 'Reuters', 'published_at': '2026-04-01', 'sentiment_hint': 0.8},
        {'title': 'Market crashes on recession fears', 'source': 'Bloomberg', 'published_at': '2026-04-01', 'sentiment_hint': -0.6},
        {'title': 'Tech stocks rally on AI news', 'source': 'CNBC', 'published_at': '2026-04-02', 'sentiment_hint': 0.5},
        {'title': 'Investors worried about rate hike', 'source': 'Reuters', 'published_at': '2026-04-02', 'sentiment_hint': -0.4},
        {'title': 'Company reports stable growth', 'source': 'Bloomberg', 'published_at': '2026-04-03', 'sentiment_hint': 0.2},
    ]

    from data_processor import NewsDataCleaner, TimeSeriesAnalyzer

    cleaner = NewsDataCleaner()
    df = cleaner.clean(test_news)

    ts_analyzer = TimeSeriesAnalyzer()
    daily_df = ts_analyzer.aggregate_by_date(df)

    # 流式输出报告
    print("\n流式输出报告内容:")
    for section in generate_report_sections(df, daily_df):
        print(section)

    # 保存报告
    save_report_to_file(df, daily_df, 'data/test_report.txt')


# ============================================================
# 主程序
# ============================================================

def main():
    """运行所有测试"""
    print("=" * 60)
    print("Day 13: report_generator.py 模块测试")
    print("=" * 60)

    test_chart_generation()
    test_report_generation()

    print("\n" + "=" * 60)
    print("✅ report_generator.py 模块测试完成！")
    print("=" * 60)
    print("""
知识点应用总结：
1. ✅ Matplotlib 绑图：折线图、饼图、条形图、直方图
2. ✅ Matplotlib 多子图：subplot 2x2 布局
3. ✅ 生成器：generate_report_sections 流式输出报告内容
4. ✅ 文件操作：保存图表和报告文件
    """)


if __name__ == "__main__":
    main()