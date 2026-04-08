"""
Day 32: OutputParser 输出解析器

学习目标:
- 理解 OutputParser 的作用
- 掌握 PydanticOutputParser
- 学会 CommaSeparatedListOutputParser
- 能够自定义解析器
"""

from langchain_core.output_parsers import (
    StrOutputParser,
    CommaSeparatedListOutputParser,
    PydanticOutputParser,
    JsonOutputParser,
    OutputFixingParser
)
from langchain.prompts import PromptTemplate
from config import create_llm
from pydantic import BaseModel, Field
from typing import List


def str_output_parser():
    """StrOutputParser 基础示例"""
    print("=" * 50)
    print("StrOutputParser 基础示例")
    print("=" * 50)

    llm = create_llm(temperature=0.7)

    prompt = PromptTemplate(
        template="用一句话解释{concept}",
        input_variables=["concept"]
    )

    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"concept": "市盈率"})

    print(f"\n问题：用一句话解释市盈率")
    print(f"回答：{result}")


def list_output_parser():
    """CommaSeparatedListOutputParser 列表解析"""
    print("\n" + "=" * 50)
    print("CommaSeparatedListOutputParser 列表示例")
    print("=" * 50)

    output_parser = CommaSeparatedListOutputParser()

    prompt = PromptTemplate(
        template="列出 5 个适合新手入手的蓝筹股（只写股票名称，用逗号分隔）。\n{format_instructions}",
        input_variables=[],
        partial_variables={"format_instructions": output_parser.get_format_instructions()}
    )

    llm = create_llm(temperature=0.7)

    chain = prompt | llm | output_parser
    result = chain.invoke({})

    print(f"\n5 个蓝筹股：{result}")
    print(f"类型：{type(result)}")


def pydantic_output_parser():
    """PydanticOutputParser 结构化输出"""
    print("\n" + "=" * 50)
    print("PydanticOutputParser 结构化输出")
    print("=" * 50)

    # 1. 定义输出结构
    class StockInfo(BaseModel):
        name: str = Field(description="股票全称")
        code: str = Field(description="股票代码")
        industry: str = Field(description="所属行业")
        pe_ratio: float = Field(description="市盈率")
        market_cap: str = Field(description="市值")

    # 2. 创建解析器
    parser = PydanticOutputParser(pydantic_object=StockInfo)

    # 3. 获取格式说明
    format_instructions = parser.get_format_instructions()

    # 4. 在 Prompt 中使用
    prompt = PromptTemplate(
        template="""分析{stock_code}股票，返回结构化信息。
{format_instructions}
""",
        input_variables=["stock_code"],
        partial_variables={"format_instructions": format_instructions}
    )

    llm = create_llm(temperature=0.3)

    # 5. 创建链
    chain = prompt | llm | parser

    # 6. 执行并获取结构化结果
    result = chain.invoke({"stock_code": "贵州茅台"})

    print(f"\n结构化股票信息:")
    print(f"  名称：{result.name}")
    print(f"  代码：{result.code}")
    print(f"  行业：{result.industry}")
    print(f"  PE: {result.pe_ratio}")
    print(f"  市值：{result.market_cap}")


def json_output_parser():
    """JsonOutputParser JSON 输出"""
    print("\n" + "=" * 50)
    print("JsonOutputParser JSON 输出")
    print("=" * 50)

    parser = JsonOutputParser()

    prompt = PromptTemplate(
        template="""返回以下股票的 JSON 数据：
股票：{stock}
{format_instructions}
只返回 JSON，不要其他内容。
""",
        input_variables=["stock"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    llm = create_llm(temperature=0.3)

    chain = prompt | llm | parser
    result = chain.invoke({"stock": "贵州茅台"})

    print(f"\nJSON 结果:")
    print(result)
    print(f"\n类型：{type(result)}")


def stock_analysis_report():
    """股票分析报告完整示例"""
    print("\n" + "=" * 50)
    print("股票分析报告完整示例")
    print("=" * 50)

    # 定义复杂的输出结构
    class AnalysisReport(BaseModel):
        stock_name: str = Field(description="股票名称")
        summary: str = Field(description="一句话总结")
        strengths: List[str] = Field(description="优势列表")
        risks: List[str] = Field(description="风险列表")
        target_price: float = Field(description="目标价格")
        recommendation: str = Field(description="投资建议", enum=["买入", "持有", "卖出"])
        confidence: float = Field(description="置信度 0-1", ge=0, le=1)

    parser = PydanticOutputParser(pydantic_object=AnalysisReport)

    prompt = PromptTemplate(
        template="""你是一位专业的股票分析师。请分析{stock_name} ({stock_code})。

当前价格：{price}

请从以下几个方面进行分析：
1. 公司基本面（行业地位、主营业务）
2. 财务状况（营收、利润、负债）
3. 估值水平（PE、PB 等）
4. 风险提示

{format_instructions}

请用专业但易懂的语言回答。""",
        input_variables=["stock_name", "stock_code", "price"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    llm = create_llm(temperature=0.3)

    chain = prompt | llm | parser
    result = chain.invoke({
        "stock_name": "贵州茅台",
        "stock_code": "600519",
        "price": 1800.0
    })

    print(f"\n{'='*50}")
    print(f"{result.stock_name} 分析报告")
    print(f"{'='*50}")
    print(f"📝 总结：{result.summary}")
    print(f"\n💪 优势:")
    for s in result.strengths:
        print(f"  - {s}")
    print(f"\n⚠️  风险:")
    for r in result.risks:
        print(f"  - {r}")
    print(f"\n💡 投资建议：{result.recommendation}")
    print(f"📊 置信度：{result.confidence:.0%}")
    print(f"🎯 目标价格：{result.target_price} 元")


def output_fixing_parser():
    """OutputFixingParser 容错解析"""
    print("\n" + "=" * 50)
    print("OutputFixingParser 容错解析示例")
    print("=" * 50)

    class SimpleStock(BaseModel):
        name: str
        price: float

    normal_parser = PydanticOutputParser(pydantic_object=SimpleStock)

    llm = create_llm(temperature=0.3)

    # 使用 OutputFixingParser 包装
    fixing_parser = OutputFixingParser.from_llm(
        parser=normal_parser,
        llm=llm
    )

    prompt = PromptTemplate(
        template="""返回股票信息：{format_instructions}""",
        input_variables=[],
        partial_variables={"format_instructions": fixing_parser.get_format_instructions()}
    )

    chain = prompt | llm | fixing_parser
    result = chain.invoke({})

    print(f"解析结果：name={result.name}, price={result.price}")


def main():
    """主函数"""
    str_output_parser()
    list_output_parser()
    pydantic_output_parser()
    json_output_parser()
    stock_analysis_report()
    # output_fixing_parser()  # 可选：容错解析示例

    print("\n" + "=" * 50)
    print("✅ Day 32 学习完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
