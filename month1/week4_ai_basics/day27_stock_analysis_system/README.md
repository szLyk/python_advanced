# Day 27: 月度综合项目 - Python 股票分析系统

## 项目目标

整合 Month 1 学习的所有内容，构建一个完整的 Python 股票分析系统。

## 项目概述

本项目将融合以下技术：
- Python 核心语法（装饰器、异步、上下文管理器）
- 数据处理（NumPy、Pandas）
- API 开发（FastAPI、Pydantic、SQLAlchemy）
- AI 应用（LLM API、Embedding）

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                     股票分析系统                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  数据采集    │───▶│  数据处理    │───▶│  数据存储    │     │
│  │  (异步爬虫)  │    │  (Pandas)   │    │ (SQLite)    │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│          │                  │                  │           │
│          ▼                  ▼                  ▼           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  数据分析    │───▶│  AI 分析    │───▶│  API 服务    │     │
│  │  (NumPy)    │    │ (LLM API)   │    │  (FastAPI)  │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│          │                                      │           │
│          ▼                                      ▼           │
│  ┌─────────────┐                        ┌─────────────┐     │
│  │  报告生成    │                        │  前端展示    │     │
│  │ (LLM 摘要)  │                        │  (可选)     │     │
│  └─────────────┘                        └─────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 功能模块

### 1. 数据采集模块
- 异步爬虫获取股票价格数据
- RSS 新闻抓取
- 数据缓存机制

### 2. 数据处理模块
- 价格数据清洗
- 技术指标计算（均线、波动率）
- 新闻情绪分析

### 3. 数据存储模块
- SQLite 数据库存储
- SQLAlchemy ORM 操作
- 数据查询接口

### 4. AI 分析模块
- LLM 新闻摘要
- Embedding 语义检索
- 投资建议生成

### 5. API 服务模块
- RESTful API 接口
- JWT 认证
- 数据可视化

## 项目结构

```
stock_analysis_system/
├── main.py                 # 主程序入口
├── config.py               # 配置管理
├── database.py             # 数据库连接
├── models.py               # 数据模型
├── services/
│   ├── collector.py        # 数据采集服务
│   ├── analyzer.py         # 数据分析服务
│   ├── ai_service.py       # AI 分析服务
│   └── reporter.py         # 报告生成服务
├── api/
│   ├── routes.py           # API 路由
│   └── schemas.py          # API 数据模型
├── utils/
│   ├── decorators.py       # 装饰器工具
│   ├── async_helper.py     # 异步工具
│   └── cache.py            # 缓存工具
├── requirements.txt        # 依赖包
└── README.md               # 项目说明
```

## 核心代码示例

### 数据采集（异步爬虫）

```python
import aiohttp
import asyncio

async def fetch_stock_data(symbol: str):
    """异步获取股票数据"""
    url = f"https://api.example.com/stock/{symbol}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data

async def fetch_multiple_stocks(symbols: list):
    """批量获取股票数据"""
    tasks = [fetch_stock_data(s) for s in symbols]
    results = await asyncio.gather(*tasks)
    return results
```

### 数据分析（Pandas + NumPy）

```python
import pandas as pd
import numpy as np

def analyze_price_data(prices: pd.DataFrame):
    """分析价格数据"""
    # 计算移动平均
    prices['ma_5'] = prices['close'].rolling(5).mean()
    prices['ma_20'] = prices['close'].rolling(20).mean()

    # 计算波动率
    prices['volatility'] = prices['close'].pct_change().std()

    # 计算涨跌幅
    prices['change_pct'] = (prices['close'] - prices['open']) / prices['open'] * 100

    return prices
```

### AI 分析（LLM API）

```python
async def summarize_news(news_text: str):
    """使用 LLM 摘要新闻"""
    prompt = f"请用一句话总结这条财经新闻：\n{news_text}"

    response = await llm_service.chat(
        prompt,
        system_message="你是财经新闻摘要专家"
    )
    return response

async def generate_analysis_report(stock_data: dict):
    """生成分析报告"""
    prompt = f"""
    根据以下数据生成简要分析报告：
    - 股票代码: {stock_data['symbol']}
    - 当前价格: {stock_data['price']}
    - 5日均价: {stock_data['ma_5']}
    - 波动率: {stock_data['volatility']}
    """
    return await llm_service.chat(prompt)
```

### API 服务（FastAPI）

```python
from fastapi import FastAPI, Depends

app = FastAPI(title="股票分析系统")

@app.get("/stocks/{symbol}")
async def get_stock_analysis(symbol: str):
    """获取股票分析"""
    # 获取数据
    stock_data = await collector.fetch_stock(symbol)
    # 分析
    analysis = await analyzer.analyze(stock_data)
    # 生成报告
    report = await ai_service.generate_report(analysis)
    return {"stock": symbol, "analysis": analysis, "report": report}

@app.get("/news/summary")
async def get_news_summary():
    """获取新闻摘要"""
    news = await collector.fetch_news()
    summaries = await ai_service.summarize_batch(news)
    return summaries
```

## 使用方式

```bash
# 安装依赖
pip install -r requirements.txt

# 运行数据采集
python main.py --collect

# 运行分析
python main.py --analyze --symbol AAPL

# 启动 API 服务
python main.py --serve

# API 文档
http://127.0.0.1:8000/docs
```

## 学习要点

通过本项目，你将学会：
1. 如何整合多个技术模块
2. 异步编程的实际应用
3. 数据处理的完整流程
4. AI API 的调用和集成
5. RESTful API 的设计实践

## 扩展方向

1. 添加实时数据推送（WebSocket）
2. 实现用户关注列表管理
3. 添加数据可视化（图表）
4. 部署到云服务器
5. 添加定时任务（Celery）

## 参考资料

- Month 1 各 Week 学习笔记
- FastAPI 文档
- Pandas 文档
- OpenAI API 文档