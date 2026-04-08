"""
Day 55: 综合项目 - 股票知识库 RAG 系统

项目目标:
- 加载多种来源的股票数据
- 构建向量索引
- 实现语义检索和问答
- 提供来源引用
- 支持多轮对话
"""

import os
from typing import List

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Milvus
from langchain.memory import ConversationBufferMemory
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from config import create_llm, create_embeddings

try:
    from pymilvus import connections, utility
    MILVUS_AVAILABLE = True
except ImportError:
    MILVUS_AVAILABLE = False
    print("⚠️  pymilvus 未安装，请运行：pip install pymilvus")


# ==================== 配置 ====================

COLLECTION_NAME = "stock_knowledge_rag"
MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"


# ==================== 知识库数据 ====================

def create_knowledge_base() -> List[Document]:
    """创建知识库数据（模拟）"""
    # 实际项目中可以从文件加载

    # 股票百科数据
    wiki_docs = [
        Document(
            page_content="""
市盈率（PE）
市盈率是股票价格与每股收益的比率，计算公式：PE = 股价/每股收益。
市盈率用于评估股票估值水平。一般来说：
- PE<15：低估
- PE 15-25：合理
- PE>25：高估
但不同行业的 PE 水平差异较大，需要横向比较。
""",
            metadata={"source": "股票百科", "category": "指标", "tag": "PE"}
        ),
        Document(
            page_content="""
市净率（PB）
市净率是股票价格与每股净资产的比率，计算公式：PB = 股价/每股净资产。
市净率用于评估股票相对于净资产的溢价程度。
- PB<1：股价低于净资产
- PB 1-3：合理区间
- PB>3：高溢价
银行、地产等重资产行业 PB 通常较低。
""",
            metadata={"source": "股票百科", "category": "指标", "tag": "PB"}
        ),
        Document(
            page_content="""
ROE（净资产收益率）
ROE 是净利润与净资产的比率，计算公式：ROE = 净利润/净资产。
ROE 衡量公司利用股东资本创造利润的能力。
- ROE>20%：优秀
- ROE 15%-20%：良好
- ROE<10%：较差
巴菲特曾说："如果非要我用一个指标选股，我会选择 ROE。"
""",
            metadata={"source": "股票百科", "category": "指标", "tag": "ROE"}
        ),
    ]

    # 股票研报数据
    report_docs = [
        Document(
            page_content="""
贵州茅台（600519）深度研究报告

投资要点：
1. 公司是国内高端白酒龙头企业，品牌护城河深厚
2. 2024 年 Q1 营收同比增长 18%，净利润增长 20%
3. 直销渠道占比持续提升，毛利率稳步增长
4. 当前 PE 约 30 倍，处于历史合理区间

财务数据：
- 2023 年营收：1500 亿元
- 2023 年净利润：750 亿元
- 毛利率：92%
- 净利率：50%

风险提示：宏观经济波动、白酒政策调控、原材料价格波动
""",
            metadata={"source": "茅台研报", "stock_code": "600519", "category": "研报"}
        ),
        Document(
            page_content="""
五粮液（000858）公司深度报告

核心观点：
1. 浓香型白酒龙头，产品矩阵完善
2. 第八代五粮液稳价放量，渠道改革成效显现
3. 系列酒发力，形成新的增长点
4. 当前估值低于茅台，具备配置价值

财务预测：
- 2024 年营收增速：15%
- 2024 年净利润增速：18%
- 目标价：180 元
- 当前 PE：25 倍

风险提示：高端酒竞争加剧、渠道改革不及预期
""",
            metadata={"source": "五粮液研报", "stock_code": "000858", "category": "研报"}
        ),
        Document(
            page_content="""
宁德时代（300750）研究报告

投资逻辑：
1. 全球动力电池市占率超过 30%，龙头地位稳固
2. 技术创新持续，麒麟电池、钠离子电池量产
3. 海外扩张加速，欧洲工厂投产
4. 储能业务高速增长

财务数据：
- 2023 年营收：4000 亿元
- 2023 年净利润：450 亿元
- 研发投入：180 亿元
- 全球市占率：37%

风险提示：原材料价格波动、行业竞争加剧、下游需求不及预期
""",
            metadata={"source": "宁德时代研报", "stock_code": "300750", "category": "研报"}
        ),
    ]

    # 行业数据
    industry_docs = [
        Document(
            page_content="""
白酒行业 2024 年度策略报告

行业观点：
1. 白酒行业集中度持续提升，龙头受益
2. 高端酒需求稳定，次高端竞争加剧
3. 渠道库存处于合理水平
4. 推荐关注茅五泸等龙头企业

估值分析：
- 茅台 PE(TTM): 30x，历史中枢 35x
- 五粮液 PE(TTM): 25x，历史中枢 28x
- 泸州老窖 PE(TTM): 22x，历史中枢 25x

投资策略：逢低配置龙头，关注春节动销情况
""",
            metadata={"source": "白酒行业报告", "category": "行业", "industry": "白酒"}
        ),
        Document(
            page_content="""
新能源行业 2024 年度策略报告

行业观点：
1. 全球电动车渗透率持续提升
2. 动力电池需求旺盛
3. 储能市场爆发式增长
4. 推荐关注宁德时代等龙头企业

政策环境：
- 中国：双碳目标支持
- 欧洲：2035 年禁售燃油车
- 美国：通胀削减法案补贴

风险提示：原材料价格波动、地缘政治风险
""",
            metadata={"source": "新能源行业报告", "category": "行业", "industry": "新能源"}
        ),
    ]

    return wiki_docs + report_docs + industry_docs


