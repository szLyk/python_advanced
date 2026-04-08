"""
Day 37: Tool 定义

学习目标:
- 理解 LangChain Tool 的概念
- 掌握 @tool 装饰器使用
- 学会自定义工具注册
- 理解 Tool 描述和参数设计
"""

from langchain.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from config import create_llm
import random


# ==================== 基础工具 ====================

@tool
def add(a: float, b: float) -> str:
    """两个数相加"""
    return str(a + b)


@tool
def multiply(a: float, b: float) -> str:
    """两个数相乘"""
    return str(a * b)


# ==================== 股票工具集 ====================

# 模拟股票数据
STOCK_DATA = {
    "AAPL": {"name": "苹果", "price": 175.5, "pe": 28.5, "change": 1.2},
    "GOOGL": {"name": "谷歌", "price": 140.2, "pe": 25.1, "change": -0.5},
    "MSFT": {"name": "微软", "price": 420.8, "pe": 35.2, "change": 2.1},
    "600519": {"name": "贵州茅台", "price": 1800.0, "pe": 30.5, "change": 0.8},
    "300750": {"name": "宁德时代", "price": 180.0, "pe": 20.1, "change": 1.5},
    "000858": {"name": "五粮液", "price": 150.0, "pe": 25.3, "change": -0.3},
}


@tool
def get_stock_price(symbol: str) -> str:
    """
    获取股票当前价格

    Args:
        symbol: 股票代码，如"AAPL"、"600519"

    Returns:
        股票价格信息
    """
    if symbol not in STOCK_DATA:
        return f"未找到股票：{symbol}"

    data = STOCK_DATA[symbol]
    return f"{data['name']} ({symbol}) 当前价格：{data['price']} 元"


@tool
def get_stock_pe(symbol: str) -> str:
    """
    获取股票市盈率

    Args:
        symbol: 股票代码

    Returns:
        市盈率信息
    """
    if symbol not in STOCK_DATA:
        return f"未找到股票：{symbol}"

    data = STOCK_DATA[symbol]
    return f"{data['name']} ({symbol}) PE: {data['pe']}"


@tool
def get_stock_change(symbol: str) -> str:
    """
    获取股票涨跌幅

    Args:
        symbol: 股票代码

    Returns:
        涨跌幅信息
    """
    if symbol not in STOCK_DATA:
        return f"未找到股票：{symbol}"

    data = STOCK_DATA[symbol]
    direction = "涨" if data['change'] > 0 else "跌"
    return f"{data['name']} ({symbol}) {direction}{abs(data['change'])}%"


@tool
def get_stock_info(symbol: str) -> str:
    """
    获取股票完整信息

    Args:
        symbol: 股票代码

    Returns:
        完整股票信息
    """
    if symbol not in STOCK_DATA:
        return f"未找到股票：{symbol}"

    data = STOCK_DATA[symbol]
    direction = "涨" if data['change'] > 0 else "跌"
    return (
        f"===== {data['name']} ({symbol}) =====\n"
        f"当前价格：{data['price']} 元\n"
        f"涨跌幅：{direction}{abs(data['change'])}%\n"
        f"市盈率：{data['pe']}"
    )


# ==================== 新闻查询工具 ====================

@tool
def search_stock_news(symbol: str, days: int = 7) -> str:
    """
    搜索股票相关新闻

    Args:
        symbol: 股票代码
        days: 查询最近 N 天的新闻

    Returns:
        新闻摘要列表
    """
    if symbol not in STOCK_DATA:
        return f"未找到股票：{symbol}"

    name = STOCK_DATA[symbol]["name"]

    # 模拟新闻数据
    news_templates = [
        f"{name} 发布最新季度财报，营收同比增长 X%",
        f"{name} 新产品发布，市场反响热烈",
        f"分析师上调{name}目标价至 X 元",
        f"{name} 与某知名企业达成战略合作",
        f"{name} 获得机构投资者增持",
    ]

    news = []
    for i in range(min(days, 5)):
        template = news_templates[i % len(news_templates)]
        news_item = template.replace("X", str(random.randint(10, 50)))
        news.append(f"[{i+1}天前] {news_item}")

    return "\n".join(news)


# ==================== Agent 创建 ====================

def create_stock_agent(verbose=False):
    """创建股票 Agent"""
    tools = [
        get_stock_price,
        get_stock_pe,
        get_stock_change,
        get_stock_info,
        search_stock_news,
    ]

    llm = create_llm(temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是股票分析助手。
你可以帮助用户查询：
- 股票价格
- 市盈率
- 涨跌幅
- 完整信息
- 相关新闻

请用专业但易懂的语言回答。"""),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=verbose,
        handle_parsing_errors=True,
        max_iterations=10
    )

    return agent_executor


# ==================== 主程序 ====================

def test_tools():
    """测试工具"""
    print("=" * 50)
    print("工具测试")
    print("=" * 50)

    # 测试各个工具
    print(f"\nget_stock_price('AAPL'): {get_stock_price.invoke({'symbol': 'AAPL'})}")
    print(f"get_stock_pe('600519'): {get_stock_pe.invoke({'symbol': '600519'})}")
    print(f"get_stock_change('300750'): {get_stock_change.invoke({'symbol': '300750'})}")
    print(f"get_stock_info('000858'): {get_stock_info.invoke({'symbol': '000858'})}")
    print(f"\nsearch_stock_news('AAPL', 3):\n{search_stock_news.invoke({'symbol': 'AAPL', 'days': 3})}")


def test_agent():
    """测试 Agent"""
    print("\n" + "=" * 50)
    print("Agent 测试")
    print("=" * 50)

    agent = create_stock_agent(verbose=True)

    test_questions = [
        "苹果股票现在多少钱？",
        "茅台的 PE 是多少？",
        "宁德时代今天涨了吗？",
        "帮我看看五粮液的情况",
        "AAPL 最近有什么新闻？",
    ]

    for question in test_questions:
        print(f"\n问题：{question}")
        result = agent.invoke({"input": question})
        print(f"答案：{result['output'][:300]}...")


def interactive_mode():
    """交互模式"""
    print("\n" + "=" * 50)
    print("股票 Agent 交互模式")
    print("=" * 50)
    print("支持股票：AAPL, GOOGL, MSFT, 600519, 300750, 000858")
    print("输入'q'退出")
    print("=" * 50)

    agent = create_stock_agent(verbose=False)

    while True:
        user_input = input("\n🔍 请输入：").strip()

        if user_input.lower() == 'q':
            print("👋 再见！")
            break

        if not user_input:
            continue

        try:
            result = agent.invoke({"input": user_input})
            print(f"\n🤖 {result['output']}")
        except Exception as e:
            print(f"❌ 错误：{e}")


def main():
    """主函数"""
    print("请选择模式:")
    print("1. 工具测试")
    print("2. Agent 测试（预设问题）")
    print("3. 交互模式")

    choice = input("输入选项 (1/2/3): ").strip()

    if choice == "1":
        test_tools()
    elif choice == "2":
        test_agent()
    else:
        interactive_mode()

    print("\n" + "=" * 50)
    print("✅ Day 37 学习完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
