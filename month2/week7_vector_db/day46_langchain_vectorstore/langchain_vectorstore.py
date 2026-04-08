"""
Day 46: LangChain 集成

学习目标:
- 掌握 LangChain VectorStore 接口
- 学会 Milvus 向量存储
- 实现相似度搜索链
- 了解文档检索流程
"""

from langchain.schema import Document
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


def get_embeddings():
    """获取 Embedding 模型"""
    return create_embeddings()


def connect_milvus():
    """连接 Milvus"""
    try:
        connections.connect(host="localhost", port="19530", timeout=5)
        print("✅ Milvus 连接成功")
        return True
    except Exception as e:
        print(f"❌ Milvus 连接失败：{e}")
        return None


def vectorstore_from_documents():
    """从文档创建 VectorStore"""
    print("=" * 50)
    print("从文档创建 VectorStore")
    print("=" * 50)

    if not connect_milvus():
        return None

    # 准备文档
    documents = [
        Document(
            page_content="贵州茅台是白酒龙头企业，成立于 1999 年，主营高端白酒生产",
            metadata={"stock_code": "600519", "category": "白酒", "year": 2024}
        ),
        Document(
            page_content="五粮液是浓香型白酒的代表产品，产自四川宜宾",
            metadata={"stock_code": "000858", "category": "白酒", "year": 2024}
        ),
        Document(
            page_content="宁德时代是全球动力电池龙头企业，市占率超过 30%",
            metadata={"stock_code": "300750", "category": "新能源", "year": 2024}
        ),
    ]

    embeddings = get_embeddings()

    try:
        # 创建 VectorStore
        vectorstore = Milvus.from_documents(
            documents=documents,
            embedding=embeddings,
            connection_args={"host": "localhost", "port": "19530"},
            collection_name="langchain_demo",
            drop_old=True  # 如果已存在则删除重建
        )

        print(f"✅ VectorStore 创建成功")
        print(f"   Collection: langchain_demo")
        print(f"   文档数量：{len(documents)}")

        return vectorstore

    except Exception as e:
        print(f"❌ 错误：{e}")
        return None


def similarity_search(vectorstore):
    """相似度搜索"""
    print("\n" + "=" * 50)
    print("相似度搜索")
    print("=" * 50)

    if not vectorstore:
        return

    # 测试查询
    queries = [
        "白酒股票",
        "新能源",
        "茅台相关",
    ]

    for query in queries:
        print(f"\n查询：'{query}'")
        results = vectorstore.similarity_search(query, k=2)

        for doc in results:
            code = doc.metadata.get("stock_code", "未知")
            content = doc.page_content[:50] + "..."
            print(f"  [{code}] {content}")


def retriever_demo(vectorstore):
    """Retriever 演示"""
    print("\n" + "=" * 50)
    print("Retriever 演示")
    print("=" * 50)

    if not vectorstore:
        return

    # 创建 Retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 2}
    )

    # 测试检索
    query = "白酒行业有哪些公司？"
    print(f"\n检索：'{query}'")

    docs = retriever.invoke(query)

    print(f"\n检索到 {len(docs)} 篇文档:")
    for i, doc in enumerate(docs, 1):
        print(f"  [{i}] {doc.page_content[:60]}...")


def rag_chain_demo(vectorstore):
    """RAG 链演示"""
    print("\n" + "=" * 50)
    print("RAG 链演示")
    print("=" * 50)

    if not vectorstore:
        return

    # 创建 Retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    # LLM
    llm = create_llm(temperature=0.3)

    # Prompt
    system_prompt = """你是股票知识助手。请根据以下上下文回答问题。

上下文：
{context}

问题：{input}

如果上下文中没有答案，请直接说明。
请用中文回答。"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    # 创建 RAG 链
    combine_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, combine_chain)

    # 测试
    questions = [
        "白酒行业有哪些公司？",
        "茅台是做什么的？",
        "新能源行业有什么龙头？",
    ]

    for question in questions:
        print(f"\n问题：{question}")
        response = rag_chain.invoke({"input": question})
        print(f"答案：{response['answer'][:200]}...")


def main():
    """主函数"""
    print("=" * 60)
    print("Day 46: LangChain 集成")
    print("=" * 60)

    if not MILVUS_AVAILABLE:
        print("\n❌ pymilvus 未安装")
        return

    # 创建 VectorStore
    vectorstore = vectorstore_from_documents()

    if vectorstore:
        # 相似度搜索
        similarity_search(vectorstore)

        # Retriever 演示
        retriever_demo(vectorstore)

        # RAG 链演示
        rag_chain_demo(vectorstore)

    print("\n" + "=" * 60)
    print("✅ Day 46 学习完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
