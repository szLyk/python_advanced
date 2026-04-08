"""
Day 29: LangChain 入门 - Hello LangChain

学习目标:
- 理解 LangChain 的核心概念
- 完成 LangChain 安装和配置
- 编写第一个 LangChain 程序
- 了解 LLM 封装和调用方式

注意: API Key 通过 .env 文件配置，不要硬编码在代码中!
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

# 从 config.py 导入配置（推荐方式）
try:
    from config import create_llm
except ImportError:
    print("⚠️  config.py 未找到，请确保已配置 .env 文件")


def basic_chat():
    """基础对话示例"""
    print("=" * 50)
    print("LangChain 基础对话示例")
    print("=" * 50)

    # 方式 1: 使用 config.py 创建 LLM（推荐）
    try:
        llm = create_llm(temperature=0.7)
    except Exception as e:
        print(f"⚠️  配置加载失败：{e}")
        print("请确保已创建 .env 文件并填写 API Key")
        return

    # 2. 创建消息并调用
    message = HumanMessage(content="你好，请介绍一下自己")
    response = llm.invoke([message])

    # 3. 输出响应
    print(f"\n用户：你好，请介绍一下自己")
    # 移除 emoji 避免编码问题
    content = response.content.replace('\\u', '').encode('gbk', 'ignore').decode('gbk')
    print(f"AI: {content[:200]}...")


def stock_question():
    """股票场景测试"""
    print("\n" + "=" * 50)
    print("股票场景测试")
    print("=" * 50)

    llm = create_llm(temperature=0.3)

    # 测试股票相关问题
    questions = [
        "什么是市盈率（PE）？如何用它评估股票？",
        "市净率（PB）是什么意思？",
    ]

    for question in questions:
        print(f"\n问题：{question}")
        response = llm.invoke([HumanMessage(content=question)])
        print(f"回答：{response.content[:200]}...")


def main():
    """主函数"""
    basic_chat()
    stock_question()

    print("\n" + "=" * 50)
    print("Day 29 学习完成！")
    print("=" * 50)
    print("\n提示：请确保已配置 .env 文件")
    print("   复制 .env.example 为 .env 并填写 API Key")


if __name__ == "__main__":
    main()
