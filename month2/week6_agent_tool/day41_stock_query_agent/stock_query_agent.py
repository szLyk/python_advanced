"""
Day 41: 综合项目 - 股票查询 Agent

项目目标:
- 创建一个完整的股票查询 Agent
- 支持自然语言股票查询
- 集成多个股票数据 Tool
- 实现多轮对话记忆
"""

from langchain.memory import ConversationSummaryBufferMemory
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from config import create_llm
from langchain.tools import tool
import random


# ==================== 模拟股票数据 ====================

STOCK_DATA = {
    "AAPL": {
        "name": "苹果公司",
        "price": 175.5,
        "change": 1.2,
        "change_pct": 0.69,
        "pe": 28.5,
        "market_cap": "2.8 万亿",
        "industry": "科技",
        "description": "全球科技巨头，主营 iPhone、Mac、iPad 等产品"
    },
    "GOOGL": {
        "name": "谷歌母公司",
        "price": 140.2,
        "change": -0.5,
        "change_pct": -0.36,
        "pe": 25.1,
        "market_cap": "1.8 万亿",
        "industry": "科技",
        "description": "全球最大搜索引擎，主营广告、云服务"
    },
    "MSFT": {
        "name": "微软公司",
        "price": 420.8,
        "change": 2.1,
        "change_pct": 0.50,
        "pe": 35.2,
        "market_cap": "3.1 万亿",
        "industry": "科技",
        "description": "全球最大软件公司，主营 Windows、Office、Azure"
    },
    "600519": {
        "name": "贵州茅台",
        "price": 1800.0,
        "change": 0.8,
        "change_pct": 0.04,
        "pe": 30.5,
        "market_cap": "2.3 万亿",
        "industry": "白酒",
        "description": "中国高端白酒龙头企业"
    },
    "300750": {
        "name": "宁德时代",
        "price": 180.0,
        "change": 1.5,
        "change_pct": 0.84,
        "pe": 20.1,
        "market_cap": "7800 亿",
        "industry": "新能源",
        "description": "全球动力电池龙头企业"
    },
    "000858": {
        "name": "五粮液",
        "price": 150.0,
        "change": -0.3,
        "change_pct": -0.20,
        "pe": 25.3,
        "market_cap": "5800 亿",
        "industry": "白酒",
        "description": "中国浓香型白酒代表"
    },
}


# ==================== 工具定义 ====================

@tool
def get_stock_price(symbol: str) -> str:
    """
    获取股票当前价格

    Args:
        symbol: 股票代码，如"AAPL"、"600519"
    """
    if symbol not in STOCK_DATA:
        return f"未找到股票：{symbol}"

    data = STOCK_DATA[symbol]
    direction = "涨" if data['change'] > 0 else "跌"
    return f"{data['name']} ({symbol}) 当前价格：{data['price']} 元，{direction}{data['change_pct']}%"


@tool
def get_stock_info(symbol: str) -> str:
    """
    获取股票基本信息

    Args:
        symbol: 股票代码
    """
    if symbol not in STOCK_DATA:
        return f"未找到股票：{symbol}"

    data = STOCK_DATA[symbol]
    direction = "涨" if data['change'] > 0 else "跌"
    return (
        f"===== {data['name']} ({symbol}) =====\n"
        f"所属行业：{data['industry']}\n"
        f"当前价格：{data['price']} 元 ({direction}{data['change_pct']}%)\n"
        f"市盈率：{data['pe']}\n"
        f"市值：{data['market_cap']}\n"
        f"公司简介：{data['description']}"
    )


@tool
def get_stock_pe(symbol: str) -> str:
    """
    获取股票市盈率

    Args:
        symbol: 股票代码
    """
    if symbol not in STOCK_DATA:
        return f"未找到股票：{symbol}"

    data = STOCK_DATA[symbol]
    return f"{data['name']} ({symbol}) PE: {data['pe']}"


