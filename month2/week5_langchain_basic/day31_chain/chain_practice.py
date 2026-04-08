"""
Day 31: Chain 链式调用

学习目标:
- 理解 Chain 的概念和作用
- 掌握 SequentialChain 顺序链
- 了解 TransformChain 数据转换
- 学会 LCEL 链式语法
"""

from langchain.chains import SequentialChain, LLMChain, TransformChain
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import create_llm


def sequential_chain_example():
    """SequentialChain 顺序链示例"""
    print("=" * 50)
    print("SequentialChain 顺序链示例")
    print("=" * 50)

    llm = create_llm(temperature=0.7)

    # 步骤 1: 解释概念
    chain1 = LLMChain(
        llm=llm,
        prompt=PromptTemplate(
            template="请解释股票术语：{term}",
            input_variables=["term"]
        ),
        output_key="definition"
    )

    # 步骤 2: 给出计算方法
    chain2 = LLMChain(
        llm=llm,
        prompt=PromptTemplate(
            template="请说明{term}的计算方法：\n{definition}",
            input_variables=["term", "definition"]
        ),
        output_key="formula"
    )

    # 步骤 3: 提供实际案例
    chain3 = LLMChain(
        llm=llm,
        prompt=PromptTemplate(
            template="请给出{term}的实际应用案例：\n{formula}",
            input_variables=["term", "formula"]
        ),
        output_key="example"
    )

    # 串联所有步骤
    overall_chain = SequentialChain(
        chains=[chain1, chain2, chain3],
        input_variables=["term"],
        output_variables=["definition", "formula", "example"],
        verbose=True
    )

    # 执行
    result = overall_chain.invoke({"term": "市盈率"})

    print("\n=== 市盈率详解 ===")
    print(f"定义：{result['definition'][:200]}...")
    print(f"\n计算方法：{result['formula'][:200]}...")
    print(f"\n实际案例：{result['example'][:200]}...")


def lcel_chain_example():
    """LCEL (LangChain Expression Language) 示例"""
    print("\n" + "=" * 50)
    print("LCEL 链式语法示例")
    print("=" * 50)

    llm = create_llm(temperature=0.7)

    # 使用 LCEL 语法（推荐）
    prompt = PromptTemplate(
        template="分析{stock}股票的投资价值，从以下几个方面：1. 行业地位 2. 财务状况 3. 估值水平",
        input_variables=["stock"]
    )

    # 使用 | 操作符串联
    chain = prompt | llm | StrOutputParser()

    # 执行
    result = chain.invoke({"stock": "贵州茅台"})

    print(f"\n贵州茅台投资价值分析:\n{result[:500]}...")


def transform_chain_example():
    """TransformChain 数据转换示例"""
    print("\n" + "=" * 50)
    print("TransformChain 数据转换示例")
    print("=" * 50)

    # 定义转换函数
    def transform_func(inputs: dict) -> dict:
        """自定义转换逻辑"""
        stock_data = inputs.get("raw_data", "{}")
        import json
        try:
            data = json.loads(stock_data)
            formatted = f"股票：{data.get('name', '未知')}, 价格：{data.get('price', 0)}, 涨幅：{data.get('change', 0)}%"
            return {"formatted_data": formatted}
        except:
            return {"formatted_data": "数据解析失败"}

    transform_chain = TransformChain(
        input_variables=["raw_data"],
        output_variables=["formatted_data"],
        transform=transform_func
    )

    # 测试
    test_data = '{"name": "贵州茅台", "price": 1800, "change": 1.5}'
    result = transform_chain.invoke({"raw_data": test_data})

    print(f"原始数据：{test_data}")
    print(f"格式化后：{result['formatted_data']}")


def stock_analysis_chain():
    """完整的股票分析 Chain"""
    print("\n" + "=" * 50)
    print("股票分析完整 Chain")
    print("=" * 50)

    llm = create_llm(temperature=0.3)

    # 步骤 1: 获取基本信息
    info_prompt = PromptTemplate(
        template="请介绍{stock_name} ({stock_code}) 的基本信息，包括行业、主营业务、市场地位。",
        input_variables=["stock_name", "stock_code"]
    )
    info_chain = LLMChain(llm=llm, prompt=info_prompt, output_key="basic_info")

    # 步骤 2: 分析竞争优势
    advantage_prompt = PromptTemplate(
        template="基于以下信息，分析{stock_name}的竞争优势：\n{basic_info}",
        input_variables=["stock_name", "basic_info"]
    )
    advantage_chain = LLMChain(llm=llm, prompt=advantage_prompt, output_key="advantage")

    # 步骤 3: 生成投资建议
    advice_prompt = PromptTemplate(
        template="基于以下分析，给出投资建议：\n基本信息：{basic_info}\n竞争优势：{advantage}",
        input_variables=["basic_info", "advantage"]
    )
    advice_chain = LLMChain(llm=llm, prompt=advice_prompt, output_key="advice")

    # 串联
    overall_chain = SequentialChain(
        chains=[info_chain, advantage_chain, advice_chain],
        input_variables=["stock_name", "stock_code"],
        output_variables=["basic_info", "advantage", "advice"],
        verbose=True
    )

    # 执行
    result = overall_chain.invoke({
        "stock_name": "贵州茅台",
        "stock_code": "600519"
    })

    print("\n=== 贵州茅台分析报告 ===")
    print(f"\n基本信息：{result['basic_info'][:200]}...")
    print(f"\n竞争优势：{result['advantage'][:200]}...")
    print(f"\n投资建议：{result['advice'][:200]}...")


def main():
    """主函数"""
    sequential_chain_example()
    lcel_chain_example()
    transform_chain_example()
    stock_analysis_chain()

    print("\n" + "=" * 50)
    print("✅ Day 31 学习完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
