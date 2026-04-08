# Day 34: 综合项目 - 股票分析助手（基础版）

> **日期**: 2026-05-06（周二）  
> **周次**: Week 5 - LangChain 基础  
> **预计耗时**: 6 小时

---

## 项目目标

创建一个基于 LangChain 的股票分析助手，能够：

- [ ] 回答股票基本概念问题
- [ ] 分析指定股票的基本信息
- [ ] 提供简单的投资建议
- [ ] 支持多轮对话

---

## 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                   股票分析助手架构                       │
├─────────────────────────────────────────────────────────┤
│  用户界面 (CLI)                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │  用户：分析贵州茅台                               │   │
│  │  助手：贵州茅台 (600519) 是白酒行业龙头企业...   │   │
│  └──────────────────────────────────────────────────┘   │
│                          ↑↓                              │
├─────────────────────────────────────────────────────────┤
│  LangChain 核心层                                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Prompt    │ → │    LLM      │ → │   Parser    │     │
│  │   Template  │   │  (DeepSeek) │   │  (结构化)   │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                          ↑↓                              │
├─────────────────────────────────────────────────────────┤
│  工具层 (可选)                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  股票查询   │  │  财务数据   │  │  新闻检索   │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

---

## 项目结构

```
day34_stock_assistant/
├── README.md                      # 本文件
├── stock_assistant_basic.py       # 主程序
├── prompts/
│   ├── stock_analysis.py          # 股票分析 Prompt
│   └── stock_qa.py                # 股票问答 Prompt
├── chains/
│   ├── analysis_chain.py          # 分析 Chain
│   └── qa_chain.py                # 问答 Chain
├── parsers/
│   └── stock_parser.py            # 输出解析器
├── utils/
│   └── stock_data.py              # 股票数据模拟
└── requirements.txt               # 依赖清单
```

---

## 实现步骤

### Step 1: 环境准备

```bash
# 安装依赖
pip install langchain langchain-openai pydantic

# 配置 API Key
export OPENAI_API_KEY="sk-xxx"
# 或使用 DeepSeek
export OPENAI_API_KEY="sk-xxx"
export OPENAI_BASE_URL="https://api.deepseek.com"
```

### Step 2: 定义数据结构

```python
# parsers/stock_parser.py

from pydantic import BaseModel, Field

class StockAnalysis(BaseModel):
    """股票分析报告"""
    stock_name: str = Field(description="股票名称")
    stock_code: str = Field(description="股票代码")
    industry: str = Field(description="所属行业")
    summary: str = Field(description="一句话总结")
    strengths: list[str] = Field(description="优势列表")
    risks: list[str] = Field(description="风险列表")
    recommendation: str = Field(description="投资建议", enum=["买入", "持有", "卖出"])
    confidence: float = Field(description="置信度", ge=0, le=1)
```

### Step 3: 创建 Prompt 模板

```python
# prompts/stock_analysis.py

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from parsers.stock_parser import StockAnalysis

def create_stock_analysis_prompt():
    parser = PydanticOutputParser(pydantic_object=StockAnalysis)
    
    template = """你是一位专业的股票分析师。请分析以下股票。

股票名称：{stock_name}
股票代码：{stock_code}

请从以下几个方面进行分析：
1. 公司基本面（行业地位、主营业务）
2. 财务状况（营收、利润、负债）
3. 估值水平（PE、PB 等）
4. 风险提示

{format_instructions}

请用专业但易懂的语言回答。"""

    return PromptTemplate(
        template=template,
        input_variables=["stock_name", "stock_code"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    ), parser
```

### Step 4: 创建分析 Chain

```python
# chains/analysis_chain.py

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from prompts.stock_analysis import create_stock_analysis_prompt

def create_analysis_chain():
    llm = ChatOpenAI(
        model="deepseek-chat",
        base_url="https://api.deepseek.com",
        temperature=0.3
    )
    
    prompt, parser = create_stock_analysis_prompt()
    
    chain = prompt | llm | parser
    
    return chain
```

### Step 5: 主程序

