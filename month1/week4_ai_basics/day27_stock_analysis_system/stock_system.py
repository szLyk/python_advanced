"""
Day 27: 月度综合项目 - Python 股票分析系统

整合 Month 1 学习内容：
- Python 核心（装饰器、异步）
- 数据处理（NumPy、Pandas）
- API 开发（FastAPI、SQLAlchemy）
- AI 应用（LLM、Embedding）
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from functools import wraps
from contextlib import asynccontextmanager
import numpy as np
import pandas as pd

# ============================================
# 1. 工具装饰器
# ============================================

def timer(func):
    """计时装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[Timer] {func.__name__} 执行时间: {end - start:.2f}s")
        return result
    return wrapper


def async_timer(func):
    """异步计时装饰器"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        print(f"[Timer] {func.__name__} 执行时间: {end - start:.2f}s")
        return result
    return wrapper


def cache_result(expire_seconds: int = 60):
    """结果缓存装饰器"""
    cache = {}

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key in cache:
                cached_data, cached_time = cache[key]
                if time.time() - cached_time < expire_seconds:
                    print(f"[Cache] 使用缓存结果: {func.__name__}")
                    return cached_data

            result = func(*args, **kwargs)
            cache[key] = (result, time.time())
            return result
        return wrapper
    return decorator


def retry(max_retries: int = 3, delay: float = 1.0):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i < max_retries - 1:
                        print(f"[Retry] {func.__name__} 第{i+1}次失败，等待重试...")
                        time.sleep(delay)
                    else:
                        raise e
        return wrapper
    return decorator


def log_call(func):
    """调用日志装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[Log] 调用 {func.__name__}，参数: args={args[:2]}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[Log] {func.__name__} 返回: {str(result)[:50]}...")
        return result
    return wrapper


# ============================================
# 2. 异步上下文管理器
# ============================================

@asynccontextmanager
async def async_db_connection():
    """模拟异步数据库连接"""
    print("[DB] 连接数据库...")
    conn = {"connected": True, "queries": []}
    try:
        yield conn
    finally:
        print(f"[DB] 关闭数据库连接，执行了 {len(conn['queries'])} 次查询")


class AsyncResource:
    """异步资源管理"""

    async def __aenter__(self):
        print("[Resource] 获取资源...")
        self.data = {"status": "ready"}
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("[Resource] 释放资源...")
        self.data = {"status": "closed"}


# ============================================
# 3. 数据模型
# ============================================

class StockData:
    """股票数据模型"""

    def __init__(self, symbol: str, name: str):
        self.symbol = symbol
        self.name = name
        self.prices: List[Dict] = []
        self.news: List[Dict] = []

    def add_price(self, date: str, open: float, close: float, high: float, low: float, volume: int):
        self.prices.append({
            "date": date,
            "open": open,
            "close": close,
            "high": high,
            "low": low,
            "volume": volume
        })

    def to_dataframe(self) -> pd.DataFrame:
        """转换为 DataFrame"""
        return pd.DataFrame(self.prices)


class AnalysisResult:
    """分析结果模型"""

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.current_price: float = 0
        self.ma_5: float = 0
        self.ma_20: float = 0
        self.volatility: float = 0
        self.change_pct: float = 0
        self.news_summary: str = ""
        self.sentiment: str = ""
        self.recommendation: str = ""

    def to_dict(self) -> Dict:
        return {
            "symbol": self.symbol,
            "current_price": self.current_price,
            "ma_5": self.ma_5,
            "ma_20": self.ma_20,
            "volatility": self.volatility,
            "change_pct": self.change_pct,
            "news_summary": self.news_summary,
            "sentiment": self.sentiment,
            "recommendation": self.recommendation,
            "generated_at": datetime.now().isoformat()
        }


# ============================================
# 4. 数据采集服务（模拟）
# ============================================

