"""
Day 34: 综合项目 - 股票分析助手（基础版）

项目目标:
- 创建一个基于 LangChain 的股票分析助手
- 能够回答股票基本概念问题
- 分析指定股票的基本信息
- 提供简单的投资建议
"""

from langchain_core.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from config import create_llm
from pydantic import BaseModel, Field
from typing import List


# ==================== 数据结构定义 ====================

class StockAnalysis(BaseModel):
    """股票分析报告"""
    stock_name: str = Field(description="股票名称")
    stock_code: str = Field(description="股票代码")
    industry: str = Field(description="所属行业")
    summary: str = Field(description="一句话总结")
    strengths: List[str] = Field(description="优势列表")
    risks: List[str] = Field(description="风险列表")
    recommendation: str = Field(description="投资建议", enum=["买入", "持有", "卖出"])
    confidence: float = Field(description="置信度", ge=0, le=1)


# ==================== Prompt 配置 ====================

def create_analysis_prompt():
    """创建股票分析 Prompt"""
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


# ==================== Chain 创建 ====================

def create_analysis_chain():
    """创建分析 Chain"""
    llm = create_llm(temperature=0.3)

    prompt, parser = create_analysis_prompt()
    chain = prompt | llm | parser

    return chain


# ==================== 主程序 ====================

def analyze_stock(stock_name: str, stock_code: str):
    """分析单只股票"""
    try:
        chain = create_analysis_chain()
        result = chain.invoke({
            "stock_name": stock_name,
            "stock_code": stock_code
        })
        return result
    except Exception as e:
        print(f"分析失败：{e}")
        return None


def print_analysis_report(result: StockAnalysis):
    """打印分析报告"""
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


def main():
    """主函数"""
    print("=" * 60)
    print("📈 股票分析助手（基础版）")
    print("=" * 60)
    print("支持功能：")
    print("  - 分析指定股票的基本信息")
    print("  - 提供投资建议")
    print("  - 输出结构化报告")
    print("\n输入'q'退出")
    print("=" * 60)

    # 预设股票池
    stock_pool = {
        "茅台": ("贵州茅台", "600519"),
        "五粮液": ("五粮液", "000858"),
        "宁德": ("宁德时代", "300750"),
        "平安": ("中国平安", "601318"),
        "招商": ("招商银行", "600036"),
    }

    print("\n💡 提示：可以直接输入股票名称或代码")
    print(f"📚 支持股票：{', '.join(stock_pool.keys())}")

    while True:
        user_input = input("\n🔍 请输入要分析股票（名称或代码）：").strip()

        if user_input.lower() == 'q':
            print("👋 再见！")
            break

        if not user_input:
            continue

        # 查找股票
        stock_name = None
        stock_code = None

        if user_input in stock_pool:
            stock_name, stock_code = stock_pool[user_input]
        elif user_input.isdigit() and len(user_input) == 6:
            # 直接输入 6 位代码
            stock_code = user_input
            stock_name = user_input
        else:
            # 尝试模糊匹配
            for name, (full_name, code) in stock_pool.items():
                if name in user_input or user_input in name:
                    stock_name = full_name
                    stock_code = code
                    break
            if not stock_name:
                stock_name = user_input
                stock_code = "未知"

        print(f"\n正在分析 {stock_name} ({stock_code})...")
        result = analyze_stock(stock_name, stock_code)

        if result:
            print_analysis_report(result)
        else:
            print("❌ 分析失败，请检查配置或网络连接")


def demo_mode():
    """演示模式：分析预设股票"""
    print("=" * 60)
    print("演示模式：分析预设股票")
    print("=" * 60)

    stocks = [
        ("贵州茅台", "600519"),
        ("宁德时代", "300750"),
    ]

    for stock_name, stock_code in stocks:
        print(f"\n分析 {stock_name}...")
        result = analyze_stock(stock_name, stock_code)
        if result:
            print_analysis_report(result)


if __name__ == "__main__":
    # 选择模式
    print("请选择模式:")
    print("1. 演示模式 (分析预设股票)")
    print("2. 交互模式 (手动输入)")

    choice = input("输入选项 (1/2): ").strip()

    if choice == "1":
        demo_mode()
    else:
        main()
