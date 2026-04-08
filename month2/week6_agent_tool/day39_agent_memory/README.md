# Day 39: 记忆管理

> **日期**: 2026-05-11（周日）  
> **周次**: Week 6 - Agent + Tool 调用  
> **预计耗时**: 2 小时

---

## 今日学习目标

- [ ] 理解对话记忆的重要性
- [ ] 掌握 ConversationBufferMemory
- [ ] 了解 ConversationSummaryMemory
- [ ] 学会记忆长度控制

---

## 学习内容

### 1. 为什么需要记忆？

**无记忆的对话**：
```
用户：我叫小明，今年 25 岁
AI: 你好小明！

用户：我刚才说了什么？
AI: 抱歉，我不记得了...（因为没有记忆）
```

**有记忆的对话**：
```
用户：我叫小明，今年 25 岁
AI: 你好小明！

用户：我刚才说了什么？
AI: 你刚才说你叫小明，今年 25 岁
```

### 2. ConversationBufferMemory（缓冲记忆）

最简单的记忆类型，存储所有历史消息：

```python
from langchain.memory import ConversationBufferMemory
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 创建记忆
memory = ConversationBufferMemory(
    memory_key="chat_history",  # 必须与 prompt 中的 key 匹配
    return_messages=True,       # 返回消息对象而非字符串
    input_key="input",          # 输入变量名
    output_key="output"         # 输出变量名
)

# 创建带记忆的 Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有帮助的助手"),
    ("placeholder", "{chat_history}"),  # 插入历史消息
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent = create_tool_calling_agent(llm, [], prompt)
executor = AgentExecutor(
    agent=agent,
    tools=[],
    memory=memory,
    verbose=True
)

# 多轮对话
executor.invoke({"input": "我叫小明"})
executor.invoke({"input": "我叫什么名字？"})  # 能回答"小明"
```

### 3. ConversationSummaryMemory（摘要记忆）

当对话太长时，用摘要压缩历史：

```python
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")

memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history",
    return_messages=True
)

# 对话会被总结成简短的摘要
# 原始：用户说 A，AI 回复 B，用户说 C，AI 回复 D...
# 摘要：用户询问了 X 问题，AI 给出了 Y 建议
```

### 4. 带缓冲的摘要记忆（推荐）

结合两者优点：最近的对话用缓冲，久远的用摘要：

```python
from langchain.memory import ConversationSummaryBufferMemory

memory = ConversationSummaryBufferMemory(
    llm=llm,
    memory_key="chat_history",
    max_token_limit=2000,  # 超过这个长度就开始摘要
    return_messages=True
)

# 优点：
# - 最近的对话保持原样（精确）
# - 久远的对话被压缩（节省 token）
# - 不会丢失重要信息
```

### 5. 记忆持久化

将记忆保存到文件/数据库：

```python
from langchain.memory import ConversationBufferMemory
import json

memory = ConversationBufferMemory(return_messages=True)

# 保存
def save_memory(memory, filepath):
    history = memory.chat_memory
    messages = []
    for msg in history.messages:
        messages.append({
            "type": msg.type,
            "content": msg.content
        })
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

# 加载
def load_memory(memory, filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        messages = json.load(f)
    for msg in messages:
        if msg["type"] == "human":
            memory.chat_memory.add_user_message(msg["content"])
        else:
            memory.chat_memory.add_ai_message(msg["content"])
```

---

## 实践任务

### 任务 1: 基础记忆练习 ✅

```python
# agent_memory.py

from langchain.memory import ConversationBufferMemory
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的聊天助手"),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
agent = create_tool_calling_agent(llm, [], prompt)
executor = AgentExecutor(agent=agent, tools=[], memory=memory, verbose=True)

# 测试多轮对话
print(executor.invoke({"input": "我叫小明，喜欢打篮球"}))
print(executor.invoke({"input": "我喜欢什么运动？"}))
print(executor.invoke({"input": "我叫什么名字？"}))
```

### 任务 2: 摘要记忆对比 ✅

```python
# summary_memory.py

from langchain.memory import ConversationSummaryBufferMemory

# 比较 BufferMemory 和 SummaryBufferMemory
# 进行长对话后查看 token 使用量差异

# 1. 普通 Buffer（会消耗大量 token）
buffer_memory = ConversationBufferMemory(...)

# 2. 摘要缓冲（自动压缩）
summary_memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=500  # 超过 500 token 就开始摘要
)
```

### 任务 3: 股票分析对话助手 ✅

```python
# stock_chat_agent.py

# 创建一个带记忆的股票分析 Agent
# 支持以下对话：
# 用户：我想了解贵州茅台
# AI: 贵州茅台是白酒龙头企业...
# 用户：它的 PE 是多少？（能理解"它"指茅台）
# AI: 茅台的 PE 约为 30.5...
# 用户：那五粮液呢？（能理解在比较白酒股）
# AI: 五粮液的 PE 约为 25.3，比茅台低...
```

---

## 知识点总结

| 记忆类型 | 特点 | 适用场景 |
|----------|------|----------|
| BufferMemory | 存储全部历史 | 短对话 |
| SummaryMemory | 只保存摘要 | 长对话 |
| SummaryBufferMemory | 最近 + 摘要 | 推荐，通用场景 |
| ReadOnlyMemory | 只读不可写 | 预设上下文 |

### 记忆配置参数

```python
ConversationBufferMemory(
    memory_key="chat_history",     # 记忆在 prompt 中的变量名
    return_messages=True,          # 返回消息对象
    input_key="input",             # 输入变量名
    output_key="output",           # 输出变量名
    human_prefix="用户",            # 人类消息前缀
    ai_prefix="助手",              # AI 消息前缀
)
```

---

## 常见问题

### Q1: memory_key 不匹配怎么办？

```python
# 错误示例
memory = ConversationBufferMemory(memory_key="history")  # 设置了 history
prompt = ChatPromptTemplate.from_messages([
    ("placeholder", "{chat_history}"),  # 但 prompt 用 chat_history
])

# 正确做法
memory = ConversationBufferMemory(memory_key="chat_history")  # 保持一致
```

### Q2: 对话太长 token 超限？

```python
# 使用摘要缓冲记忆
memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=2000  # 限制最大 token 数
)
```

### Q3: 如何清空记忆？

```python
# 清空历史
memory.clear()

# 或者重新创建 memory 实例
memory = ConversationBufferMemory(...)
```

---

## 代码文件

```
day39_agent_memory/
├── README.md                    # 本文件
├── agent_memory.py              # 基础记忆练习
├── summary_memory.py            # 摘要记忆练习
├── stock_chat_agent.py          # 股票对话助手
└── memory_persistence.py        # 记忆持久化
```

---

## 参考资源

- [LangChain Memory 文档](https://python.langchain.com/docs/concepts/memory)
- [ConversationBufferMemory API](https://api.python.langchain.com/en/latest/memory/langchain.memory.buffer.ConversationBufferMemory.html)
- [Memory 类型对比](https://python.langchain.com/docs/integrations/memory/)

---

## 下一步

- **Day 40**: Week 6 复习/补进度
- **Day 41**: 综合项目 - 股票查询 Agent

---

**💡 今日格言**: "记忆让 AI 从'健忘症'变成'老朋友'"
