# Day 31: Chain 链式调用

> **日期**: 2026-05-03（周六）  
> **周次**: Week 5 - LangChain 基础  
> **预计耗时**: 2 小时

---

## 今日学习目标

- [ ] 理解 Chain 的概念和作用
- [ ] 掌握 SequentialChain 顺序链
- [ ] 了解 TransformChain 数据转换
- [ ] 学会自定义 Chain

---

## 学习内容

### 1. 为什么需要 Chain？

单一 LLM 调用的局限：
```python
# 一次调用只能完成一个任务
response = llm.invoke("分析茅台股票")
```

Chain 的优势：
```python
# 将多个步骤串联起来，形成完整工作流
chain = step1 | step2 | step3
result = chain.invoke({"input": "茅台股票"})
```

### 2. Chain 基础概念

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Step 1    │ -> │   Step 2    │ -> │   Step 3    │
│  获取数据   │    │  分析数据   │    │  生成报告   │
└─────────────┘    └─────────────┘    └─────────────┘
       ↓                  ↓                  ↓
   输入：股票代码      输入：原始数据      输入：分析结果
   输出：原始数据      输出：分析结果      输出：最终报告
```

### 3. SequentialChain（顺序链）

按顺序执行多个 Chain，前一个输出作为后一个输入：

```python
from langchain.chains import SequentialChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# 步骤 1: 获取股票基本信息
prompt1 = PromptTemplate(
    template="请列出{stock_name}的基本信息，包括股票代码、所属行业、主营业务。",
    input_variables=["stock_name"]
)
chain1 = LLMChain(llm=llm, prompt=prompt1, output_key="basic_info")

# 步骤 2: 分析竞争优势
prompt2 = PromptTemplate(
    template="基于以下信息，分析{stock_name}的竞争优势：\n{basic_info}",
    input_variables=["stock_name", "basic_info"]
)
chain2 = LLMChain(llm=llm, prompt=prompt2, output_key="competitive_advantage")

# 步骤 3: 生成投资建议
prompt3 = PromptTemplate(
    template="基于以下分析，给出投资建议：\n基本信息：{basic_info}\n竞争优势：{competitive_advantage}",
    input_variables=["basic_info", "competitive_advantage"]
)
chain3 = LLMChain(llm=llm, prompt=prompt3, output_key="investment_advice")

# 串联所有步骤
overall_chain = SequentialChain(
    chains=[chain1, chain2, chain3],
    input_variables=["stock_name"],
    output_variables=["basic_info", "competitive_advantage", "investment_advice"],
    verbose=True
)

# 执行
result = overall_chain.invoke({"stock_name": "贵州茅台"})
print(result["investment_advice"])
```

### 4. TransformChain（转换链）

对数据进行自定义转换处理：

```python
from langchain.chains import TransformChain
import json

def transform_func(inputs: dict) -> dict:
    """自定义转换逻辑"""
    stock_data = inputs["raw_data"]
    
    # 解析并处理数据
    data = json.loads(stock_data)
    formatted = f"股票：{data['name']}, 价格：{data['price']}, 涨幅：{data['change']}%"
    
    return {"formatted_data": formatted}

transform_chain = TransformChain(
    input_variables=["raw_data"],
    output_variables=["formatted_data"],
    transform=transform_func
)
```

### 5. LCEL（LangChain Expression Language）

LangChain 新版推荐的链式语法：

```python
from langchain_core.output_parsers import StrOutputParser

# 使用 | 操作符串联
chain = prompt | llm | StrOutputParser()

# 执行
result = chain.invoke({"stock_name": "贵州茅台"})
```

### 6. 并行链（Parallel Chain）

同时执行多个独立任务：

```python
from langchain.schema.runnable import RunnableParallel

# 并行获取多个信息
parallel_chain = RunnableParallel(
    basic_info=chain1,
    technical=chain2,
    fundamental=chain3
)

result = parallel_chain.invoke({"stock_name": "茅台"})
# result = {
#     "basic_info": "...",
#     "technical": "...",
#     "fundamental": "..."
# }
```

---

## 实践任务

### 任务 1: SequentialChain 练习 ✅

```python
# sequential_chain.py