class DataCollector:
    """数据采集服务"""

    @staticmethod
    @timer
    @cache_result(expire_seconds=120)
    def fetch_stock_price(symbol: str) -> Dict:
        """获取股票价格（模拟）"""
        # 模拟数据
        mock_data = {
            "AAPL": {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "price": 150.25,
                "history": [
                    {"date": "2026-04-01", "open": 148.0, "close": 150.0, "high": 151.0, "low": 147.5, "volume": 5000000},
                    {"date": "2026-04-02", "open": 150.0, "close": 152.0, "high": 153.0, "low": 149.5, "volume": 6000000},
                    {"date": "2026-04-03", "open": 152.0, "close": 151.5, "high": 154.0, "low": 151.0, "volume": 4500000},
                    {"date": "2026-04-04", "open": 151.5, "close": 150.25, "high": 152.5, "low": 149.0, "volume": 5500000},
                    {"date": "2026-04-05", "open": 150.0, "close": 155.0, "high": 156.0, "low": 149.5, "volume": 7000000},
                ]
            },
            "GOOGL": {
                "symbol": "GOOGL",
                "name": "Google",
                "price": 2800.50,
                "history": [
                    {"date": "2026-04-01", "open": 2750, "close": 2780, "high": 2790, "low": 2740, "volume": 2000000},
                    {"date": "2026-04-02", "open": 2780, "close": 2800, "high": 2810, "low": 2775, "volume": 2100000},
                    {"date": "2026-04-03", "open": 2800, "close": 2790, "high": 2820, "low": 2785, "volume": 1900000},
                    {"date": "2026-04-04", "open": 2790, "close": 2800.50, "high": 2815, "low": 2780, "volume": 2200000},
                    {"date": "2026-04-05", "open": 2800, "close": 2850, "high": 2860, "low": 2795, "volume": 2500000},
                ]
            },
            "TSLA": {
                "symbol": "TSLA",
                "name": "Tesla",
                "price": 750.80,
                "history": [
                    {"date": "2026-04-01", "open": 720, "close": 740, "high": 745, "low": 715, "volume": 8000000},
                    {"date": "2026-04-02", "open": 740, "close": 750, "high": 755, "low": 735, "volume": 8500000},
                    {"date": "2026-04-03", "open": 750, "close": 745, "high": 760, "low": 740, "volume": 7000000},
                    {"date": "2026-04-04", "open": 745, "close": 750.80, "high": 758, "low": 742, "volume": 7500000},
                    {"date": "2026-04-05", "open": 750, "close": 780, "high": 785, "low": 748, "volume": 9000000},
                ]
            }
        }
        return mock_data.get(symbol.upper(), {"error": "Stock not found"})

    @staticmethod
    @async_timer
    async def fetch_news_async(symbol: str) -> List[Dict]:
        """异步获取新闻（模拟）"""
        await asyncio.sleep(0.1)  # 模拟网络延迟

        mock_news = {
            "AAPL": [
                {"title": "苹果发布新产品，股价大涨", "content": "苹果公司今日发布新款iPhone...", "date": "2026-04-05"},
                {"title": "苹果财报超预期", "content": "苹果公司第二季度财报...", "date": "2026-04-04"},
            ],
            "GOOGL": [
                {"title": "谷歌AI技术突破", "content": "谷歌宣布AI领域重大进展...", "date": "2026-04-05"},
                {"title": "谷歌云业务增长强劲", "content": "谷歌云服务收入...", "date": "2026-04-04"},
            ],
            "TSLA": [
                {"title": "特斯拉交付量创新高", "content": "特斯拉第一季度交付...", "date": "2026-04-05"},
                {"title": "特斯拉工厂扩张计划", "content": "特斯拉宣布新工厂...", "date": "2026-04-04"},
            ]
        }
        return mock_news.get(symbol.upper(), [])

    @staticmethod
    async def fetch_multiple_stocks(symbols: List[str]) -> Dict:
        """批量获取股票数据"""
        tasks = [DataCollector.fetch_news_async(s) for s in symbols]
        results = await asyncio.gather(*tasks)
        return {symbol: news for symbol, news in zip(symbols, results)}