# ==================== 数据处理 ====================

def process_documents(documents: List[Document]) -> List[Document]:
    """处理文档（分块）"""
    print(f"原始文档数：{len(documents)}")

    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", "！", "？"],
        chunk_size=300,
        chunk_overlap=30
    )

    chunks = splitter.split_documents(documents)
    print(f"分块后文档数：{len(chunks)}")

    # 打印统计信息
    chunk_sizes = [len(c.page_content) for c in chunks]
    print(f"平均块大小：{sum(chunk_sizes) / len(chunk_sizes):.0f} 字符")

    return chunks


# ==================== VectorStore ====================

def create_vector_store(documents: List[Document]) -> Milvus:
    """创建向量存储"""
    print("\n连接 Milvus...")
    connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)

    embeddings = create_embeddings()

    print("创建 VectorStore...")
    vectorstore = Milvus.from_documents(
        documents=documents,
        embedding=embeddings,
        connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT},
        collection_name=COLLECTION_NAME,
        drop_old=True
    )

    print(f"✅ VectorStore '{COLLECTION_NAME}' 创建成功")
    return vectorstore


def load_vector_store() -> Milvus:
    """加载现有 VectorStore"""
    print("\n连接 Milvus...")
    connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)

    embeddings = create_embeddings()

    vectorstore = Milvus(
        embedding_function=embeddings,
        connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT},
        collection_name=COLLECTION_NAME,
    )

    print(f"✅ VectorStore '{COLLECTION_NAME}' 加载成功")
    return vectorstore


# ==================== RAG 系统 ====================

def create_retriever(vectorstore, k: int = 3):
    """创建检索器"""
    return vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": k, "score_threshold": 0.3}
    )


