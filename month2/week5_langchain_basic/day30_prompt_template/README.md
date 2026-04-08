# Day 30: Prompt 模板

> **日期**: 2026-05-02（周五）  
> **周次**: Week 5 - LangChain 基础  
> **预计耗时**: 2 小时

---

## 今日学习目标

- [ ] 掌握 PromptTemplate 基础用法
- [ ] 学会变量替换技巧
- [ ] 理解 FewShot Prompting（少样本提示）
- [ ] 掌握 Prompt 设计技巧

---

## 学习内容

### 1. 为什么需要 Prompt 模板？

直接写 Prompt 的问题：
```python
# 每次都要手动拼接字符串
prompt = f"请分析{stock_name} ({stock_symbol}) 的股票情况，当前价格{price}元"
```

使用模板的优势：
```python
# 可复用、结构清晰、易于维护
template = "请分析{stock_name} ({stock_symbol}) 的股票情况，当前价格{price}元"
prompt = PromptTemplate(template=template, input_variables=["stock_name", "stock_symbol", "price"])
```

### 2. PromptTemplate 基础

```python
from langchain.prompts import PromptTemplate

# 方式 1: 简单模板
template = "请告诉我关于{topic}的{count}个要点"
prompt = PromptTemplate(
    template=template,
    input_variables=["topic", "count"]
)

# 格式化输出
formatted = prompt.format(topic="市盈率", count=3)
print(formatted)
# 输出：请告诉我关于市盈率的 3 个要点
```

### 3. 带指令的模板

```python
template = """
你是一位专业的股票分析师。请用简洁专业的语言回答以下问题。

问题：{question}

请从以下几个方面分析：
1. 基本概念
2. 计算方法
3. 实际应用

回答：
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["question"]
)
```

### 4. FewShot Prompting（少样本提示）

给模型提供示例，让它更好地理解任务：

```python
from langchain.prompts import FewShotPromptTemplate, PromptTemplate

# 定义示例
examples = [
    {
        "question": "什么是 PE？",
        "answer": "PE 是市盈率（Price-to-Earnings Ratio），计算公式为：股价/每股收益。用于评估股票估值水平。"
    },
    {
        "question": "什么是 PB？",
        "answer": "PB 是市净率（Price-to-Book Ratio），计算公式为：股价/每股净资产。用于评估股票相对于净资产的溢价。"
    },
]

# 示例模板
example_template = """
问题：{question}
回答：{answer}
"""

example_prompt = PromptTemplate(
    template=example_template,
    input_variables=["question", "answer"]
)

# FewShot 主模板
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="你是一位股票分析师助手。请根据示例的风格回答问题。",
    suffix="问题：{new_question}\n回答：",
    input_variables=["new_question"],
    example_separator="\n\n"
)

# 生成最终 Prompt
final_prompt = few_shot_prompt.format(new_question="什么是 ROE？")
print(final_prompt)
```

### 5. Prompt 设计技巧

#### 技巧 1: 明确角色
```python
template = """你是一位拥有 10 年经验的股票分析师，擅长用通俗易懂的语言解释复杂的金融概念。"""
```

#### 技巧 2: 提供上下文
```python
template = """
背景：用户正在学习股票基础知识，是初学者水平。
任务：解释以下概念，避免使用过多专业术语。
概念：{concept}
"""
```

#### 技巧 3: 指定输出格式
```python
template = """
请用以下格式回答：
【定义】一句话定义
【公式】计算公式（如有）
【示例】一个实际例子
【应用】如何在实际中使用

概念：{concept}
"""
```

#### 技巧 4: 逐步思考（Chain of Thought）
```python
template = """
请一步步思考：
1. 首先分析问题的核心
2. 然后列出关键要点
3. 最后给出完整答案

问题：{question}
"""
```

---

## 实践任务

### 任务 1: 创建股票分析 Prompt 模板 ✅

```python
# prompt_template.py

from langchain.prompts import PromptTemplate

# 创建一个股票分析模板
stock_template = PromptTemplate(
    template="""你是一位专业的股票分析师。

股票名称：{stock_name}
股票代码：{stock_code}
当前价格：{price}

请分析这只股票的当前状况，包括：
1. 估值水平（高/中/低）
2. 投资建议（买入/持有/卖出）
3. 风险提示

分析：""",
    input_variables=["stock_name", "stock_code", "price"]
)

# 测试
print(stock_template.format(
    stock_name="贵州茅台",
    stock_code="600519",
    price=1800
))
```

### 任务 2: FewShot 股票问答 ✅

```python
# few_shot_stock.py

examples = [
    {"question": "茅台市盈率 30 倍算高吗？", "answer": "对于贵州茅台这样的消费龙头，30 倍 PE 处于合理区间。历史平均 PE 约 35 倍，目前估值略低于平均水平。"},
    {"question": "银行股 PB 0.5 倍意味着什么？", "answer": "PB 0.5 倍表示股价只有净资产的一半，说明市场对银行资产质量有担忧，或者认为其盈利能力不足。"},
]

# 创建 FewShot 模板并测试
```

### 任务 3: 优化你的 Prompt ✅

尝试以下优化：
- [ ] 添加角色设定
- [ ] 指定输出格式
- [ ] 添加示例
- [ ] 添加思考步骤

---

## 知识点总结

| 组件 | 作用 | 使用场景 |
|------|------|----------|
| PromptTemplate | 基础模板 | 简单的变量替换 |
| FewShotPromptTemplate | 带示例的模板 | 需要模型模仿特定风格 |
| input_variables | 定义输入变量 | 声明模板需要的参数 |
| template | 模板字符串 | 定义 Prompt 结构 |

### Prompt 设计 Checklist

- [ ] 角色设定清晰
- [ ] 任务描述明确
- [ ] 提供必要上下文
- [ ] 指定输出格式
- [ ] 添加示例（如需）
- [ ] 限制输出长度

---

## 常见问题

### Q1: 如何处理中文变量？
```python
# 支持中文变量名
template = "分析{股票名称}的{指标}"
prompt = PromptTemplate(template=template, input_variables=["股票名称", "指标"])
```

### Q2: FewShot 示例多少合适？
- 简单任务：1-3 个示例
- 复杂任务：3-5 个示例
- 太多会消耗 token 且可能让模型困惑

### Q3: 如何调试 Prompt？
```python
# 打印格式化后的完整 Prompt
formatted = prompt.format(...)
print("=" * 50)
print(formatted)
print("=" * 50)
```

---

## 代码文件

```
day30_prompt_template/
├── README.md                    # 本文件
├── prompt_template.py           # PromptTemplate 练习
├── few_shot_prompt.py           # FewShot 练习
├── stock_prompts.py             # 股票场景 Prompt 集
└── requirements.txt             # 依赖清单
```

---

## 参考资源

- [LangChain Prompt 文档](https://python.langchain.com/docs/concepts/prompt_templates)
- [FewShot Prompting 论文](https://arxiv.org/abs/2002.08387)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

---

## 下一步

- **Day 31**: Chain（顺序链、转换链）
- **明日任务**: 学习如何将多个 Prompt 串联成完整流程

---

**💡 今日格言**: "好的 Prompt 设计 = 清晰的指令 + 合适的示例 + 明确的格式"
