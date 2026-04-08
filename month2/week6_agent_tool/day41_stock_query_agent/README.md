# Day 41: 综合项目 - 股票查询 Agent

> **日期**: 2026-05-13（周二）  
> **周次**: Week 6 - Agent + Tool 调用  
> **预计耗时**: 6 小时

---

## 项目目标

创建一个完整的股票查询 Agent，能够：

- [ ] 理解自然语言查询
- [ ] 调用多个股票数据工具
- [ ] 支持多轮对话记忆
- [ ] 返回结构化的股票信息

---

## 项目架构

```
┌─────────────────────────────────────────────────────────┐
│                  股票查询 Agent 架构                     │
├─────────────────────────────────────────────────────────┤
│  用户输入                                                │
│  "帮我分析下贵州茅台，价格和估值怎么样？"                │
│                          ↓                              │
├─────────────────────────────────────────────────────────┤
│  Agent (ReAct 决策)                                      │
│  Thought: 用户需要了解茅台的价格和估值                  │
│  Action: 调用 get_stock_price                           │
│  Action: 调用 get_pe_ratio                              │
│  Action: 调用 get_company_info                          │
│                          ↓                              │
├─────────────────────────────────────────────────────────┤
│  Tools (工具执行)                                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ 价格查询    │  │ 估值查询    │  │ 公司信息    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                          ↓                              │
├─────────────────────────────────────────────────────────┤
│  Memory (对话记忆)                                       │
│  记录用户偏好和历史查询                                  │
│                          ↓                              │
├─────────────────────────────────────────────────────────┤
│  最终回答                                                │
│  "贵州茅台 (600519) 当前价格 1800 元，PE 约 30.5 倍..."    │
└─────────────────────────────────────────────────────────┘
```

---

## 项目结构

```
day41_stock_query_agent/
├── README.md                      # 本文件
├── main.py                        # 主程序入口
├── agent/
│   ├── stock_agent.py             # Agent 创建
│   └── agent_prompts.py           # Agent Prompt 配置
├── tools/
│   ├── stock_price_tool.py        # 价格查询工具
│   ├── stock_info_tool.py         # 股票信息工具
│   ├── stock_chart_tool.py        # K 线数据工具
│   └── stock_news_tool.py         # 新闻查询工具
├── memory/
│   └── conversation_memory.py     # 对话记忆配置
├── data/
│   └── mock_stock_data.py         # 模拟股票数据
└── requirements.txt               # 依赖清单
```

---

## 实现步骤

### Step 1: 模拟股票数据

```python
# data/mock_stock_data.py

STOCK_DATA = {
    "600519": {
        "name": "贵州茅台",
        "price": 1800.0,
        "change": 1.5,
        "change_pct": 0.08,
        "pe_ratio": 30.5,
        "pb_ratio": 8.2,
        "market_cap": "2.3 万亿",
        "volume": 1250000,
        "industry": "白酒",
        "description": "中国高端白酒龙头企业"
    },
    "000858": {
        "name": "五粮液",
        "price": 150.0,
        "change": -0.8,
        "change_pct": -0.53,
        "pe_ratio": 25.3,
        "pb_ratio": 6.5,
        "market_cap": "5800 亿",
        "volume": 980000,
        "industry": "白酒",
        "description": "中国浓香型白酒代表"
    },
    "300750": {
        "name": "宁德时代",
        "price": 180.0,
        "change": 3.2,
        "change_pct": 1.81,
        "pe_ratio": 20.1,
        "pb_ratio": 4.8,
        "market_cap": "7800 亿",
        "volume": 2100000,
        "industry": "新能源",
        "description": "全球动力电池龙头企业"
    },
}

def get_stock_by_name_or_code(query: str) -> str:
    """根据名称或代码查找股票"""
    for code, data in STOCK_DATA.items():
        if query in code or query in data["name"]:
            return code
    return None
```

### Step 2: 创建工具集

