# Day 37: Tool 定义

> **日期**: 2026-05-09（周五）  
> **周次**: Week 6 - Agent + Tool 调用  
> **预计耗时**: 2 小时

---

## 今日学习目标

- [ ] 理解 LangChain Tool 的概念
- [ ] 掌握 @tool 装饰器使用
- [ ] 学会自定义工具注册
- [ ] 理解 Tool 描述和参数设计

---

## 学习内容

### 1. 什么是 Tool？

**Tool = Agent 的"手脚"**

```
Agent（大脑）: 决策、思考、选择
  ↓
Tool（手脚）: 执行具体任务
  - 查询股票价格
  - 计算数学公式
  - 搜索网络信息
  - 调用 API
```

### 2. @tool 装饰器基础

```python
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """搜索信息并返回结果"""
    # 实现搜索逻辑
    return f"搜索结果：{query}"
```

**关键要素**：
- 函数名：工具的名称
- 参数：Agent 传递给工具的值
- 返回值：必须是字符串（Agent 能理解的格式）
- 文档字符串：**非常重要**！Agent 靠它理解工具用途

### 3. 带参数的 @tool

```python
@tool
def get_stock_info(symbol: str, field: str = "price") -> str:
    """
    获取股票信息
    
    Args:
        symbol: 股票代码（如"AAPL"、"600519"）
        field: 要查询的字段（price/pe_ratio/market_cap）
    
    Returns:
        股票信息字符串
    """
    stock_data = {
        "AAPL": {"price": "175.5", "pe_ratio": "28.5", "market_cap": "2.8T"},
        "600519": {"price": "1800", "pe_ratio": "30.5", "market_cap": "2.3T"},
    }
    
    if symbol not in stock_data:
        return f"未找到股票：{symbol}"
    
    return f"{symbol} 的{field}为：{stock_data[symbol].get(field, '未知')}"
```

### 4. 自定义 Tool 描述

```python
from langchain.tools import Tool

# 方式 1: 使用 @tool（推荐）
@tool("stock_query")
def query_stock(symbol: str) -> str:
    """查询股票实时数据"""
    ...

# 方式 2: 手动定义（更灵活）
def stock_search(symbol: str) -> str:
    return f"{symbol} 的价格是 100 元"

tool = Tool(
    name="stock_search",
    func=stock_search,
    description="查询股票价格，输入股票代码返回当前价格"
)

# 方式 3: 自定义描述（覆盖默认）
@tool
def calculate(x: float, y: float, operation: str = "add") -> str:
    """计算两个数的运算结果"""
    ...

calculate.description = """
执行数学计算。支持加 (add)、减 (subtract)、乘 (multiply)、除 (divide)。
输入格式：{"x": 数字，"y": 数字，"operation": "操作类型"}
"""
```

### 5. 异步 Tool

```python
from langchain.tools import tool
import asyncio

@tool
async def fetch_stock_news(symbol: str) -> str:
    """异步获取股票新闻"""
    await asyncio.sleep(1)  # 模拟网络请求
    return f"{symbol} 的最新新闻..."
```

### 6. Tool 返回值最佳实践

```python
# ✅ 好的返回值：清晰、结构化
@tool
def get_pe_ratio(symbol: str) -> str:
    """获取市盈率"""
    return f"{symbol} 的 PE 为 25.3，行业平均为 30.1，低于平均水平"

# ❌ 差的返回值：只有数字，缺少上下文
@tool
def get_pe_ratio_bad(symbol: str) -> str:
    return "25.3"  # Agent 不知道这是什么
```

---

## 实践任务

### 任务 1: 基础 Tool 练习 ✅

```python
# custom_tools.py

from langchain.tools import tool

@tool
def add(a: float, b: float) -> str:
    """两个数相加"""
    return str(a + b)

@tool
def multiply(a: float, b: float) -> str:
    """两个数相乘"""
    return str(a * b)

# 测试工具
print(add.invoke({"a": 10, "b": 20}))  # 30
print(multiply.invoke({"a": 5, "b": 6}))  # 30
```

### 任务 2: 股票工具集 ✅

