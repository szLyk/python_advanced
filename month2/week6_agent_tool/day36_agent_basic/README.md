# Day 36: Agent 基础

> **日期**: 2026-05-08（周四）  
> **周次**: Week 6 - Agent + Tool 调用  
> **预计耗时**: 2 小时

---

## 今日学习目标

- [ ] 理解 Agent 的概念和作用
- [ ] 掌握 ReAct 模式原理
- [ ] 了解 LangChain Agent 类型
- [ ] 能够运行简单的 Zero-shot Agent

---

## 学习内容

### 1. 什么是 Agent？

**Agent = LLM + 决策能力 + 工具使用**

```
传统 LLM:
  输入 → [LLM] → 输出（仅基于训练知识）

Agent:
  输入 → [LLM 思考] → 选择工具 → 执行 → 观察结果 → 再思考 → ... → 最终输出
```

### 2. ReAct 模式（Reasoning + Acting）

ReAct 是 Agent 的核心工作原理：

```
┌─────────────────────────────────────────────────────────┐
│                    ReAct 循环                           │
│                                                         │
│  Thought（思考）: 我现在需要做什么？                    │
│       ↓                                                 │
│  Action（行动）: 调用哪个工具？                         │
│       ↓                                                 │
│  Observation（观察）: 工具返回了什么？                  │
│       ↓                                                 │
│  Thought（再思考）: 接下来做什么？                      │
│       ↓                                                 │
│  ... 循环直到得出结论 ...                               │
│                                                         │
│  Final Answer（最终回答）                               │
└─────────────────────────────────────────────────────────┘
```

**实际例子**：
```
用户：贵州茅台现在的市盈率是多少？比去年怎么样？

Agent 思考过程：
Thought: 我需要获取茅台的当前 PE 和去年的 PE 数据
Action: stock_info_tool, args: {"symbol": "600519", "field": "pe_ratio"}
Observation: 当前 PE=30.5, 去年 PE=35.2

Thought: 我现在有了数据，可以进行比较
Final Answer: 贵州茅台当前市盈率为 30.5，相比去年的 35.2 下降了约 13%，
             估值有所回落，处于更合理的区间。
```

### 3. LangChain Agent 类型

```
LangChain Agent 体系
├── Zero-shot Agent（零样本 Agent）
│   └── 无需示例，直接根据工具描述决策
│
├── Few-shot Agent（少样本 Agent）
│   └── 提供示例，让 Agent 模仿
│
├── Structured Chat Agent
│   └── 使用结构化输出的 Agent
│
└── OpenAI Functions Agent
    └── 利用 OpenAI Function Calling 能力
```

### 4. 创建第一个 Agent

```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.tools import tool

# 1. 定义工具
@tool
def search(query: str) -> str:
    """搜索信息"""
    return f"搜索结果：关于{query}的信息"

tools = [search]

# 2. 创建 Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有帮助的助手"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),  # 存储思考过程
])

# 3. 初始化 LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 4. 创建 Agent
agent = create_tool_calling_agent(llm, tools, prompt)

# 5. 创建执行器
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # 打印思考过程
    handle_parsing_errors=True
)

# 6. 执行
result = agent_executor.invoke({"input": "搜索一下 Python 装饰器"})
print(result["output"])
```

### 5. 查看 Agent 思考过程

```python
# verbose=True 时可以看到完整的 ReAct 过程：
"""
> Entering new AgentExecutor chain...
Thought: 用户想要搜索 Python 装饰器的信息
Action: search
Action Input: {"query": "Python 装饰器"}
Observation: 搜索结果：关于 Python 装饰器的信息
Thought: 我现在有了搜索结果，可以回答用户了
Final Answer: 根据搜索结果，Python 装饰器是一种...
> Finished chain.
"""
```

---

## 实践任务

### 任务 1: 运行基础 Agent ✅

```python
# agent_basic.py

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.tools import tool

@tool
def calculator(expression: str) -> str:
    """计算数学表达式"""
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误：{e}"

tools = [calculator]

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个数学助手"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 测试
result = agent_executor.invoke({"input": "计算 123 * 456"})
print(result["output"])
```

### 任务 2: 多工具 Agent ✅

```python
# multi_tool_agent.py

@tool
def get_stock_price(symbol: str) -> str:
    """获取股票价格"""
    prices = {"AAPL": "175.5", "GOOGL": "140.2", "MSFT": "420.8"}
    return prices.get(symbol, "未知")

@tool
def get_pe_ratio(symbol: str) -> str:
    """获取市盈率"""
    pes = {"AAPL": "28.5", "GOOGL": "25.1", "MSFT": "35.2"}
    return pes.get(symbol, "未知")

# 创建有多个工具的 Agent 并测试
```

### 任务 3: 分析思考过程 ✅

运行 Agent 并记录 ReAct 循环：
- [ ] Thought 出现了几次？
- [ ] Action 调用了哪些工具？
- [ ] Observation 返回了什么？
- [ ] Final Answer 如何总结？

---

## 知识点总结

| 组件 | 作用 |
|------|------|
| Tool | Agent 可以使用的功能 |
| Prompt | 指导 Agent 如何思考 |
| Agent | 决策核心，选择工具 |
| AgentExecutor | 执行 ReAct 循环 |
| agent_scratchpad | 存储中间思考过程 |

### ReAct 模式关键点

1. **Thought**: 明确当前目标
2. **Action**: 选择合适的工具
3. **Observation**: 分析工具返回
4. **循环**: 直到问题解决了
5. **Final Answer**: 给出完整回答

---

## 常见问题

### Q1: Agent 和 Chain 有什么区别？

| Chain | Agent |
|-------|-------|
| 固定流程 | 动态决策 |
| 预先定义的步骤 | 根据情况选择工具 |
| 适合确定性任务 | 适合开放性任务 |

### Q2: Agent 为什么会进入死循环？
```python
# 原因：Agent 一直找不到合适的工具或无法得出结论

# 解决方法：
# 1. 设置 max_iterations
agent_executor = AgentExecutor(..., max_iterations=5)

# 2. 改进工具描述，让 Agent 更好理解

# 3. 优化 Prompt，给出更清晰的指导
```

### Q3: 如何选择合适的 Agent 类型？
- **Zero-shot**: 大多数场景，工具描述清晰时
- **Few-shot**: 需要 Agent 模仿特定行为时
- **Structured Chat**: 需要更稳定的输出格式时

---

## 代码文件

```
day36_agent_basic/
├── README.md                    # 本文件
├── agent_basic.py               # 基础 Agent
├── multi_tool_agent.py          # 多工具 Agent
├── react_analysis.md            # ReAct 过程分析
└── requirements.txt             # 依赖清单
```

---

## 参考资源

- [LangChain Agent 文档](https://python.langchain.com/docs/concepts/agents)
- [ReAct 论文](https://arxiv.org/abs/2210.03629)
- [LangChain Tools](https://python.langchain.com/docs/integrations/tools/)

---

## 下一步

- **Day 37**: 自定义 Tool（@tool 装饰器）
- **明日任务**: 学习如何为 Agent 添加工具

---

**💡 今日格言**: "Agent 让 LLM 从'纸上谈兵'变成'实战指挥'"