```python
# tools/stock_price_tool.py

from langchain.tools import tool
from data.mock_stock_data import STOCK_DATA, get_stock_by_name_or_code

@tool
def get_stock_price(query: str) -> str:
    """
    获取股票当前价格
    
    Args:
        query: 股票名称或代码，如"茅台"或"600519"
    
    Returns:
        股票价格信息
    """
    code = get_stock_by_name_or_code(query)
    if not code:
        return f"未找到股票：{query}"
    
    data = STOCK_DATA[code]
    return (
        f"{data['name']} ({code})\n"
        f"当前价格：{data['price']} 元\n"
        f"涨跌：{data['change']} ({data['change_pct']}%)"
    )
```

```python
# tools/stock_info_tool.py

from langchain.tools import tool
from data.mock_stock_data import STOCK_DATA, get_stock_by_name_or_code

@tool
def get_stock_info(query: str) -> str:
    """
    获取股票基本信息
    
    Args:
        query: 股票名称或代码
    
    Returns:
        股票详细信息
    """
    code = get_stock_by_name_or_code(query)
    if not code:
        return f"未找到股票：{query}"
    
    data = STOCK_DATA[code]
    return (
        f"{data['name']} ({code})\n"
        f"所属行业：{data['industry']}\n"
        f"市盈率 (PE): {data['pe_ratio']}\n"
        f"市净率 (PB): {data['pb_ratio']}\n"
        f"市值：{data['market_cap']}\n"
        f"公司简介：{data['description']}"
    )
```

```python
# tools/stock_news_tool.py

from langchain.tools import tool
import random

@tool
def get_stock_news(query: str, days: int = 7) -> str:
    """
    获取股票相关新闻
    
    Args:
        query: 股票名称或代码
        days: 查询最近 N 天的新闻
    
    Returns:
        新闻摘要列表
    """
    code = get_stock_by_name_or_code(query)
    if not code:
        return f"未找到股票：{query}"
    
    # 模拟新闻数据
    news_templates = [
        "{name} 发布最新季度财报，营收同比增长 X%",
        "{name} 新产品发布，市场反响热烈",
        "分析师上调{name}目标价至 X 元",
        "{name} 与某知名企业达成战略合作",
        "{name} 获得机构投资者增持",
    ]
    
    from data.mock_stock_data import STOCK_DATA
    name = STOCK_DATA[code]["name"]
    
    news = []
    for i in range(min(days, 5)):
        template = random.choice(news_templates)
        news_item = template.replace("{name}", name).replace("X", str(random.randint(10, 50)))
        news.append(f"[{i+1}天前] {news_item}")
    
    return "\n".join(news)
```

### Step 3: Agent 配置

```python
# agent/stock_agent.py

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from tools.stock_price_tool import get_stock_price
from tools.stock_info_tool import get_stock_info
from tools.stock_news_tool import get_stock_news
from agent.agent_prompts import STOCK_AGENT_PROMPT

def create_stock_agent():
    """创建股票查询 Agent"""
    
    # 工具列表
    tools = [get_stock_price, get_stock_info, get_stock_news]
    
    # LLM 配置
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.3,  # 较低温度让回答更稳定
        max_tokens=1000
    )
    
    # Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", STOCK_AGENT_PROMPT),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    # 记忆
    memory = ConversationSummaryBufferMemory(
        llm=llm,
        memory_key="chat_history",
        return_messages=True,
        max_token_limit=2000
    )
    
    # 创建 Agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # 创建执行器
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10
    )
    
    return executor
```

```python
# agent/agent_prompts.py

STOCK_AGENT_PROMPT = """你是一位专业的股票分析助手，具备以下能力：

1. 查询股票实时价格
2. 获取股票基本信息（PE、PB、市值等）
3. 获取股票相关新闻

回答规则：
- 使用专业但易懂的语言
- 数据要准确，不确定时要说明
- 主动提供相关建议
- 如果用户提到"它"、"这个"等代词，根据上下文理解指代的股票
- 比较股票时要清晰列出差异

如果用户查询的股票不存在，友好地提示用户重新输入。"""
```

