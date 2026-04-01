# Day 13: 综合项目 - 股票新闻情绪分析系统

## 项目目标
- [x] 综合运用 Week 1 + Week 2 所有知识点
- [x] 实现异步新闻采集
- [x] 进行情绪分析
- [x] 数据处理和可视化
- [x] 生成分析报告

---

## 项目概述

本项目是一个**股票新闻情绪分析系统**，完整融合前两周学习的所有知识点：

| Week | 知识点 | 应用场景 |
|------|--------|----------|
| Week 1 | 装饰器 | @timer 计时、@retry 重试、@cache 缓存、@rate_limit 限速 |
| Week 1 | 上下文管理器 | APISessionManager、fetch_stats_context |
| Week 1 | 异步编程 | asyncio.gather 并发、aiohttp 异步 HTTP |
| Week 1 | 生成器 | 流式处理新闻、分批输出报告 |
| Week 2 | NumPy | 情绪分数计算、统计运算、布尔索引 |
| Week 2 | Pandas | 数据清洗、时间序列、分组聚合 |
| Week 2 | 可视化 | 折线图、饼图、条形图、直方图 |

---

## 项目结构

```
day13_project/
├── config.py                   # 配置文件（API Key、情绪词典等）
├── news_fetcher.py             # 异步新闻采集模块
├── sentiment_analyzer.py       # 情绪分析模块
├── data_processor.py           # 数据处理模块
├── report_generator.py         # 报告生成模块
├── news_sentiment_system.py    # 主程序入口
├── stock_analysis.py           # （旧）股票数据分析
├── README.md                   # 项目说明
└── data/
    ├── news_data.csv           # 新闻数据
    ├── sentiment_report.txt    # 分析报告
    └── sentiment_chart.png     # 情绪趋势图
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install aiohttp pandas numpy matplotlib
```

### 2. 运行程序

```bash
python news_sentiment_system.py
```

### 3. 使用真实 API（可选）

编辑 `config.py`：

```python
USE_REAL_API = True  # 切换为真实 API

API_KEYS = {
    'newsapi': 'YOUR_API_KEY',  # 注册: https://newsapi.org/register
    'gnews': 'YOUR_API_KEY',     # 注册: https://gnews.io/register
}
```

---

## 核心功能

### 1. 异步新闻采集 (`news_fetcher.py`)

```python
# 装饰器应用
@timer(unit='s')
@retry(max_attempts=3, delay=1)
@rate_limit(calls_per_second=1.0)
async def fetch_news():
    ...

# 上下文管理器
async with APISessionManager("NewsFetcher") as manager:
    ...
```

### 2. 情绪分析 (`sentiment_analyzer.py`)

```python
# NumPy 批量计算
scores = analyzer.analyze_batch_numpy(texts)

# 统计结果
stats = analyzer.get_statistics(scores)
```

### 3. 数据处理 (`data_processor.py`)

```python
# Pandas 数据清洗
df = cleaner.clean(news_list)

# 时间序列分析
daily_df = ts_analyzer.aggregate_by_date(df)

# 生成器流式处理
for news in process_news_stream(news_list):
    ...
```

### 4. 可视化报告 (`report_generator.py`)

```python
# 生成综合图表
chart_generator.plot_comprehensive_report(df, daily_df, 'chart.png')

# 生成文本报告
save_report_to_file(df, daily_df, 'report.txt')
```

---

## 输出示例

### 分析报告 (`sentiment_report.txt`)

```
==================================================
股票新闻情绪分析报告
==================================================

一、数据概要
----------------------------------------
总新闻数: 20
日期范围: 2026-02-10 至 2026-02-16

二、情绪统计
----------------------------------------
平均情绪分数: 0.039
正面新闻数: 10 (50.0%)
负面新闻数: 10 (50.0%)

三、趋势分析
----------------------------------------
情绪趋势: 稳定

四、典型新闻
----------------------------------------
最正面新闻:
  [0.810] Cryptocurrency market sees unprecedented gains
  [0.758] Stock prices surge amid positive earnings report

最负面新闻:
  [-0.683] Oil prices plunge due to supply surplus
  [-0.677] Market drops as inflation concerns grow
```

---

## 学习成果

完成本项目后，你将掌握：

1. **装饰器实战**：计时、重试、缓存、限速
2. **异步编程**：并发请求、Session 管理
3. **上下文管理器**：资源管理、统计追踪
4. **生成器应用**：流式处理大数据
5. **NumPy 向量化**：高效数值计算
6. **Pandas 数据处理**：清洗、聚合、时间序列
7. **可视化**：多图表综合展示

---

## 后续扩展

- 接入真实新闻 API（NewsAPI / GNews）
- 添加更多情绪词典（金融专用）
- 实现情绪预警功能
- 对接股票价格数据进行关联分析
- 使用 LLM 进行深度情绪分析

---

## 今日产出
- [x] config.py - 配置文件
- [x] news_fetcher.py - 异步新闻采集
- [x] sentiment_analyzer.py - 情绪分析
- [x] data_processor.py - 数据处理
- [x] report_generator.py - 报告生成
- [x] news_sentiment_system.py - 主程序
- [x] data/news_data.csv - 新闻数据
- [x] data/sentiment_report.txt - 分析报告
- [x] data/sentiment_chart.png - 情绪趋势图