def create_rag_chain(retriever, memory=None):
    """创建 RAG 问答链"""
    llm = create_llm(temperature=0.3)

    system_prompt = """你是股票知识库助手 RAG 系统。请根据以下上下文回答问题。

【上下文信息】
{context}

【用户问题】
{input}

【回答要求】
1. 先给出核心结论（1-2 句话）
2. 详细解释并引用来源（如"根据 XX 研报"）
3. 如有数据请列出具体数值
4. 如果上下文中没有答案，请说明"资料不足"
5. 保持专业但易懂的风格

请用中文回答。"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    combine_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, combine_chain)

    return rag_chain


# ==================== 主程序 ====================

def build_knowledge_base():
    """构建知识库"""
    print("=" * 60)
    print("构建股票知识库")
    print("=" * 60)

    # 加载文档
    print("\n📚 加载文档...")
    documents = create_knowledge_base()

    # 分块
    print("\n✂️  文本分块...")
    chunks = process_documents(documents)

    # 创建 VectorStore
    print("\n💾 创建向量索引...")
    vectorstore = create_vector_store(chunks)

    print("\n✅ 知识库构建完成！")
    return vectorstore


def print_welcome():
    """打印欢迎信息"""
    print("\n" + "=" * 60)
    print("📈 股票知识库 RAG 系统")
    print("=" * 60)
    print("支持功能：")
    print("  - 股票百科问答（PE、PB、ROE 等）")
    print("  - 个股研报查询（茅台、五粮液、宁德时代）")
    print("  - 行业分析（白酒、新能源）")
    print("  - 多轮对话")
    print("\n输入命令：")
    print("  - 'help': 显示帮助")
    print("  - 'clear': 清空对话历史")
    print("  - 'quit': 退出系统")
    print("=" * 60)


def interactive_mode():
    """交互模式"""
    print_welcome()

    # 加载 VectorStore
    vectorstore = load_vector_store()
    retriever = create_retriever(vectorstore)
    rag_chain = create_rag_chain(retriever)

    # 对话记忆
    memory = ConversationBufferMemory(return_messages=True)

    while True:
        user_input = input("\n🔍 请输入：").strip()

        if user_input.lower() == 'quit':
            print("👋 再见！")
            break

        if user_input.lower() == 'help':
            print("\n帮助：")
            print("  可以问的问题示例：")
            print("  - '市盈率是什么意思？'")
            print("  - '茅台的投资价值如何？'")
            print("  - '白酒行业有什么投资机会？'")
            print("  - '宁德时代和比亚迪哪个更好？'")
            continue

        if user_input.lower() == 'clear':
            memory.clear()
            print("✅ 对话历史已清空")
            continue

        if not user_input:
            continue

        try:
            response = rag_chain.invoke({"input": user_input})
            print(f"\n🤖 {response['answer']}")
            print(f"\n📚 参考来源：{len(response['context'])} 篇文档")

            # 保存到记忆
            memory.save_context({"input": user_input}, {"output": response['answer']})

        except Exception as e:
            print(f"\n❌ 错误：{e}")


def demo_mode():
    """演示模式"""
    print("=" * 60)
    print("演示模式")
    print("=" * 60)

    # 构建知识库
    vectorstore = build_knowledge_base()
    retriever = create_retriever(vectorstore)
    rag_chain = create_rag_chain(retriever)

    # 演示问题
    questions = [
        "市盈率是什么意思？",
        "茅台的投资价值如何？",
        "白酒行业有什么投资机会？",
        "宁德时代的竞争优势是什么？",
        "茅台和五粮液哪个 PE 更低？",
    ]

    for question in questions:
        print(f"\n{'='*60}")
        print(f"问题：{question}")
        print("=" * 60)

        response = rag_chain.invoke({"input": question})
        print(f"答案：{response['answer'][:600]}...")
        print(f"参考来源：{len(response['context'])} 篇文档")


def main():
    """主函数"""
    if not MILVUS_AVAILABLE:
        print("\n❌ pymilvus 未安装")
        return

    print("请选择模式:")
    print("1. 演示模式（构建索引 + 测试）")
    print("2. 交互模式（问答）")

    choice = input("\n输入选项 (1/2): ").strip()

    if choice == "1":
        demo_mode()
    else:
        interactive_mode()

    print("\n" + "=" * 60)
    print("✅ Day 55 学习完成！")
    print("=" * 60)
    print("\n🎉 Month 2 全部完成！你已掌握 LangChain + Agent + RAG 的核心能力！")


if __name__ == "__main__":
    main()
