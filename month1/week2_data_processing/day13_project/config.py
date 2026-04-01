"""
Day 13 项目配置文件

数据源配置：
- 默认使用模拟数据（稳定、可演示）
- 注册 NewsAPI/GNews 后可切换真实 API

注册地址：
- NewsAPI: https://newsapi.org/register
- GNews: https://gnews.io/register

安全说明：
- API Keys 存储在 .env 文件中，该文件已在 .gitignore 中排除
- 请勿在代码中硬编码 API Keys
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件（从当前目录或父目录）
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# ============================================================
# 数据源切换
# ============================================================

USE_REAL_API = True  # False = 模拟数据, True = 真实 API

# API Keys（从 .env 文件读取）
API_KEYS = {
    'newsapi': os.getenv('NEWSAPI_API_KEY', ''),
    'gnews': os.getenv('GNEWS_API_KEY', ''),
}

# RSS.app 自定义源（从 .env 读取）
RSS_APP_REUTERS_URL = os.getenv('RSS_APP_REUTERS_URL', '')

# API 端点
API_ENDPOINTS = {
    'newsapi': 'https://newsapi.org/v2/everything',
    'gnews': 'https://gnews.io/api/v4/search',
}

# RSS 源配置
# 主要源：Google News RSS（稳定可靠）
# 备用源：rss.app（第三方聚合，偶发不稳定）
RSS_SOURCES = {
    # === 主要源（优先使用）===
    'reuters_via_google': {
        # 路透社官方 RSS 已废弃，使用 Google News 过滤路透社新闻
        'url': 'https://news.google.com/rss/search?q=reuters+business&hl=en-US&gl=US&ceid=US:en',
        'name': 'Reuters (via Google News)',
        'priority': 1,
    },
    'google_business': {
        # Google News 商业新闻聚合
        'url': 'https://news.google.com/rss/search?q=stock+market+finance&hl=en-US&gl=US&ceid=US:en',
        'name': 'Google News Business',
        'priority': 1,
    },
    'bbc_business': {
        'url': 'https://feeds.bbci.co.uk/news/business/rss.xml',
        'name': 'BBC Business',
        'priority': 2,
    },
    'cnbc_markets': {
        'url': 'https://www.cnbc.com/id/10000664/device/rss/rss.html',
        'name': 'CNBC Markets',
        'priority': 2,
    },
    'marketwatch': {
        'url': 'https://www.marketwatch.com/rss/topstories',
        'name': 'MarketWatch',
        'priority': 2,
    },
    # === 备用源（网络不稳定时可能失败）===
    'reuters_rssapp': {
        # rss.app 自定义聚合的路透社财经新闻（URL 从 .env 读取）
        'url': RSS_APP_REUTERS_URL if RSS_APP_REUTERS_URL else 'https://rss.app/feeds/EtHhREsCL5E9uxbA.xml',
        'name': 'Reuters Finance (rss.app)',
        'priority': 3,
    },
}

# API 查询参数
API_PARAMS = {
    'newsapi': {
        'q': 'stock OR market OR finance OR economy',
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 50,
    },
    'gnews': {
        'q': 'stock market finance',
        'lang': 'en',
        'max': 50,
    },
}

# ============================================================
# 模拟数据配置
# ============================================================

MOCK_NEWS_COUNT = 50  # 模拟新闻数量

# 模拟新闻模板（标题 + 情绪倾向）
MOCK_NEWS_TEMPLATES = [
    ("Stock prices surge amid positive earnings report", 0.8),
    ("Market drops as inflation concerns grow", -0.6),
    ("Tech stocks rally on AI breakthrough news", 0.7),
    ("Investors worried about interest rate hike", -0.5),
    ("Federal Reserve signals potential rate cut", 0.4),
    ("Oil prices plunge due to supply surplus", -0.7),
    ("Banking sector shows strong quarterly growth", 0.6),
    ("Trade tensions escalate affecting global markets", -0.5),
    ("Cryptocurrency market sees unprecedented gains", 0.9),
    ("Retail stocks decline on weak consumer spending", -0.4),
    ("Manufacturing sector rebounds with new orders", 0.5),
    ("Housing market slowdown raises recession fears", -0.6),
    ("Green energy stocks boom on policy support", 0.8),
    ("Supply chain disruptions hit tech companies", -0.5),
    ("S&P 500 reaches new all-time high", 0.7),
    ("Bond yields spike triggering stock sell-off", -0.6),
    ("Semiconductor shortage impacts auto industry", -0.4),
    ("Cloud computing giants report record profits", 0.6),
    ("Currency volatility affects international trade", -0.3),
    ("Pharma stocks surge on vaccine approval news", 0.5),
]

# ============================================================
# 情绪分析配置
# ============================================================

# 正面情绪关键词
POSITIVE_WORDS = [
    'rise', 'rising', 'surge', 'surging', 'gain', 'gaining',
    'profit', 'profits', 'growth', 'growing', 'rally', 'rallying',
    'boom', 'booming', 'increase', 'increasing', 'up', 'higher',
    'positive', 'strong', 'strength', 'success', 'successful',
    'record', 'all-time', 'high', 'peak', 'recover', 'recovery',
    'beat', 'beating', 'exceed', 'exceeding', 'outperform',
    'bullish', 'buy', 'upgrade', 'optimistic', 'hope', 'hopeful',
]

# 负面情绪关键词
NEGATIVE_WORDS = [
    'fall', 'falling', 'drop', 'dropping', 'decline', 'declining',
    'loss', 'losses', 'plunge', 'plunging', 'crash', 'crashing',
    'sink', 'sinking', 'down', 'lower', 'decrease', 'decreasing',
    'negative', 'weak', 'weakness', 'fail', 'failure', 'failed',
    'recession', 'crisis', 'concern', 'concerns', 'worried',
    'fear', 'fears', 'sell', 'selling', 'sell-off', 'bearish',
    'downgrade', 'pessimistic', 'risk', 'risky', 'short',
    'miss', 'missing', 'underperform', 'worse', 'worst',
]

# ============================================================
# 可视化配置
# ============================================================

CHART_CONFIG = {
    'figure_size': (12, 8),
    'dpi': 100,
    'style': 'seaborn-v0_8-whitegrid',
}

# ============================================================
# 输出文件配置
# ============================================================

OUTPUT_FILES = {
    'news_csv': 'data/news_data.csv',
    'report_txt': 'data/sentiment_report.txt',
    'chart_png': 'data/sentiment_chart.png',
}