# Day 32: OutputParser 输出解析器

> **日期**: 2026-05-04（周日）  
> **周次**: Week 5 - LangChain 基础  
> **预计耗时**: 2 小时

---

## 今日学习目标

- [ ] 理解 OutputParser 的作用
- [ ] 掌握 PydanticOutputParser
- [ ] 学会 CommaSeparatedListOutputParser
- [ ] 能够自定义解析器

---

## 学习内容

### 1. 为什么需要 OutputParser？

LLM 原始输出的问题：
```python
# 直接输出，格式不固定
response = llm.invoke("列出 5 个科技股")
print(response.content)
# 输出：1. 苹果 2. 微软 3. 谷歌... （纯文本，难以程序化处理）
```

使用 OutputParser：
```python
# 结构化输出，可直接用于代码
response = chain.invoke({"query": "列出 5 个科技股"})
print(response)
# 输出：["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
```

### 2. StrOutputParser（最基础）

```python
from langchain_core.output_parsers import StrOutputParser

chain = prompt | llm | StrOutputParser()
result = chain.invoke({"input": "你好"})
# 直接返回字符串
```

### 3. CommaSeparatedListOutputParser（列表解析）

```python
from langchain_core.output_parsers import CommaSeparatedListOutputParser

# 创建解析器
output_parser = CommaSeparatedListOutputParser()

# 获取格式说明
format_instructions = output_parser.get_format_instructions()
# 输出：Your response should be a list of comma separated values...

# 在 Prompt 中使用
prompt = PromptTemplate(
    template="列出{topic}相关的 5 个关键词。\n{format_instructions}",
    input_variables=["topic"],
    partial_variables={"format_instructions": format_instructions}
)

chain = prompt | llm | output_parser
result = chain.invoke({"topic": "股票投资"})
print(result)
# 输出：["价值投资", "技术分析", "分散风险", "长期持有", "止损"]
```

### 4. PydanticOutputParser（结构化输出）⭐重点

```python
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# 1. 定义输出结构
class StockAnalysis(BaseModel):
    stock_name: str = Field(description="股票名称")
    current_price: float = Field(description="当前价格")
    pe_ratio: float = Field(description="市盈率")
    recommendation: str = Field(description="投资建议", enum=["买入", "持有", "卖出"])
    reason: str = Field(description="理由")

# 2. 创建解析器
parser = PydanticOutputParser(pydantic_object=StockAnalysis)

# 3. 获取格式说明
format_instructions = parser.get_format_instructions()

# 4. 在 Prompt 中使用
prompt = PromptTemplate(
    template="""分析{stock_code}股票。
    {format_instructions}
    """,
    input_variables=["stock_code"],
    partial_variables={"format_instructions": format_instructions}
)

# 5. 创建链
chain = prompt | llm | parser

# 6. 执行并获取结构化结果
result = chain.invoke({"stock_code": "600519"})
print(result.stock_name)      # 访问属性
print(result.recommendation)  # 贵州茅台
```

### 5. JsonOutputParser（JSON 输出）

```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

prompt = PromptTemplate(
    template="""返回以下股票的 JSON 数据：
    股票：{stock}
    {format_instructions}
    """,
    input_variables=["stock"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

chain = prompt | llm | parser
result = chain.invoke({"stock": "茅台"})
# 输出：{"name": "贵州茅台", "code": "600519", "price": 1800.0}
```

### 6. 处理解析错误

```python
from langchain_core.output_parsers import OutputFixingParser

# 包装一个"修复"解析器
normal_parser = PydanticOutputParser(pydantic_object=StockAnalysis)
fixing_parser = OutputFixingParser.from_llm(
    parser=normal_parser,
    llm=llm  # 用 LLM 尝试修复格式错误的输出
)

chain = prompt | llm | fixing_parser
# 即使 LLM 输出格式稍有偏差，也能尝试修复并解析
```

---

## 实践任务

### 任务 1: 列表解析练习 ✅

