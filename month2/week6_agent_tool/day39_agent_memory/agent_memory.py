"""
Day 39: 记忆管理

学习目标:
- 理解对话记忆的重要性
- 掌握 ConversationBufferMemory
- 了解 ConversationSummaryMemory
- 学会记忆长度控制
"""

from langchain.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationSummaryBufferMemory
)
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from config import create_llm
from langchain.tools import tool


# ==================== 工具定义 ====================

@tool
def get_stock_info(symbol: str) -> str:
    """获取股票信息"""
    stocks = {
        "AAPL": "苹果公司，科技巨头，主营 iPhone、Mac 等产品",
        "GOOGL": "谷歌母公司，主营搜索、广告、云服务等",
        "MSFT": "微软公司，主营软件、云服务、游戏等",
        "600519": "贵州茅台，白酒龙头，主营高端白酒生产",
    }
    return stocks.get(symbol, "未知股票")


# ==================== 基础记忆 ====================

def test_buffer_memory():
    """测试缓冲记忆"""
    print("=" * 50)
    print("ConversationBufferMemory 测试")
    print("=" * 50)

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    # 模拟对话
    memory.save_context({"input": "我叫小明"}, {"output": "你好小明！"})
    memory.save_context({"input": "我喜欢打篮球"}, {"output": "篮球是很好的运动！"})

    # 获取历史
    history = memory.chat_memory.messages
    print(f"\n对话历史 ({len(history)} 条):")
    for msg in history:
        print(f"  {msg.type}: {msg.content}")

    # 清空记忆
    memory.clear()
    print(f"\n清空后历史：{memory.chat_memory.messages}")


def test_summary_memory():
    """测试摘要记忆"""
    print("\n" + "=" * 50)
    print("ConversationSummaryMemory 测试")
    print("=" * 50)

    llm = create_llm(temperature=0)

    memory = ConversationSummaryMemory(
        llm=llm,
        memory_key="chat_history",
        return_messages=True
    )

    # 模拟长对话
    conversations = [
        ("我叫小明，今年 25 岁", "你好小明，很高兴认识你！"),
        ("我在北京工作", "北京是个好地方，工作机会很多"),
        ("我喜欢打篮球和足球", "你的运动爱好很广泛啊"),
        ("最近想看股票投资", "投资需要谨慎，建议先学习基础知识"),
    ]

    for input_text, output_text in conversations:
        memory.save_context({"input": input_text}, {"output": output_text})

    # 获取摘要
    print("\n摘要内容:")
    print(memory.buffer[:500])


def test_summary_buffer_memory():
    """测试摘要缓冲记忆（推荐）"""
    print("\n" + "=" * 50)
    print("ConversationSummaryBufferMemory 测试")
    print("=" * 50)

    llm = create_llm(temperature=0)

    memory = ConversationSummaryBufferMemory(
        llm=llm,
        memory_key="chat_history",
        return_messages=True,
        max_token_limit=500  # 超过这个长度就开始摘要
    )

    # 模拟对话
    conversations = [
        ("我叫小明", "你好！"),
        ("我今年 25 岁", "很年轻的年纪！"),
        ("我在北京工作", "北京工作机会多"),
        ("我喜欢投资", "投资需要谨慎"),
        ("最近关注股票", "建议学习基础知识"),
        ("茅台怎么样？", "茅台是白酒龙头"),
        ("估值合理吗？", "PE 约 30 倍，合理"),
    ]

    for input_text, output_text in conversations:
        memory.save_context({"input": input_text}, {"output": output_text})

    print(f"\n记忆内容长度：{len(memory.buffer)}")
    print(f"前 200 字符：{memory.buffer[:200]}...")


# ==================== 带记忆的 Agent ====================

def create_agent_with_memory():
    """创建带记忆的 Agent"""
    llm = create_llm(temperature=0.7)

    # 创建记忆
    memory = ConversationSummaryBufferMemory(
        llm=llm,
        memory_key="chat_history",
        return_messages=True,
        max_token_limit=1000
    )

    tools = [get_stock_info]

    # 创建带记忆的 Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个友好的聊天助手，可以回答股票相关问题"),
        ("placeholder", "{chat_history}"),  # 插入历史消息
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,  # 关键：传入 memory
        verbose=True,
        handle_parsing_errors=True
    )

    return agent_executor


def test_memory_agent():
    """测试带记忆的 Agent"""
    print("\n" + "=" * 50)
    print("带记忆 Agent 测试")
    print("=" * 50)

    agent = create_agent_with_memory()

    # 多轮对话测试
    conversations = [
        "我叫小明，帮我介绍一下 AAPL",
        "我刚才问的是什么公司？",  # 测试记忆
        "那 GOOGL 呢？",  # 测试上下文理解
    ]

    for question in conversations:
        print(f"\n用户：{question}")
        result = agent.invoke({"input": question})
        print(f"AI: {result['output'][:200]}...")


def interactive_mode():
    """交互模式"""
    print("\n" + "=" * 50)
    print("带记忆对话交互模式")
    print("=" * 50)
    print("AI 会记住之前的对话内容")
    print("输入'q'退出")
    print("=" * 50)

    agent = create_agent_with_memory()

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
    print("1. 记忆组件测试")
    print("2. 带记忆 Agent 测试")
    print("3. 交互模式")

    choice = input("输入选项 (1/2/3): ").strip()

    if choice == "1":
        test_buffer_memory()
        test_summary_memory()
        test_summary_buffer_memory()
    elif choice == "2":
        test_memory_agent()
    else:
        interactive_mode()

    print("\n" + "=" * 50)
    print("✅ Day 39 学习完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
