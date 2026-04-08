"""
Day 38: Function Calling

学习目标:
- 理解 Function Calling 原理
- 学会外部 API 调用
- 掌握工具选择和调用机制
- 了解错误处理方法
"""

from langchain.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from config import create_llm
import random


# ==================== 模拟 API 工具 ====================

@tool
def get_stock_price_api(symbol: str) -> str:
    """
    模拟股票价格 API

    Args:
        symbol: 股票代码
    """
    # 模拟实时价格
    prices = {
        "AAPL": 175.5 + random.uniform(-2, 2),
        "GOOGL": 140.2 + random.uniform(-2, 2),
        "MSFT": 420.8 + random.uniform(-5, 5),
        "600519": 1800.0 + random.uniform(-20, 20),
        "300750": 180.0 + random.uniform(-5, 5),
    }
    price = prices.get(symbol, 100.0)
    return f"{symbol} 实时价格：${price:.2f}"


@tool
def get_exchange_rate(from_currency: str, to_currency: str) -> str:
    """
    获取汇率（模拟 API）

    Args:
        from_currency: 源货币（如"USD"）
        to_currency: 目标货币（如"CNY"）
    """
    # 模拟汇率
    rates = {
        ("USD", "CNY"): 7.25,
        ("CNY", "USD"): 0.138,
        ("EUR", "USD"): 1.09,
        ("GBP", "USD"): 1.27,
        ("JPY", "USD"): 0.0067,
    }
    key = (from_currency.upper(), to_currency.upper())
    rate = rates.get(key, 1.0)
    return f"1 {from_currency.upper()} = {rate} {to_currency.upper()}"


@tool
def get_weather(city: str) -> str:
    """
    获取天气（模拟 API）

    Args:
        city: 城市名
    """
    weathers = {
        "北京": "晴，15-25°C",
        "上海": "多云，18-28°C",
        "深圳": "小雨，22-30°C",
        "纽约": "晴，10-20°C",
        "伦敦": "阴，8-15°C",
        "东京": "晴，12-22°C",
    }
    return f"{city} 天气：{weathers.get(city, '未知')}"


# ==================== 真实 API 调用示例 ====================

def get_real_stock_price(symbol: str) -> str:
    """
    获取真实股票价格（使用新浪财经 API）
    注意：实际使用时需要处理网络请求
    """
    try:
        # 这里用模拟数据演示
        # 实际代码应该是：
        # import requests
        # url = f"http://hq.sinajs.cn/list={symbol}"
        # response = requests.get(url, timeout=5)
        # data = response.text
        # 解析返回数据...

        prices = {
            "sh600519": "1800.00",
            "sz300750": "180.00",
        }
        key = f"sh{symbol}" if symbol.startswith("6") else f"sz{symbol}"
        price = prices.get(key, "100.00")
        return f"{symbol} 价格：{price} 元"
    except Exception as e:
        return f"API 调用失败：{str(e)}"


# ==================== 错误处理示例 ====================

@tool
def safe_api_call(symbol: str) -> str:
    """
    安全调用 API（带错误处理）

    Args:
        symbol: 股票代码
    """
    try:
        # 模拟 API 调用
        if symbol not in ["AAPL", "GOOGL", "MSFT", "600519"]:
            raise ValueError(f"未知股票：{symbol}")

        price = random.uniform(100, 500)
        return f"{symbol} 价格：${price:.2f}"
    except ValueError as e:
        return f"参数错误：{str(e)}"
    except Exception as e:
        return f"发生错误：{str(e)}"


# ==================== 多工具协调 ====================

def create_multi_tool_agent():
    """创建多工具 Agent"""
    tools = [
        get_stock_price_api,
        get_exchange_rate,
        get_weather,
        safe_api_call,
    ]

    llm = create_llm(temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个多功能助手。
你可以：
- 查询股票价格
- 查询汇率
- 查询天气
- 进行安全 API 调用

根据用户需求选择合适的工具。"""),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10
    )

    return agent_executor


# ==================== 主程序 ====================

def test_tools():
    """测试各个工具"""
    print("=" * 50)
    print("工具测试")
    print("=" * 50)

    print(f"\nget_stock_price_api('AAPL'): {get_stock_price_api.invoke({'symbol': 'AAPL'})}")
    print(f"get_exchange_rate('USD', 'CNY'): {get_exchange_rate.invoke({'from_currency': 'USD', 'to_currency': 'CNY'})}")
    print(f"get_weather('北京'): {get_weather.invoke({'city': '北京'})}")
    print(f"safe_api_call('AAPL'): {safe_api_call.invoke({'symbol': 'AAPL'})}")


def test_agent():
    """测试 Agent"""
    print("\n" + "=" * 50)
    print("多工具 Agent 测试")
    print("=" * 50)

    agent = create_multi_tool_agent()

    test_questions = [
        "苹果股票现在多少钱？",
        "美元兑人民币汇率是多少？",
        "北京今天天气怎么样？",
        "帮我查一下 GOOGL 的价格",
    ]

    for question in test_questions:
        print(f"\n问题：{question}")
        result = agent.invoke({"input": question})
        print(f"答案：{result['output']}")


def interactive_mode():
    """交互模式"""
    print("\n" + "=" * 50)
    print("多工具 Agent 交互模式")
    print("=" * 50)
    print("支持功能：")
    print("  - 查询股票价格（如：AAPL 多少钱）")
    print("  - 查询汇率（如：USD 兑 CNY）")
    print("  - 查询天气（如：北京天气）")
    print("输入'q'退出")
    print("=" * 50)

    agent = create_multi_tool_agent()

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
    print("✅ Day 38 学习完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
