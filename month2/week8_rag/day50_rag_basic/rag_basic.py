"""
Day 50: RAG 原理

学习目标:
- 理解 RAG（检索增强生成）概念
- 掌握 RAG 工作流程
- 了解 RAG vs 纯 LLM 的区别
- 学会 RAG 应用场景分析
"""

from langchain.vectorstores import Milvus
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from config import create_llm, create_embeddings

try:
    from pymilvus import connections
    MILVUS_AVAILABLE = True
except ImportError:
    MILVUS_AVAILABLE = False


def compare_llm_vs_rag():
    """对比纯 LLM 和 RAG"""
    print("=" * 60)
    print("纯 LLM vs RAG 对比")
    print("=" * 60)

    print("""
【纯 LLM 方式】
用户问题 → [LLM] → 答案
- 仅靠训练记忆
- 可能过时（训练数据截止）
- 可能编造（幻觉问题）
- 无法追溯来源

【RAG 方式】
用户问题 → [检索] → 相关文档 → [LLM] → 答案
- 基于检索到的事实
- 可以使用最新数据
- 减少幻觉
- 可提供来源引用

【示例对比】
问题："2024 年白酒行业发展趋势如何？"

纯 LLM 回答:
"根据我的知识，白酒行业..."
❌ 可能过时，无法确认数据来源

RAG 回答:
"根据 XX 研报（2024 年 3 月），白酒行业..."
✅ 基于最新研报，可追溯来源
""")


def create_mock_vectorstore():
    """创建模拟 VectorStore（演示用）"""
    print("\n" + "=" * 60)
    print("创建模拟 VectorStore")
    print("=" * 60)

    if not MILVUS_AVAILABLE:
        print("⚠️  pymilvus 未安装，使用模拟数据演示")
        return None

    try:
        from langchain.schema import Document

        # 准备文档
        documents = [
            Document(
                page_content="贵州茅台 2024 年 Q1 营收同比增长 18%，净利润增长 20%",
                metadata={"source": "茅台研报", "year": 2024}
            ),
            Document(
                page_content="白酒行业集中度持续提升，龙头企业受益",
                metadata={"source": "白酒行业报告", "year": 2024}
            ),
            Document(
                page_content="宁德时代动力电池市占率超过 30%",
                metadata={"source": "新能源研报", "year": 2024}
            ),
        ]

        connections.connect(host="localhost", port="19530")

        embeddings = create_embeddings()

        vectorstore = Milvus.from_documents(
            documents=documents,
            embedding=embeddings,
            connection_args={"host": "localhost", "port": "19530"},
            collection_name="rag_demo",
            drop_old=True
        )

        print("✅ VectorStore 创建成功")
        return vectorstore

    except Exception as e:
        print(f"⚠️  创建失败：{e}")
        print("将继续使用纯文字演示 RAG 流程")
        return None


def demonstrate_rag_flow():
    """演示 RAG 工作流程"""
    print("\n" + "=" * 60)
    print("RAG 工作流程演示")
    print("=" * 60)

    # 模拟 RAG 流程
    print("""
【步骤 1: 文档准备】
原始文档:
  1. "贵州茅台 2024 年 Q1 营收同比增长 18%"
  2. "白酒行业集中度提升，龙头受益"
  3. "宁德时代市占率超过 30%"
                    ↓
文本分块 → Embedding 向量化 → 存入向量数据库

【步骤 2: 用户查询】
问题："茅台 2024 年业绩如何？"
                    ↓
问题向量化 → 相似度搜索 → 找到相关文档

【步骤 3: 检索结果】
检索到的文档:
  - "贵州茅台 2024 年 Q1 营收同比增长 18%" (相似度 0.92)
  - "白酒行业集中度提升，龙头受益" (相似度 0.75)

【步骤 4: LLM 生成答案】
Prompt:
  上下文: {检索到的文档}
  问题：茅台 2024 年业绩如何？

LLM 回答:
  "根据研报数据，贵州茅台 2024 年 Q1 营收同比增长 18%..."
""")


def create_rag_chain_demo(vectorstore):
    """创建 RAG 链演示"""
    print("\n" + "=" * 60)
    print("创建 RAG 链")
    print("=" * 60)

    if not vectorstore:
        print("⚠️  使用模拟模式演示")

        # 模拟 RAG 回答
        demo_qa = {
            "茅台 2024 年业绩如何？": "【模拟 RAG 回答】根据检索到的研报，贵州茅台 2024 年 Q1 营收同比增长 18%，净利润增长 20%。来源：茅台研报",
            "白酒行业有什么投资机会？": "【模拟 RAG 回答】根据行业报告，白酒行业集中度持续提升，龙头企业受益。推荐关注茅五泸等龙头企业。来源：白酒行业报告",
            "宁德时代的竞争优势？": "【模拟 RAG 回答】宁德时代是全球动力电池龙头，市占率超过 30%，技术创新持续。来源：新能源研报",
        }

        for question, answer in demo_qa.items():
            print(f"\n问题：{question}")
            print(f"答案：{answer}")

        return

    # 真实 RAG 链
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    llm = create_llm(temperature=0.3)

    system_prompt = """请根据以下上下文回答问题。

上下文：
{context}

问题：{input}

如果上下文中没有答案，请说明。
请用中文回答。"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    combine_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, combine_chain)

    # 测试
    questions = [
        "茅台 2024 年业绩如何？",
        "白酒行业有什么投资机会？",
    ]

    for question in questions:
        print(f"\n问题：{question}")
        response = rag_chain.invoke({"input": question})
        print(f"答案：{response['answer'][:300]}...")
        print(f"引用文档：{len(response['context'])} 篇")


def analyze_use_cases():
    """分析 RAG 应用场景"""
    print("\n" + "=" * 60)
    print("RAG 应用场景分析")
    print("=" * 60)

    use_cases = [
        {
            "场景": "企业知识库问答",
            "数据源": "内部文档、Wiki、手册",
            "典型问题": "公司的报销流程是什么？",
            "优势": "答案准确、可追溯"
        },
        {
            "场景": "客服系统",
            "数据源": "产品文档、FAQ、工单",
            "典型问题": "这个产品怎么用？",
            "优势": "减少人工客服压力"
        },
        {
            "场景": "研报检索",
            "数据源": "研究报告、行业分析",
            "典型问题": "茅台的投资价值如何？",
            "优势": "基于最新研报分析"
        },
        {
            "场景": "法律咨询",
            "数据源": "法条、案例、合同模板",
            "典型问题": "这种情况怎么维权？",
            "优势": "答案有法律依据"
        },
    ]

    for i, uc in enumerate(use_cases, 1):
        print(f"\n{i}. {uc['场景']}")
        print(f"   数据源：{uc['数据源']}")
        print(f"   典型问题：{uc['典型问题']}")
        print(f"   优势：{uc['优势']}")


def main():
    """主函数"""
    print("=" * 60)
    print("Day 50: RAG 原理")
    print("=" * 60)

    # 对比 LLM vs RAG
    compare_llm_vs_rag()

    # 演示 RAG 流程
    demonstrate_rag_flow()

    # 创建 VectorStore
    vectorstore = create_mock_vectorstore()

    # 创建 RAG 链
    create_rag_chain_demo(vectorstore)

    # 分析应用场景
    analyze_use_cases()

    print("\n" + "=" * 60)
    print("✅ Day 50 学习完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