from langchain.chains import SequentialChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# 创建一个 3 步股票分析链
# 步骤 1: 解释概念
# 步骤 2: 给出计算方法
# 步骤 3: 提供实际案例

chain1 = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        template="请解释股票术语：{term}",
        input_variables=["term"]
    ),
    output_key="definition"
)

chain2 = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        template="请说明{term}的计算方法：\n{definition}",
        input_variables=["term", "definition"]
    ),
    output_key="formula"
)

chain3 = LLMChain(
    llm=llm,
    prompt=PromptTemplate(
        template="请给出{term}的实际应用案例：\n{formula}",
        input_variables=["term", "formula"]
    ),
    output_key="example"
)

# 串联
overall = SequentialChain(
    chains=[chain1, chain2, chain3],
    input_variables=["term"],
    output_variables=["definition", "formula", "example"],
    verbose=True
)

# 测试
result = overall.invoke({"term": "市盈率"})
print(result)
```

### 任务 2: LCEL 风格链 ✅

```python
# lcel_chain.py

from langchain_core.output_parsers import StrOutputParser

# 使用 LCEL 语法
prompt = PromptTemplate(
    template="分析{stock}股票的投资价值，从以下几个方面：1.行业地位 2.财务状况 3.估值水平",
    input_variables=["stock"]
)

chain = prompt | llm | StrOutputParser()
result = chain.invoke({"stock": "宁德时代"})
print(result)
```

### 任务 3: 自定义股票分析链 ✅

创建一个完整的股票分析 Chain：
- [ ] 输入：股票代码
- [ ] 步骤 1: 获取基本信息
- [ ] 步骤 2: 财务分析
- [ ] 步骤 3: 技术面分析
- [ ] 步骤 4: 生成报告
- [ ] 输出：完整分析报告

---

## 知识点总结

| Chain 类型 | 作用 | 适用场景 |
|------------|------|----------|
| LLMChain | 基础 LLM 调用 | 单一 Prompt 调用 |
| SequentialChain | 顺序执行 | 多步骤任务流 |
| TransformChain | 数据转换 | 自定义处理逻辑 |
| RunnableParallel | 并行执行 | 独立多任务 |

### LCEL 语法优势

```python
# 传统方式
chain = SequentialChain(chains=[a, b, c], ...)

# LCEL 方式（推荐）
chain = a | b | c
```

---

## 常见问题

### Q1: SequentialChain 和 LCEL 选哪个？
- **SequentialChain**: 旧版 API，功能更丰富
- **LCEL**: 新版推荐，语法更简洁
- 建议：新项目用 LCEL

### Q2: 如何传递多个输出？
```python
# output_key 指定输出键名
chain = LLMChain(..., output_key="result")

# SequentialChain 中自动合并
overall_chain.output_variables = ["key1", "key2", "key3"]
```

### Q3: 如何调试 Chain？
```python
# verbose=True 打印每步详情
chain = SequentialChain(..., verbose=True)

# 查看中间结果
result = chain.invoke(...)
print(result)  # 包含所有 output_variables
```

---

## 代码文件

```
day31_chain/
├── README.md                    # 本文件
├── sequential_chain.py          # SequentialChain 练习
├── lcel_chain.py                # LCEL 风格练习
├── transform_chain.py           # TransformChain 练习
└── stock_analysis_chain.py      # 股票分析完整 Chain
```

---

## 参考资源

- [LangChain Chains 文档](https://python.langchain.com/docs/concepts/chains)
- [LCEL 表达式语言](https://python.langchain.com/docs/concepts/lcel)
- [SequentialChain API](https://api.python.langchain.com/en/latest/chains/langchain.chains.sequential.SequentialChain.html)

---

## 下一步

- **Day 32**: OutputParser（输出解析器）
- **明日任务**: 学习如何解析和结构化 LLM 输出

---

**💡 今日格言**: "Chain 让 AI 思考更有条理"
