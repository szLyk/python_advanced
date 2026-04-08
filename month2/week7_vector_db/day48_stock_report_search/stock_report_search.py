"""
Day 48: 综合项目 - 股票研报检索系统

项目目标:
- 加载 PDF/TXT 研报文档
- 自动分块和向量化
- 语义检索相关研报
- 返回带来源的检索结果
"""

import os
from typing import List

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Milvus
from langchain.retrievers import SelfQueryRetriever
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from config import create_llm, create_embeddings

# 检查依赖
try:
    from pymilvus import connections, utility
    MILVUS_AVAILABLE = True
except ImportError:
    MILVUS_AVAILABLE = False
    print("⚠️  pymilvus 未安装，请运行：pip install pymilvus")


# ==================== 配置 ====================

COLLECTION_NAME = "stock_reports"
MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"


def get_embeddings():
    """获取 Embedding 模型"""
    return create_embeddings()


def get_text_splitter():
    """获取文本分块器"""
    return RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", "！", "？", " "],
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
    )


# ==================== 文档加载 ====================

def load_sample_documents() -> List[Document]:
    """加载示例文档（模拟研报数据）"""
    # 实际项目中可以从文件加载
    sample_reports = [
        Document(
            page_content="""贵州茅台（600519）深度研究报告

投资要点：
1. 公司是国内高端白酒龙头企业，品牌护城河深厚
2. 2024 年 Q1 营收同比增长 18%，净利润增长 20%
3. 直销渠道占比持续提升，毛利率稳步增长
4. 当前 PE 约 30 倍，处于历史合理区间

风险提示：
- 宏观经济波动风险
- 白酒政策调控风险
- 原材料价格波动
""",
            metadata={"source": "maotai_research.pdf", "stock_code": "600519", "category": "研报", "year": 2024}
        ),
        Document(
            page_content="""五粮液（000858）公司深度报告

核心观点：
1. 浓香型白酒龙头，产品矩阵完善
2. 第八代五粮液稳价放量，渠道改革成效显现
3. 系列酒发力，形成新的增长点
4. 当前估值低于茅台，具备配置价值

财务预测：
- 2024 年营收增速：15%
- 2024 年净利润增速：18%
- 目标价：180 元
""",
            metadata={"source": "wuliangye_report.pdf", "stock_code": "000858", "category": "研报", "year": 2024}
        ),
        Document(
            page_content="""白酒行业 2024 年度策略报告

行业观点：
1. 白酒行业集中度持续提升，龙头受益
2. 高端酒需求稳定，次高端竞争加剧
3. 渠道库存处于合理水平
4. 推荐关注茅五泸等龙头企业

估值分析：
- 茅台 PE(TTM): 30x
- 五粮液 PE(TTM): 25x
- 泸州老窖 PE(TTM): 22x
""",
            metadata={"source": "baijiu_industry_2024.pdf", "category": "行业报告", "year": 2024}
        ),
        Document(
            page_content="""宁德时代（300750）研究报告

投资逻辑：
1. 全球动力电池市占率超过 30%，龙头地位稳固
2. 技术创新持续，麒麟电池、钠离子电池量产
3. 海外扩张加速，欧洲工厂投产
4. 储能业务高速增长

风险提示：
- 原材料价格波动
- 行业竞争加剧
- 下游需求不及预期
""",
            metadata={"source": "ningdeyang_report.pdf", "stock_code": "300750", "category": "研报", "year": 2024}
        ),
    ]

    return sample_reports


# ==================== 数据处理 ====================

def process_documents(documents: List[Document]) -> List[Document]:
    """处理文档（分块）"""
    print(f"原始文档数：{len(documents)}")

    splitter = get_text_splitter()
    chunks = splitter.split_documents(documents)

    print(f"分块后文档数：{len(chunks)}")

    return chunks


# ==================== VectorStore ====================