```python
# stock_tools.py

from langchain.tools import tool

# 模拟数据
STOCK_DATA = {
    "AAPL": {"name": "苹果", "price": 175.5, "pe": 28.5, "change": 1.2},
    "GOOGL": {"name": "谷歌", "price": 140.2, "pe": 25.1, "change": -0.5},
    "MSFT": {"name": "微软", "price": 420.8, "pe": 35.2, "change": 2.1},
}

@tool
def get_stock_price(symbol: str) -> str:
    """
    获取股票当前价格
    
    Args:
        symbol: 股票代码，如"AAPL"
    
    Returns:
        股票价格信息
    """
    if symbol not in STOCK_DATA:
        return f"未找到股票：{symbol}"
    data = STOCK_DATA[symbol]
    return f"{data['name']} ({symbol}) 当前价格：${data['price']}"

@tool
def get_stock_pe(symbol: str) -> str:
    """获取股票市盈率"""
    ...

@tool
def get_stock_change(symbol: str) -> str:
    """获取股票涨跌幅"""
    ...

# 创建包含所有股票的 Agent 并测试
```

### 任务 3: 新闻查询工具 ✅

```python
# news_tool.py

@tool
def search_stock_news(symbol: str, days: int = 7) -> str:
    """
    搜索股票相关新闻
    
    Args:
        symbol: 股票代码
        days: 查询最近 N 天的新闻
    
    Returns:
        新闻摘要
    """
    # 模拟新闻数据
    news = [
        f"{symbol} 发布新产品",
        f"{symbol} 季度财报超预期",
        f"分析师上调{symbol}目标价",
    ]
    return "\n".join(news[:days])

# 测试并将工具添加到 Agent
```

---

## 知识点总结

### @tool 装饰器要点

| 要素 | 说明 | 重要性 |
|------|------|--------|
| 函数名 | 工具的内部名称 | ⭐⭐⭐ |
| 参数名 | Agent 传递的变量 | ⭐⭐⭐ |
| 参数类型 | 帮助 Agent 理解格式 | ⭐⭐ |
| 文档字符串 | Agent 理解用途的关键 | ⭐⭐⭐⭐⭐ |
| 返回值 | 必须是字符串 | ⭐⭐⭐⭐ |

### 好的工具描述示例

```python
# ❌ 模糊的描述
"""查询数据"""

# ✅ 清晰的描述
"""
查询股票实时数据。输入股票代码（如"AAPL"、"600519"），
返回当前价格、涨跌幅和成交量。
"""
```

---

## 常见问题

### Q1: 工具不执行怎么办？

```python
# 检查清单：
# 1. 工具是否在 tools 列表中注册
tools = [tool1, tool2, ...]  # 确保包含你的工具

# 2. 描述是否清晰
# Agent 需要理解工具的用途

# 3. 参数名是否匹配
# Agent 传递的参数名必须与函数参数一致
```

### Q2: 如何处理复杂参数？

```python
# 方式 1: 多个简单参数
@tool
def query(symbol: str, field: str, date: str) -> str:
    ...

# 方式 2: JSON 字符串
@tool
def query_json(query_str: str) -> str:
    """
    查询数据。输入 JSON 格式：
    {"symbol": "AAPL", "field": "price", "date": "2024-01-01"}
    """
    import json
    params = json.loads(query_str)
    ...
```

### Q3: 工具返回复杂数据怎么办？

```python
# 将复杂数据转为字符串
import json

@tool
def get_full_info(symbol: str) -> str:
    data = {...}  # 复杂字典
    return json.dumps(data, ensure_ascii=False, indent=2)
```

---

## 代码文件

```
day37_custom_tools/
├── README.md                    # 本文件
├── custom_tools.py              # 基础工具练习
├── stock_tools.py               # 股票工具集
├── news_tool.py                 # 新闻查询工具
└── agent_with_tools.py          # 使用工具的 Agent
```

---

## 参考资源

- [LangChain Tools 文档](https://python.langchain.com/docs/concepts/tools)
- [@tool 装饰器 API](https://api.python.langchain.com/en/latest/tools/langchain.tools.tool.html)
- [LangChain 内置工具](https://python.langchain.com/docs/integrations/tools/)

---

## 下一步

- **Day 38**: Function Calling（API 调用、外部工具集成）
- **明日任务**: 学习如何调用外部 API

---

**💡 今日格言**: "好的工具设计 = 清晰的描述 + 简单的参数 + 有用的返回"