```python
# stock_assistant_basic.py

from chains.analysis_chain import create_analysis_chain

def main():
    print("=" * 60)
    print("📈 股票分析助手（基础版）")
    print("=" * 60)
    
    chain = create_analysis_chain()
    
    while True:
        print("\n请输入股票信息（输入 q 退出）：")
        stock_name = input("股票名称：").strip()
        
        if stock_name.lower() == 'q':
            break
            
        stock_code = input("股票代码：").strip()
        
        print("\n正在分析中...")
        try:
            result = chain.invoke({
                "stock_name": stock_name,
                "stock_code": stock_code
            })
            
            print("\n" + "=" * 60)
            print(f"📊 {result.stock_name} ({result.stock_code}) 分析报告")
            print("=" * 60)
            print(f"🏭 所属行业：{result.industry}")
            print(f"📝 总结：{result.summary}")
            print(f"\n💪 优势:")
            for s in result.strengths:
                print(f"  - {s}")
            print(f"\n⚠️  风险:")
            for r in result.risks:
                print(f"  - {r}")
            print(f"\n💡 投资建议：{result.recommendation}")
            print(f"📊 置信度：{result.confidence:.0%}")
            print("=" * 60)
        except Exception as e:
            print(f"分析失败：{e}")

if __name__ == "__main__":
    main()
```

---

## 功能扩展

### 扩展 1: 添加股票数据查询

```python
# utils/stock_data.py

# 模拟股票数据（实际项目中可接入 API）
STOCK_DATA = {
    "600519": {"name": "贵州茅台", "price": 1800.0, "pe": 30.5, "industry": "白酒"},
    "000858": {"name": "五粮液", "price": 150.0, "pe": 25.3, "industry": "白酒"},
    "300750": {"name": "宁德时代", "price": 180.0, "pe": 20.1, "industry": "新能源"},
}

def get_stock_info(code: str) -> dict:
    return STOCK_DATA.get(code, {})
```

### 扩展 2: 添加问答功能

```python
# chains/qa_chain.py

from langchain.chains import create_history_aware_retriever

def create_qa_chain():
    # 创建一个简单的问答 Chain
    template = """你是一位股票知识助手。请回答用户的问题。

问题：{question}

请用专业但易懂的语言回答。"""
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["question"]
    )
    
    llm = ChatOpenAI(model="deepseek-chat", temperature=0.7)
    
    return prompt | llm | StrOutputParser()
```

### 扩展 3: 添加对话历史

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 在 Chain 中使用
chain = create_chain()
chain_with_memory = add_memory(chain, memory)
```

---

## 运行测试

```bash
# 进入项目目录
cd day34_stock_assistant

# 运行主程序
python stock_assistant_basic.py

# 示例交互
# 股票名称：贵州茅台
# 股票代码：600519
# 正在分析中...
# ===============分析报告===============
# 贵州茅台 (600519) 是白酒行业龙头企业...
```

---

## 项目检查清单

- [ ] 环境配置完成
- [ ] 数据结构定义清晰
- [ ] Prompt 模板设计合理
- [ ] Chain 能够正常运行
- [ ] 输出格式正确解析
- [ ] 用户交互流畅
- [ ] 错误处理完善

---

## 常见问题

### Q1: API 调用失败？
```bash
# 检查 API Key 配置
echo $OPENAI_API_KEY

# 检查网络连接
curl https://api.deepseek.com

# 检查依赖
pip list | grep langchain
```

### Q2: 输出解析失败？
```python
# 1. 检查 format_instructions 是否在 Prompt 中
# 2. 降低 temperature 让输出更稳定
# 3. 使用 OutputFixingParser 包装
```

### Q3: 如何接入真实股票数据？
```python
# 可以使用以下 API：
# - 新浪财经 API（免费）
# - 聚宽数据（有免费额度）
# - Alpha Vantage（免费）
# - Yahoo Finance
```

---

## 参考资源

- [LangChain 官方示例](https://github.com/langchain-ai/langchain)
- [DeepSeek API 文档](https://platform.deepseek.com/)
- [Pydantic 最佳实践](https://docs.pydantic.dev/latest/usage/model_config/)

---

## 下一步

- **Week 6**: Agent + Tool 调用
- **Day 36**: Agent 基础（ReAct 模式）

---

**🎉 恭喜完成 Week 5！你已掌握 LangChain 基础组件！**