# ============================================
# 5. 数据分析服务
# ============================================

class DataAnalyzer:
    """数据分析服务"""

    @staticmethod
    @timer
    @log_call
    def calculate_technical_indicators(price_history: List[Dict]) -> Dict:
        """计算技术指标"""
        df = pd.DataFrame(price_history)

        # 计算移动平均
        df['ma_5'] = df['close'].rolling(5).mean()
        df['ma_20'] = df['close'].rolling(20).mean() if len(df) >= 20 else df['close'].mean()

        # 计算波动率（使用 NumPy）
        prices = np.array(df['close'])
        volatility = np.std(prices) / np.mean(prices) * 100  # 相对波动率

        # 计算涨跌幅
        df['change_pct'] = (df['close'] - df['open']) / df['open'] * 100

        # 最新数据
        latest = df.iloc[-1]

        return {
            "current_price": latest['close'],
            "ma_5": latest['ma_5'],
            "ma_20": latest['ma_20'] if len(df) >= 20 else df['close'].mean(),
            "volatility": volatility,
            "change_pct": latest['change_pct'],
            "price_data": df.to_dict('records')
        }

    @staticmethod
    def analyze_trend(indicators: Dict) -> str:
        """分析趋势"""
        current = indicators['current_price']
        ma_5 = indicators['ma_5']

        if current > ma_5 * 1.02:
            return "上升趋势"
        elif current < ma_5 * 0.98:
            return "下降趋势"
        else:
            return "横盘整理"

    @staticmethod
    def calculate_risk_level(indicators: Dict) -> str:
        """计算风险等级"""
        volatility = indicators['volatility']

        if volatility < 10:
            return "低风险"
        elif volatility < 20:
            return "中等风险"
        else:
            return "高风险"


# ============================================
# 6. AI 分析服务（模拟）
# ============================================

class AIAnalysisService:
    """AI 分析服务"""

    @staticmethod
    @async_timer
    async def summarize_news(news_list: List[Dict]) -> str:
        """摘要新闻（模拟 LLM）"""
        if not news_list:
            return "暂无新闻"

        await asyncio.sleep(0.2)  # 模拟 API 调用延迟

        # 模拟摘要
        titles = [n['title'] for n in news_list[:3]]
        return f"核心新闻：{', '.join(titles)}。总体消息偏向正面。"

    @staticmethod
    @async_timer
    async def analyze_sentiment(news_list: List[Dict]) -> str:
        """情绪分析（模拟）"""
        await asyncio.sleep(0.1)

        positive_words = ['大涨', '增长', '创新高', '超预期', '突破']
        negative_words = ['下跌', '暴跌', '亏损', '利空', '风险']

        pos_count = 0
        neg_count = 0

        for news in news_list:
            title = news['title']
            pos_count += sum(1 for w in positive_words if w in title)
            neg_count += sum(1 for w in negative_words if w in title)

        if pos_count > neg_count:
            return "正面"
        elif neg_count > pos_count:
            return "负面"
        else:
            return "中性"

    @staticmethod
    @async_timer
    async def generate_recommendation(indicators: Dict, sentiment: str) -> str:
        """生成投资建议（模拟 LLM）"""
        await asyncio.sleep(0.3)

        trend = DataAnalyzer.analyze_trend(indicators)
        risk = DataAnalyzer.calculate_risk_level(indicators)

        recommendations = {
            ("上升趋势", "正面", "低风险"): "建议买入，市场情绪良好，风险较低",
            ("上升趋势", "正面", "中等风险"): "可考虑买入，但需注意波动",
            ("上升趋势", "负面", "低风险"): "谨慎持有，等待市场情绪改善",
            ("下降趋势", "正面", "低风险"): "建议观望，等待趋势确认",
            ("下降趋势", "负面", "高风险"): "建议回避，市场风险较大",
        }

        key = (trend, sentiment, risk)
        return recommendations.get(key, "建议观望，综合分析后再决策")


# ============================================
# 7. 报告生成器
# ============================================