### Step 4: 主程序

```python
# main.py

from agent.stock_agent import create_stock_agent

def main():
    """主函数"""
    print("=" * 60)
    print("🤖 股票查询 Agent")
    print("=" * 60)
    print("支持功能：")
    print("  - 查询股票价格")
    print("  - 获取股票信息")
    print("  - 查看相关新闻")
    print("  - 多轮对话分析")
    print("\n输入'退出'结束对话")
    print("=" * 60)
    
    agent = create_stock_agent()
    
    while True:
        user_input = input("\n📝 请输入：").strip()
        
        if user_input.lower() in ["退出", "exit", "quit"]:
            print("👋 再见！")
            break
        
        if not user_input:
            continue
        
        try:
            response = agent.invoke({"input": user_input})
            print(f"\n🤖 {response['output']}")
        except Exception as e:
            print(f"\n❌ 发生错误：{e}")

if __name__ == "__main__":
    main()
```

---

## 运行测试

```bash
# 进入项目目录
cd day41_stock_query_agent

# 运行主程序
python main.py

# 示例对话
📝 请输入：帮我看看贵州茅台的情况
🤖 贵州茅台 (600519) 是白酒行业龙头企业，当前价格 1800 元...

📝 请输入：它的 PE 是多少
🤖 茅台的市盈率约为 30.5 倍...

📝 请输入：那五粮液呢
🤖 五粮液 (000858) 当前价格 150 元，PE 约 25.3 倍...
```

---

## 功能扩展

### 扩展 1: 接入真实 API

```python
# 替换模拟数据为真实 API
import requests

@tool
def get_real_stock_price(query: str) -> str:
    """使用新浪财经 API 获取真实价格"""
    code = get_stock_by_name_or_code(query)
    if not code:
        return f"未找到股票：{query}"
    
    # 转换代码格式（sz/sh）
    if code.startswith("6"):
        symbol = f"sh{code}"
    else:
        symbol = f"sz{code}"
    
    url = f"http://hq.sinajs.cn/list={symbol}"
    response = requests.get(url, timeout=5)
    # 解析返回数据...
```

### 扩展 2: 添加技术分析工具

```python
@tool
def get_technical_indicators(query: str) -> str:
    """获取技术指标（MA、MACD、KDJ 等）"""
    ...
```

### 扩展 3: 添加投资建议

```python
@tool
def get_investment_advice(query: str) -> str:
    """基于多维度分析给出投资建议"""
    ...
```

---

## 项目检查清单

- [ ] 所有工具正常工作
- [ ] Agent 能正确选择工具
- [ ] 多轮对话记忆有效
- [ ] 错误处理完善
- [ ] 回答格式清晰
- [ ] 代码已提交 GitHub

---

## 常见问题

### Q1: Agent 总是调用错误工具？
- 检查工具的 description 是否清晰
- 优化 Prompt 中的指导
- 减少相似工具的数量

### Q2: 记忆不生效？
- 检查 memory_key 是否与 Prompt 匹配
- 确认 memory 已传给 AgentExecutor
- 检查 return_messages=True

### Q3: 如何调试 Agent？
```python
# verbose=True 查看完整思考过程
executor = AgentExecutor(..., verbose=True)
```

---

## 参考资源

- [LangChain Agent 示例](https://github.com/langchain-ai/langchain/blob/master/cookbook/agent_examples.ipynb)
- [股票 API 汇总](https://github.com/topics/stock-api)

---

## 下一步

- **Week 7**: 向量数据库（Milvus）
- **Day 43**: Embedding 和向量数据库概念

---

**🎉 恭喜完成 Week 6！你已掌握 Agent + Tool 的核心能力！**