def create_vector_store(documents: List[Document]) -> Milvus:
    """创建向量存储"""
    print("\n连接 Milvus...")
    connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)

    embeddings = get_embeddings()

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

    embeddings = get_embeddings()

    vectorstore = Milvus(
        embedding_function=embeddings,
        connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT},
        collection_name=COLLECTION_NAME,
    )

    print(f"✅ VectorStore '{COLLECTION_NAME}' 加载成功")
    return vectorstore


# ==================== 检索系统 ====================

def create_retriever(vectorstore, k: int = 3):
    """创建检索器"""
    return vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": k, "score_threshold": 0.3}
    )


def create_rag_chain(retriever):
    """创建 RAG 问答链"""
    llm = create_llm(temperature=0.3)

    system_prompt = """你是股票研报分析助手。请根据以下研报内容回答问题。

研报内容：
{context}

问题：{input}

回答要求：
1. 先给出核心结论
2. 引用具体研报来源
3. 如有数据请列出具体数值
4. 如果研报中没有相关信息，请说明

请用中文专业但易懂的语言回答。"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    combine_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, combine_chain)

    return rag_chain


# ==================== 主程序 ====================

def build_index():
    """构建索引"""
    print("=" * 60)
    print("构建股票研报索引")
    print("=" * 60)

    # 加载文档
    print("\n📚 加载文档...")
    documents = load_sample_documents()

    # 分块
    print("\n✂️  文本分块...")
    chunks = process_documents(documents)

    # 创建 VectorStore
    print("\n💾 创建向量索引...")
    vectorstore = create_vector_store(chunks)

    print("\n✅ 索引构建完成！")
    return vectorstore


def search_reports(query: str, retriever) -> List:
    """搜索研报"""
    docs = retriever.invoke(query)

    print(f"\n🔍 找到 {len(docs)} 篇相关研报:")
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "未知")
        content = doc.page_content[:100] + "..."
        print(f"\n[{i}] 来源：{source}")
        print(f"    内容：{content}")

    return docs


def interactive_mode():
    """交互模式"""
    print("\n" + "=" * 60)
    print("📈 股票研报检索系统")
    print("=" * 60)

    # 加载 VectorStore
    vectorstore = load_vector_store()
    retriever = create_retriever(vectorstore)
    rag_chain = create_rag_chain(retriever)

    print("\n支持功能：")
    print("  - 研报语义检索")
    print("  - 智能问答")
    print("输入'q'退出")
    print("=" * 60)

    while True:
        user_input = input("\n🔍 请输入查询：").strip()

        if user_input.lower() == 'q':
            print("👋 再见！")
            break

        if not user_input:
            continue

        try:
            # RAG 问答
            response = rag_chain.invoke({"input": user_input})
            print(f"\n🤖 {response['answer']}")
            print(f"\n📚 参考来源：{len(response['context'])} 篇文档")

        except Exception as e:
            print(f"\n❌ 错误：{e}")


def demo_mode():
    """演示模式"""
    print("\n" + "=" * 60)
    print("演示模式")
    print("=" * 60)

    # 构建索引
    vectorstore = build_index()
    retriever = create_retriever(vectorstore)
    rag_chain = create_rag_chain(retriever)

    # 测试问题
    questions = [
        "茅台的投资价值如何？",
        "白酒行业 2024 年有什么投资机会？",
        "宁德时代的竞争优势是什么？",
    ]

    for question in questions:
        print(f"\n{'='*60}")
        print(f"问题：{question}")
        print("=" * 60)

        response = rag_chain.invoke({"input": question})
        print(f"答案：{response['answer'][:500]}...")


def main():
    """主函数"""
    import sys

    print("请选择模式:")
    print("1. 演示模式（构建索引 + 测试）")
    print("2. 交互模式（问答）")

    choice = input("\n输入选项 (1/2): ").strip()

    if not MILVUS_AVAILABLE:
        print("\n❌ pymilvus 未安装")
        return

    if choice == "1":
        demo_mode()
    else:
        interactive_mode()

    print("\n" + "=" * 60)
    print("✅ Day 48 学习完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