class ReportGenerator:
    """报告生成器"""

    @staticmethod
    @timer
    def generate_full_report(symbol: str, indicators: Dict, news_summary: str,
                            sentiment: str, recommendation: str) -> Dict:
        """生成完整分析报告"""
        report = {
            "report_id": f"{symbol}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "symbol": symbol,
            "generated_at": datetime.now().isoformat(),

            "price_analysis": {
                "current_price": indicators['current_price'],
                "moving_average_5": round(indicators['ma_5'], 2),
                "moving_average_20": round(indicators['ma_20'], 2),
                "daily_change": f"{indicators['change_pct']:.2f}%",
                "volatility": f"{indicators['volatility']:.2f}%"
            },

            "trend_analysis": {
                "trend": DataAnalyzer.analyze_trend(indicators),
                "risk_level": DataAnalyzer.calculate_risk_level(indicators)
            },

            "news_analysis": {
                "summary": news_summary,
                "sentiment": sentiment
            },

            "recommendation": recommendation,

            "summary": f"""
{symbol} 分析摘要：
- 当前价格: ${indicators['current_price']}
- 趋势判断: {DataAnalyzer.analyze_trend(indicators)}
- 新闻情绪: {sentiment}
- 投资建议: {recommendation}
            """.strip()
        }

        return report


# ============================================
# 8. 完整分析流程
# ============================================

class StockAnalysisSystem:
    """股票分析系统"""

    def __init__(self):
        self.collector = DataCollector()
        self.analyzer = DataAnalyzer()
        self.ai_service = AIAnalysisService()
        self.reporter = ReportGenerator()

    @timer
    async def analyze_stock(self, symbol: str) -> Dict:
        """完整股票分析流程"""
        print(f"\n{'='*60}")
        print(f"开始分析股票: {symbol}")
        print(f"{'='*60}")

        # 1. 数据采集
        print("\n[Step 1] 数据采集...")
        stock_data = self.collector.fetch_stock_price(symbol)

        if "error" in stock_data:
            return {"error": f"股票 {symbol} 不存在"}

        # 异步获取新闻
        news_list = await self.collector.fetch_news_async(symbol)

        # 2. 技术分析
        print("\n[Step 2] 技术分析...")
        indicators = self.analyzer.calculate_technical_indicators(stock_data['history'])

        # 3. AI 分析
        print("\n[Step 3] AI 分析...")
        news_summary = await self.ai_service.summarize_news(news_list)
        sentiment = await self.ai_service.analyze_sentiment(news_list)
        recommendation = await self.ai_service.generate_recommendation(indicators, sentiment)

        # 4. 生成报告
        print("\n[Step 4] 生成报告...")
        report = self.reporter.generate_full_report(
            symbol, indicators, news_summary, sentiment, recommendation
        )

        print(f"\n{'='*60}")
        print("分析完成！")
        print(f"{'='*60}")

        return report

    async def analyze_multiple_stocks(self, symbols: List[str]) -> Dict:
        """批量分析股票"""
        print(f"\n批量分析 {len(symbols)} 只股票...")

        tasks = [self.analyze_stock(s) for s in symbols]
        results = await asyncio.gather(*tasks)

        return {s: r for s, r in zip(symbols, results)}


# ============================================
# 9. FastAPI 集成（简化版）
# ============================================

try:
    from fastapi import FastAPI
    import uvicorn

    app = FastAPI(title="股票分析系统 API", version="1.0.0")
    system = StockAnalysisSystem()

    @app.get("/")
    async def root():
        return {"message": "股票分析系统", "version": "1.0.0", "docs": "/docs"}

    @app.get("/analyze/{symbol}")
    async def analyze_stock_api(symbol: str):
        """API 分析股票"""
        report = await system.analyze_stock(symbol)
        return report

    @app.get("/analyze/batch")
    async def analyze_batch_api(symbols: str):
        """批量分析（symbols 用逗号分隔）"""
        symbol_list = symbols.split(",")
        results = await system.analyze_multiple_stocks(symbol_list)
        return results

    def run_api_server():
        """运行 API 服务"""
        print("启动 API 服务...")
        print("API 文档: http://127.0.0.1:8000/docs")
        uvicorn.run(app, host="127.0.0.1", port=8000)