@tool
def compare_stocks(symbol1: str, symbol2: str) -> str:
    """
    比较两只股票

    Args:
        symbol1: 第一只股票代码
        symbol2: 第二只股票代码
    """
    if symbol1 not in STOCK_DATA or symbol2 not in STOCK_DATA:
        return "未找到相关股票信息"

    s1 = STOCK_DATA[symbol1]
    s2 = STOCK_DATA[symbol2]

    return (
        f"===== 股票对比 =====\n"
        f"{s1['name']} ({symbol1}) vs {s2['name']} ({symbol2})\n\n"
        f"价格：{s1['price']} vs {s2['price']}\n"
        f"PE: {s1['pe']} vs {s2['pe']}\n"
        f"市值：{s1['market_cap']} vs {s2['market_cap']}\n"
        f"行业：{s1['industry']} vs {s2['industry']}"
    )


@tool
def get_stock_news(symbol: str) -> str:
    """
    获取股票相关新闻（模拟）

    Args:
        symbol: 股票代码
    """
    if symbol not in STOCK_DATA:
        return f"未找到股票：{symbol}"

    name = STOCK_DATA[symbol]["name"]

    news_templates = [
        f"{name} 发布最新季度财报，营收超预期",
        f"{name} 新产品发布，市场反响热烈",
        f"分析师上调{name}目标价",
        f"{name} 获得机构投资者增持",
        f"{name} 与某知名企业达成战略合作",
    ]

    # 随机选择 3 条新闻
    news = random.sample(news_templates, min(3, len(news_templates)))
    return "\n".join([f"[{i+1}] {n}" for i, n in enumerate(news)])


# ==================== Agent 创建 ====================

STOCK_AGENT_PROMPT = """你是一位专业的股票分析助手。

你可以帮用户：
1. 查询股票价格和基本信息
2. 查询市盈率等指标
3. 比较两只股票
4. 获取相关新闻

回答规则：
- 使用专业但易懂的语言
- 数据要准确
- 主动提供相关建议
- 如果用户提到"它"、"这个"等代词，根据上下文理解

如果用户查询的股票不存在，友好地提示用户。"""


def create_stock_agent(verbose=False):
    """创建股票查询 Agent"""
    llm = create_llm(temperature=0.3)

    # 工具列表
    tools = [
        get_stock_price,
        get_stock_info,
        get_stock_pe,
        compare_stocks,
        get_stock_news,
    ]

    # 创建记忆
    memory = ConversationSummaryBufferMemory(
        llm=llm,
        memory_key="chat_history",
        return_messages=True,
        max_token_limit=1500
    )

    # Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", STOCK_AGENT_PROMPT),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # 创建 Agent
    agent = create_tool_calling_agent(llm, tools, prompt)

    # 创建执行器
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=verbose,
        handle_parsing_errors=True,
        max_iterations=10
    )

    return agent_executor


# ==================== 主程序 ====================

def demo_mode():
    """演示模式"""
    print("=" * 60)
    print("🤖 股票查询 Agent 演示")
    print("=" * 60)

    agent = create_stock_agent(verbose=True)

    # 预设问题
    questions = [
        "帮我看看贵州茅台的情况",
        "它的 PE 是多少？",  # 测试记忆
        "那五粮液呢？",  # 测试上下文
        "比较一下茅台和五粮液",
    ]

    for question in questions:
        print(f"\n用户：{question}")
        result = agent.invoke({"input": question})
        print(f"\nAI: {result['output'][:400]}...")


def interactive_mode():
    """交互模式"""
    print("\n" + "=" * 60)
    print("🤖 股票查询 Agent")
    print("=" * 60)
    print("支持股票：AAPL, GOOGL, MSFT, 600519, 300750, 000858")
    print("支持功能：")
    print("  - 查询股票价格")
    print("  - 获取股票信息")
    print("  - 查询 PE 等指标")
    print("  - 股票对比")
    print("  - 新闻查询")
    print("\n输入'q'退出")
    print("=" * 60)

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
            print(f"\n❌ 错误：{e}")


def main():
    """主函数"""
    print("请选择模式:")
    print("1. 演示模式（预设问题）")
    print("2. 交互模式（手动输入）")

    choice = input("输入选项 (1/2): ").strip()

    if choice == "1":
        demo_mode()
    else:
        interactive_mode()

    print("\n" + "=" * 60)
    print("✅ Day 41 学习完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
