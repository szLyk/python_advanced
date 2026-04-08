"""
Day 36: Agent 基础

学习目标:
- 理解 Agent 的概念和作用
- 掌握 ReAct 模式原理
- 了解 LangChain Agent 类型
- 能够运行简单的 Zero-shot Agent
"""

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from config import create_llm
from langchain.tools import tool


# ==================== 工具定义 ====================

@tool
def calculator(expression: str) -> str:
    """
    计算数学表达式

    Args:
        expression: 数学表达式，如 "123 * 456"

    Returns:
        计算结果
    """
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误：{e}"


@tool
def get_stock_price(symbol: str) -> str:
    """
    获取股票价格（模拟）

    Args:
        symbol: 股票代码
    """
    prices = {
        "AAPL": "175.5",
        "GOOGL": "140.2",
        "MSFT": "420.8",
        "600519": "1800.0",
        "300750": "180.0",
    }
    return f"{symbol} 价格：${prices.get(symbol, '未知')}"


@tool
def get_pe_ratio(symbol: str) -> str:
    """
    获取市盈率（模拟）

    Args:
        symbol: 股票代码
    """
    pes = {
        "AAPL": "28.5",
        "GOOGL": "25.1",
        "MSFT": "35.2",
        "600519": "30.5",
        "300750": "20.1",
    }
    return f"{symbol} PE: {pes.get(symbol, '未知')}"


# ==================== Agent 创建 ====================

def create_basic_agent():
    """创建基础 Agent"""
    tools = [calculator]

    llm = create_llm(temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个数学助手，帮助用户进行计算"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )

    return agent_executor


def create_stock_agent():
    """创建股票 Agent"""
    tools = [get_stock_price, get_pe_ratio]

    llm = create_llm(temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个股票助手，帮助用户查询股票信息"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )

    return agent_executor


# ==================== 主程序 ====================

def test_calculator_agent():
    """测试计算器 Agent"""
    print("=" * 50)
    print("计算器 Agent 测试")
    print("=" * 50)

    agent = create_basic_agent()

    test_questions = [
        "计算 123 * 456",
        "1000 + 2000 + 3000 等于多少",
        "50 * 2 + 100 = ?",
    ]

    for question in test_questions:
        print(f"\n问题：{question}")
        result = agent.invoke({"input": question})
        print(f"答案：{result['output']}")


def test_stock_agent():
    """测试股票 Agent"""
    print("\n" + "=" * 50)
    print("股票 Agent 测试")
    print("=" * 50)

    agent = create_stock_agent()

    test_questions = [
        "苹果股票现在多少钱？",
        "茅台的 PE 是多少？",
        "比较一下 AAPL 和 GOOGL 的估值",
    ]

    for question in test_questions:
        print(f"\n问题：{question}")
        result = agent.invoke({"input": question})
        print(f"答案：{result['output']}")


def interactive_mode():
    """交互模式"""
    print("\n" + "=" * 50)
    print("Agent 交互模式")
    print("=" * 50)
    print("支持功能：")
    print("  - 数学计算（如：计算 123 * 456）")
    print("  - 股票查询（如：AAPL 多少钱）")
    print("输入'q'退出")
    print("=" * 50)

    tools = [calculator, get_stock_price, get_pe_ratio]

    llm = create_llm(temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个多功能助手，可以帮助计算和查询股票"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )

    while True:
        user_input = input("\n🔍 请输入：").strip()

        if user_input.lower() == 'q':
            print("👋 再见！")
            break

        if not user_input:
            continue

        try:
            result = agent_executor.invoke({"input": user_input})
            print(f"\n🤖 {result['output']}")
        except Exception as e:
            print(f"❌ 错误：{e}")


def main():
    """主函数"""
    print("请选择模式:")
    print("1. 测试模式（运行预设问题）")
    print("2. 交互模式（手动输入）")

    choice = input("输入选项 (1/2): ").strip()

    if choice == "1":
        test_calculator_agent()
        test_stock_agent()
    else:
        interactive_mode()

    print("\n" + "=" * 50)
    print("✅ Day 36 学习完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
