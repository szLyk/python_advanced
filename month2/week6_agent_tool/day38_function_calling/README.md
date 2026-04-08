# Day 38: Function Calling

> **日期**: 2026-05-10（周六）  
> **周次**: Week 6 - Agent + Tool 调用  
> **预计耗时**: 2 小时

---

## 今日学习目标

- [ ] 理解 Function Calling 原理
- [ ] 学会外部 API 调用
- [ ] 掌握工具选择和调用机制
- [ ] 了解错误处理方法

---

## 学习内容

### 1. Function Calling 是什么？

Function Calling 是 LLM 的一种能力，让模型能够：
- 理解可用的函数列表
- 决定调用哪个函数
- 生成正确的函数参数

```
传统 LLM:
  输入："北京今天天气怎么样？"
  输出："北京今天天气晴朗，气温 25 度..." （基于训练数据，可能过时）

Function Calling:
  输入："北京今天天气怎么样？"
  输出：[调用 get_weather("北京")] → 返回实时数据 → 组织答案
```

### 2. LangChain 中的 Function Calling

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

llm = ChatOpenAI(model="gpt-3.5-turbo")

# 定义函数 schema
functions = [
    {
        "name": "get_stock_price",
        "description": "获取股票当前价格",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "股票代码，如'AAPL'"
                }
            },
            "required": ["symbol"]
        }
    }
]

# 绑定函数到 LLM
llm_with_functions = llm.bind(functions=functions)

# 调用
response = llm_with_functions.invoke("苹果股票现在多少钱？")
print(response.additional_kwargs.get("function_call"))
# 输出：{"name": "get_stock_price", "arguments": {"symbol": "AAPL"}}
```

### 3. 实际 API 调用

```python
import requests
from langchain.tools import tool

@tool
def get_real_stock_price(symbol: str) -> str:
    """
    获取股票实时价格（调用真实 API）
    
    Args:
        symbol: 股票代码
    """
    try:
        # 使用新浪财经 API（示例）
        url = f"http://hq.sinajs.cn/list={symbol}"
        response = requests.get(url, timeout=5)
        data = response.text
        
        # 解析返回数据
        # 格式：var hq_str_sz000001="平安银行，10.50,..."
        if "=" in data:
            parts = data.split("=")[1].strip('"').split(",")
            name = parts[0]
            price = parts[3]
            change = float(parts[3]) - float(parts[2])
            change_pct = (change / float(parts[2])) * 100
            return f"{name} 当前价格：{price}，涨跌：{change:.2f} ({change_pct:.2f}%)"
        return "数据解析失败"
    except Exception as e:
        return f"API 调用失败：{str(e)}"
```

### 4. 多工具协调

```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 定义多个工具
@tool
def get_price(symbol: str) -> str:
    """获取股票价格"""
    ...

@tool
def get_pe(symbol: str) -> str:
    """获取市盈率"""
    ...

@tool
def get_news(symbol: str) -> str:
    """获取相关新闻"""
    ...

tools = [get_price, get_pe, get_news]

# 创建 Agent
llm = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是股票分析助手"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 复杂查询会自动调用多个工具
result = executor.invoke({"input": "帮我分析下苹果股票，价格和估值怎么样？"})
```

### 5. 错误处理

```python
from langchain.tools import tool

@tool
def safe_api_call(symbol: str) -> str:
    """安全调用 API"""
    try:
        # 模拟 API 调用
        result = risky_operation(symbol)
        return f"成功：{result}"
    except requests.Timeout:
        return "API 请求超时，请稍后重试"
    except requests.ConnectionError:
        return "网络连接失败，请检查网络"
    except Exception as e:
        return f"发生错误：{str(e)}"

# Agent 级别错误处理
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    handle_parsing_errors=True,  # 自动修复解析错误
    max_iterations=5,  # 防止无限循环
    max_execution_time=30,  # 超时限制
)
```

---

## 实践任务

### 任务 1: 调用模拟 API ✅

```python
# function_calling.py