except ImportError:
    print("FastAPI 未安装，跳过 API 服务模块")
    app = None


# ============================================
# 10. 演示代码
# ============================================

async def demo_single_analysis():
    """演示单股票分析"""
    print("\n=== 单股票分析演示 ===")

    system = StockAnalysisSystem()
    report = await system.analyze_stock("AAPL")

    print("\n分析报告:")
    print(json.dumps(report, indent=2, ensure_ascii=False))


async def demo_batch_analysis():
    """演示批量分析"""
    print("\n=== 批量分析演示 ===")

    system = StockAnalysisSystem()
    results = await system.analyze_multiple_stocks(["AAPL", "GOOGL", "TSLA"])

    for symbol, report in results.items():
        print(f"\n{symbol} 投资建议: {report.get('recommendation', 'N/A')}")


async def demo_async_context():
    """演示异步上下文管理"""
    print("\n=== 异步上下文管理演示 ===")

    async with async_db_connection() as conn:
        print(f"数据库状态: {conn['connected']}")
        conn['queries'].append("SELECT * FROM stocks")
        conn['queries'].append("SELECT * FROM history")

    async with AsyncResource() as resource:
        print(f"资源状态: {resource.data}")


def demo_decorators():
    """演示装饰器"""
    print("\n=== 装饰器演示 ===")

    @timer
    @retry(max_retries=3)
    def unstable_function():
        """模拟不稳定函数"""
        import random
        if random.random() < 0.5:
            raise Exception("随机失败")
        return "成功执行"

    try:
        result = unstable_function()
        print(f"结果: {result}")
    except Exception as e:
        print(f"最终失败: {e}")

    # 缓存演示
    @cache_result(expire_seconds=10)
    def expensive_calculation(n: int):
        print(f"执行计算 n={n}")
        return n * n

    print(expensive_calculation(5))  # 第一次执行
    print(expensive_calculation(5))  # 使用缓存


async def demo_pandas_numpy():
    """演示 Pandas + NumPy 分析"""
    print("\n=== Pandas + NumPy 分析演示 ===")

    # 模拟价格数据
    data = {
        'date': pd.date_range('2026-04-01', periods=30),
        'close': np.random.uniform(140, 160, 30)
    }
    df = pd.DataFrame(data)

    # NumPy 计算
    prices = np.array(df['close'])
    print(f"均价: {np.mean(prices):.2f}")
    print(f"最高: {np.max(prices):.2f}")
    print(f"最低: {np.min(prices):.2f}")
    print(f"波动率: {np.std(prices):.2f}")

    # Pandas 计算
    df['ma_5'] = df['close'].rolling(5).mean()
    df['ma_10'] = df['close'].rolling(10).mean()
    df['change'] = df['close'].pct_change() * 100

    print(f"\n最近5日数据:")
    print(df.tail())


# ============================================
# 主程序
# ============================================

async def main():
    """主程序"""
    print("Day 27: Python 股票分析系统 - 月度综合项目")
    print("=" * 60)

    # 演示各种功能
    demo_decorators()
    await demo_async_context()
    await demo_pandas_numpy()
    await demo_single_analysis()
    await demo_batch_analysis()

    print("\n" + "=" * 60)
    print("项目总结:")
    print("1. 装饰器用于计时、缓存、重试、日志")
    print("2. 异步编程提高数据采集效率")
    print("3. NumPy/Pandas 用于数据分析和计算")
    print("4. AI服务模拟LLM摘要和情绪分析")
    print("5. FastAPI 提供 RESTful API 服务")

    print("\n启动API服务:")
    print("运行: python stock_system.py --serve")


if __name__ == "__main__":
    import sys

    if "--serve" in sys.argv and app:
        run_api_server()
    else:
        asyncio.run(main())