"""
Day 30: Prompt 模板

学习目标:
- 掌握 PromptTemplate 基础用法
- 学会变量替换技巧
- 理解 FewShot Prompting（少样本提示）
- 掌握 Prompt 设计技巧
"""

from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import create_llm


def basic_prompt_template():
    """基础 Prompt 模板示例"""
    print("=" * 50)
    print("基础 Prompt 模板示例")
    print("=" * 50)

    # 创建模板
    template = "请告诉我关于{topic}的{count}个要点"
    prompt = PromptTemplate(
        template=template,
        input_variables=["topic", "count"]
    )

    # 格式化输出
    formatted = prompt.format(topic="市盈率", count=3)
    print(f"\n格式化后的 Prompt: {formatted}")

    # 调用 LLM
    llm = create_llm(temperature=0.7)

    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"topic": "市盈率", "count": 3})
    print(f"\nLLM 回答:\n{result}")


def stock_analysis_prompt():
    """股票分析 Prompt 模板"""
    print("\n" + "=" * 50)
    print("股票分析 Prompt 模板")
    print("=" * 50)

    template = """你是一位专业的股票分析师。

股票名称：{stock_name}
股票代码：{stock_code}
当前价格：{price}

请分析这只股票的当前状况，包括：
1. 估值水平（高/中/低）
2. 投资建议（买入/持有/卖出）
3. 风险提示

分析："""

    prompt = PromptTemplate(
        template=template,
        input_variables=["stock_name", "stock_code", "price"]
    )

    llm = create_llm(temperature=0.3)

    chain = prompt | llm | StrOutputParser()

    # 测试
    result = chain.invoke({
        "stock_name": "贵州茅台",
        "stock_code": "600519",
        "price": "1800"
    })

    print(f"\n贵州茅台分析报告:\n{result}")


def few_shot_prompting():
    """FewShot Prompting 示例"""
    print("\n" + "=" * 50)
    print("FewShot Prompting 示例")
    print("=" * 50)

    # 定义示例
    examples = [
        {
            "question": "什么是 PE？",
            "answer": "PE 是市盈率（Price-to-Earnings Ratio），计算公式为：股价/每股收益。用于评估股票估值水平。"
        },
        {
            "question": "什么是 PB？",
            "answer": "PB 是市净率（Price-to-Book Ratio），计算公式为：股价/每股净资产。用于评估股票相对于净资产的溢价。"
        },
    ]

    # 示例模板
    example_template = """问题：{question}
回答：{answer}"""

    example_prompt = PromptTemplate(
        template=example_template,
        input_variables=["question", "answer"]
    )

    # FewShot 主模板
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="你是一位股票分析师助手。请根据示例的风格回答问题。",
        suffix="问题：{new_question}\n回答：",
        input_variables=["new_question"],
        example_separator="\n\n"
    )

    # 生成最终 Prompt
    final_prompt = few_shot_prompt.format(new_question="什么是 ROE？")
    print(f"生成的 Prompt:\n{final_prompt}")

    # 调用 LLM
    llm = create_llm(temperature=0.3)

    chain = few_shot_prompt | llm | StrOutputParser()
    result = chain.invoke({"new_question": "什么是 ROE？"})
    print(f"\nLLM 回答:\n{result}")


def prompt_design_tips():
    """Prompt 设计技巧演示"""
    print("\n" + "=" * 50)
    print("Prompt 设计技巧")
    print("=" * 50)

    # 技巧 1: 明确角色
    role_prompt = PromptTemplate(
        template="""你是一位拥有 10 年经验的股票分析师，擅长用通俗易懂的语言解释复杂的金融概念。
请解释：{concept}""",
        input_variables=["concept"]
    )

    # 技巧 2: 提供上下文
    context_prompt = PromptTemplate(
        template="""背景：用户正在学习股票基础知识，是初学者水平。
任务：解释以下概念，避免使用过多专业术语。
概念：{concept}""",
        input_variables=["concept"]
    )

    # 技巧 3: 指定输出格式
    format_prompt = PromptTemplate(
        template="""请用以下格式回答：
【定义】一句话定义
【公式】计算公式（如有）
【示例】一个实际例子
【应用】如何在实际中使用

概念：{concept}""",
        input_variables=["concept"]
    )

    llm = create_llm(temperature=0.3)

    # 测试不同 Prompt
    for i, prompt in enumerate([role_prompt, context_prompt, format_prompt], 1):
        print(f"\n--- 技巧 {i} ---")
        chain = prompt | llm | StrOutputParser()
        result = chain.invoke({"concept": "市盈率"})
        print(result[:300])


def main():
    """主函数"""
    basic_prompt_template()
    stock_analysis_prompt()
    few_shot_prompting()
    prompt_design_tips()

    print("\n" + "=" * 50)
    print("✅ Day 30 学习完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