from langchain.tools import tool
import random

@tool
def get_stock_price_api(symbol: str) -> str:
    """
    模拟股票价格 API
    
    Args:
        symbol: 股票代码
    """
    # 模拟实时价格
    prices = {
        "AAPL": 175.5 + random.uniform(-2, 2),
        "GOOGL": 140.2 + random.uniform(-2, 2),
        "MSFT": 420.8 + random.uniform(-5, 5),
    }
    price = prices.get(symbol, 100.0)
    return f"{symbol} 实时价格：${price:.2f}"

# 测试
print(get_stock_price_api.invoke({"symbol": "AAPL"}))
```

### 任务 2: 真实 API 集成 ✅

```python
# real_api_call.py

import requests
from langchain.tools import tool

@tool
def get_exchange_rate(from_currency: str, to_currency: str) -> str:
    """
    获取汇率（使用真实 API）
    
    Args:
        from_currency: 源货币（如"USD"）
        to_currency: 目标货币（如"CNY"）
    """
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url, timeout=5)
    data = response.json()
    
    rate = data["rates"].get(to_currency, 1.0)
    return f"1 {from_currency} = {rate} {to_currency}"

# 测试并集成到 Agent
```

### 任务 3: 股票分析完整流程 ✅

```python
# stock_analysis_workflow.py

# 创建一个多工具 Agent，能够：
# 1. 查询股票价格
# 2. 获取市盈率
# 3. 获取公司新闻
# 4. 综合给出分析

# 测试问题：
# - "苹果股票现在多少钱？"
# - "茅台的估值高吗？"
# - "帮我分析下微软股票"
```

---

## 知识点总结

| 概念 | 说明 |
|------|------|
| Function Schema | 函数的 JSON Schema 定义 |
| Tool Binding | 将工具绑定到 LLM |
| Tool Calling | LLM 决定调用工具 |
| Error Handling | 超时、重试、降级处理 |

### API 调用最佳实践

```python
# ✅ 推荐做法
@tool
def safe_tool(param: str) -> str:
    try:
        result = api_call(param)
        return f"成功：{result}"
    except TimeoutError:
        return "请求超时"
    except Exception as e:
        return f"错误：{e}"

# ❌ 避免做法
@tool
def unsafe_tool(param: str) -> str:
    # 没有任何错误处理
    return api_call(param)
```

---

## 常见问题

### Q1: Function Calling 和 Tool 有什么区别？

- **Function Calling**: LLM 的原生能力，输出函数调用格式
- **Tool**: LangChain 的封装，统一接口
- 实际使用中，两者经常配合

### Q2: 如何处理 API 限流？

```python
import time
from functools import wraps

def rate_limit(calls_per_second=1):
    def decorator(func):
        last_call = [0]
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < 1/calls_per_second:
                time.sleep(1/calls_per_second - elapsed)
            last_call[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(calls_per_second=2)
@tool
def api_tool(...):
    ...
```

### Q3: 免费股票 API 推荐？

- 新浪财经 API（无需 key）
- 雅虎财经（yfinance 库）
- 聚宽数据（注册送额度）
- Alpha Vantage（免费 5 次/分钟）

---

## 代码文件

```
day38_function_calling/
├── README.md                    # 本文件
├── function_calling.py          # 基础练习
├── real_api_call.py             # 真实 API 调用
├── stock_analysis_workflow.py   # 完整工作流
└── error_handling.py            # 错误处理示例
```

---

## 参考资源

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [LangChain Tools](https://python.langchain.com/docs/concepts/tools)
- [新浪财经 API](https://github.com/shidenggui/easytrader)

---

## 下一步

- **Day 39**: 记忆管理（ConversationBufferMemory）
- **明日任务**: 学习多轮对话记忆

---

**💡 今日格言**: "Function Calling 让 AI 从'知道'变成'做到'"
