"""
Day 52: RAG 完整流程

学习目标:
- 掌握 Retriever 配置
- 理解相关性排序
- 学会上下文组装
- 实现完整 RAG 流程
"""

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
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


def create_test_documents():
    """创建测试文档"""
    return [
        Document(
            page_content="贵州茅台（600519）是白酒龙头企业，2024 年 Q1 营收 350 亿元，同比增长 18%。公司品牌护城河深厚，直销渠道占比持续提升。当前 PE 约 30 倍，处于历史合理区间。",
            metadata={"source": "茅台研报", "stock_code": "600519"}
        ),
        Document(
            page_content="五粮液（000858）是浓香型白酒代表，第八代五粮液稳价放量。2024 年预计营收增速 15%，净利润增速 18%。当前 PE 约 25 倍，低于茅台。",
            metadata={"source": "五粮液研报", "stock_code": "000858"}
        ),
        Document(
            page_content="白酒行业集中度持续提升，龙头企业受益。高端酒需求稳定，次高端竞争加剧。推荐关注茅五泸等龙头企业。估值方面，茅台 PE30x，五粮液 PE25x。",
            metadata={"source": "白酒行业报告", "category": "行业"}
        ),
        Document(
            page_content="宁德时代（300750）是全球动力电池龙头，市占率超过 30%。技术创新持续，麒麟电池、钠离子电池量产。储能业务高速增长。",
            metadata={"source": "新能源研报", "stock_code": "300750"}
        ),
    ]


def setup_vectorstore(documents):
    """设置 VectorStore"""
    print("=" * 50)
    print("设置 VectorStore")
    print("=" * 50)

    if not MILVUS_AVAILABLE:
        print("⚠️  pymilvus 未安装，跳过 VectorStore 创建")
        return None

    try:
        connections.connect(host="localhost", port="19530")

        # 分块
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=20
        )
        chunks = splitter.split_documents(documents)
        print(f"分块数：{len(chunks)}")

        # 创建 VectorStore
        embeddings = create_embeddings()

        vectorstore = Milvus.from_documents(
            documents=chunks,
            embedding=embeddings,
            connection_args={"host": "localhost", "port": "19530"},
            collection_name="rag_pipeline_demo",
            drop_old=True
        )

        print("✅ VectorStore 创建成功")
        return vectorstore

    except Exception as e:
        print(f"⚠️  创建失败：{e}")
        return None


def test_retriever_configs(vectorstore):
    """测试不同 Retriever 配置"""
    print("\n" + "=" * 50)
    print("Retriever 配置测试")
    print("=" * 50)

    if not vectorstore:
        print("⚠️  使用模拟模式")
        return

    queries = ["茅台 PE 多少", "白酒行业投资机会"]

    configs = [
        {"k": 1, "name": "Top-1"},
        {"k": 2, "name": "Top-2"},
        {"k": 3, "name": "Top-3"},
    ]

    for config in configs:
        print(f"\n{config['name']} (k={config['k']}):")
        retriever = vectorstore.as_retriever(search_kwargs={"k": config['k']})

        for query in queries:
            docs = retriever.invoke(query)
            print(f"  查询：'{query}' → {len(docs)} 篇文档")


def create_rag_chain(vectorstore):
    """创建 RAG 链"""
    print("\n" + "=" * 50)
    print("创建 RAG 链")
    print("=" * 50)

    if not vectorstore:
        print("⚠️  使用模拟模式")

        # 模拟 RAG 回答
        demo_answers = {
            "茅台 PE 多少": "【模拟】根据研报，茅台当前 PE 约 30 倍，处于历史合理区间。",
            "白酒行业投资机会": "【模拟】白酒行业集中度提升，推荐关注茅五泸等龙头企业。",
            "茅台和五粮液哪个估值低": "【模拟】五粮液 PE 约 25 倍，低于茅台的 30 倍。",
        }

        return demo_answers

    # 真实 RAG 链
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    llm = create_llm(temperature=0.3)

    # 基础 Prompt
    system_prompt = """请根据以下上下文回答问题。

上下文：
{context}

问题：{input}

请用中文专业但易懂的语言回答。"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    combine_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, combine_chain)

    return rag_chain


def test_rag_chain(rag_chain):
    """测试 RAG 链"""
    print("\n" + "=" * 50)
    print("RAG 链测试")
    print("=" * 50)

    questions = [
        "茅台 PE 多少？",
        "白酒行业有什么投资机会？",
        "茅台和五粮液哪个估值低？",
    ]

    for question in questions:
        print(f"\n问题：{question}")

        if isinstance(rag_chain, dict):
            # 模拟模式
            answer = rag_chain.get(question, "未知")
            print(f"答案：{answer}")
        else:
            # 真实 RAG
            response = rag_chain.invoke({"input": question})
            print(f"答案：{response['answer'][:300]}...")
            print(f"引用文档：{len(response['context'])} 篇")


def compare_prompts():
    """比较不同 Prompt 效果"""
    print("\n" + "=" * 50)
    print("Prompt 设计对比")
    print("=" * 50)

    prompts = {
        "基础版": """请根据上下文回答问题。
上下文：{context}
问题：{input}""",

        "详细版": """你是股票分析助手。请根据以下上下文回答问题。

上下文：
{context}

问题：{input}

回答要求：
1. 先给出核心结论
2. 引用具体数据
3. 如果信息不足请说明

请用中文回答。""",

        "带格式版": """你是股票分析助手。请根据以下上下文回答问题。

上下文：
{context}

问题：{input}

请按以下格式回答：
【结论】一句话总结
【分析】详细解释
【来源】引用来源

请用中文回答。""",
    }

    for name, template in prompts.items():
        print(f"\n{name}:")
        print(f"  字符数：{len(template)}")
        print(f"  特点：{len(template.split(chr(10)))} 行")


def main():
    """主函数"""
    print("=" * 60)
    print("Day 52: RAG 完整流程")
    print("=" * 60)

    # 创建测试文档
    documents = create_test_documents()
    print(f"\n创建 {len(documents)} 篇测试文档")

    # 设置 VectorStore
    vectorstore = setup_vectorstore(documents)

    # 测试 Retriever 配置
    test_retriever_configs(vectorstore)

    # 创建 RAG 链
    rag_chain = create_rag_chain(vectorstore)

    # 测试 RAG 链
    test_rag_chain(rag_chain)

    # 比较 Prompt
    compare_prompts()

    print("\n" + "=" * 60)
    print("✅ Day 52 学习完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