```python
# list_parser.py

from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
output_parser = CommaSeparatedListOutputParser()

prompt = PromptTemplate(
    template="列出 5 个适合新手入手的蓝筹股（只写股票名称，用逗号分隔）。\n{format_instructions}",
    input_variables=[],
    partial_variables={"format_instructions": output_parser.get_format_instructions()}
)

chain = prompt | llm | output_parser
result = chain.invoke({})
print(result)
```

### 任务 2: Pydantic 结构化输出 ✅

```python
# pydantic_parser.py

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class StockInfo(BaseModel):
    name: str = Field(description="股票全称")
    code: str = Field(description="股票代码")
    industry: str = Field(description="所属行业")
    pe_ratio: float = Field(description="市盈率")
    market_cap: str = Field(description="市值")

parser = PydanticOutputParser(pydantic_object=StockInfo)

# 创建 Chain 并测试
```

### 任务 3: 股票分析报告 ✅

创建一个完整的股票分析输出结构：

```python
# stock_report_parser.py

class AnalysisReport(BaseModel):
    stock_name: str
    summary: str  # 一句话总结
    strengths: list[str]  # 优势列表
    risks: list[str]  # 风险列表
    target_price: float
    recommendation: str
    confidence: float  # 置信度 0-1

# 实现完整的分析报告 Chain
```

---

## 知识点总结

| 解析器 | 输出类型 | 适用场景 |
|--------|----------|----------|
| StrOutputParser | 字符串 | 简单文本输出 |
| CommaSeparatedListOutputParser | 列表 | 枚举项目 |
| PydanticOutputParser | Pydantic 对象 | 结构化数据 |
| JsonOutputParser | JSON/字典 | 通用结构化 |
| OutputFixingParser | 包装型 | 容错处理 |

### Pydantic 字段定义技巧

```python
from pydantic import BaseModel, Field

class Example(BaseModel):
    # 必填字段
    name: str = Field(description="描述")
    
    # 带默认值
    status: str = Field(default="active", description="状态")
    
    # 带约束
    price: float = Field(ge=0, description="价格")  # ge=大于等于
    
    # 枚举值
    level: str = Field(enum=["高", "中", "低"])
    
    # 列表字段
    tags: list[str] = Field(default_factory=list)
```

---

## 常见问题

### Q1: PydanticOutputParser 解析失败怎么办？

```python
# 1. 检查 Prompt 中是否包含 format_instructions
prompt = PromptTemplate(
    template="...{format_instructions}...",  # 必须有！
    ...
)

# 2. 使用 OutputFixingParser 包装
fixing_parser = OutputFixingParser.from_llm(parser, llm)

# 3. 降低 temperature 让输出更稳定
llm = ChatOpenAI(temperature=0.3)
```

### Q2: 如何输出中文 JSON？
```python
# Pydantic 对象转中文 JSON
from pydantic import BaseModel

class Stock(BaseModel):
    name: str
    price: float

result = Stock(name="茅台", price=1800.0)
print(result.model_dump())  # Python 字典
print(result.model_dump_json())  # JSON 字符串
```

### Q3: 如何处理嵌套结构？
```python
class Company(BaseModel):
    name: str
    ceo: str

class StockReport(BaseModel):
    company: Company  # 嵌套结构
    analysis: str

# PydanticOutputParser 支持嵌套
```

---

## 代码文件

```
day32_output_parser/
├── README.md                    # 本文件
├── list_parser.py               # 列表解析练习
├── pydantic_parser.py           # Pydantic 解析练习
├── json_parser.py               # JSON 解析练习
├── stock_report_parser.py       # 股票报告解析
└── fixing_parser.py             # 容错解析练习
```

---

## 参考资源

- [OutputParsers 文档](https://python.langchain.com/docs/concepts/output_parsers)
- [Pydantic 文档](https://docs.pydantic.dev/)
- [LangChain PydanticParser](https://python.langchain.com/docs/how_to/output_parser_structured/)

---

## 下一步

- **Day 33**: Week 5 复习/补进度
- **Day 34**: 综合项目 - 股票分析助手（基础版）

---

**💡 今日格言**: "结构化输出是让 AI 可用的关键一步"
