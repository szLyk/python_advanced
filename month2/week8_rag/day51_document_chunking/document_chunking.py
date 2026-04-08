"""
Day 51: 文档加载和分块

学习目标:
- 掌握 DocumentLoader 类型
- 学会 PDF/Text/HTML 加载
- 理解文本分块策略
- 了解元数据管理
"""

from langchain.schema import Document
from langchain.document_loaders import (
    TextLoader,
    DirectoryLoader,
)
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    ChineseTextSplitter
)
import os


# ==================== 文档加载 ====================

def create_sample_files():
    """创建示例文件"""
    print("=" * 50)
    print("创建示例文件")
    print("=" * 50)

    # 创建 data 目录
    data_dir = "data/sample_docs"
    os.makedirs(data_dir, exist_ok=True)

    # 创建示例文档
    sample_docs = {
        "stock_news_1.txt": """
贵州茅台发布 2024 年 Q1 财报

贵州茅台（600519）发布 2024 年第一季度财报。
财报显示，公司 Q1 实现营收 350 亿元，同比增长 18%。
净利润 180 亿元，同比增长 20%。

分析师认为，茅台作为高端白酒龙头，
品牌护城河深厚，直销渠道占比持续提升。
""",
        "stock_news_2.txt": """
五粮液新品发布会

五粮液（000858）在成都举办新品发布会。
第八代五粮液正式上市，建议零售价 1199 元。
公司表示，新品将进一步巩固高端市场地位。

系列酒也将推出多款新产品，
满足不同消费场景需求。
""",
        "industry_report.txt": """
白酒行业 2024 年投资策略

行业观点：
1. 白酒行业集中度持续提升
2. 高端酒需求稳定，次高端竞争加剧
3. 龙头企业受益于消费升级

估值分析：
- 茅台 PE(TTM): 30x
- 五粮液 PE(TTM): 25x
- 泸州老窖 PE(TTM): 22x

推荐关注茅五泸等龙头企业。
""",
    }

    for filename, content in sample_docs.items():
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 创建文件：{filepath}")

    return data_dir


def load_single_file(filepath):
    """加载单个文件"""
    print(f"\n加载文件：{filepath}")

    try:
        loader = TextLoader(filepath, encoding='utf-8')
        documents = loader.load()

        print(f"✅ 加载成功")
        print(f"   文档数：{len(documents)}")
        print(f"   内容长度：{len(documents[0].page_content)} 字符")
        print(f"   元数据：{documents[0].metadata}")

        return documents

    except Exception as e:
        print(f"❌ 加载失败：{e}")
        return []


def load_directory(dir_path):
    """加载目录下所有文件"""
    print(f"\n加载目录：{dir_path}")

    try:
        loader = DirectoryLoader(
            dir_path,
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        )

        documents = loader.load()

        print(f"✅ 加载成功")
        print(f"   文档数：{len(documents)}")

        return documents

    except Exception as e:
        print(f"❌ 加载失败：{e}")
        return []


# ==================== 文本分块 ====================

def demo_text_splitters(documents):
    """演示不同分块器"""
    print("\n" + "=" * 50)
    print("文本分块器对比")
    print("=" * 50)

    text = documents[0].page_content if documents else ""

    if not text:
        print("⚠️  无文本内容")
        return

    # 方法 1: CharacterTextSplitter
    print("\n1. CharacterTextSplitter (字符分块)")
    splitter1 = CharacterTextSplitter(
        separator="\n",
        chunk_size=100,
        chunk_overlap=10
    )
    chunks1 = splitter1.split_text(text)
    print(f"   分块数：{len(chunks1)}")
    print(f"   第一块：{chunks1[0][:80]}...")

    # 方法 2: RecursiveCharacterTextSplitter (推荐)
    print("\n2. RecursiveCharacterTextSplitter (递归字符分块)")
    splitter2 = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", "！", "？", " "],
        chunk_size=100,
        chunk_overlap=10
    )
    chunks2 = splitter2.split_text(text)
    print(f"   分块数：{len(chunks2)}")
    print(f"   第一块：{chunks2[0][:80]}...")

    # 方法 3: 中文专用
    print("\n3. ChineseTextSplitter (中文分块)")
    # 注意：ChineseTextSplitter 需要 jieba 支持
    try:
        splitter3 = ChineseTextSplitter(
            chunk_size=100,
            chunk_overlap=10
        )
        chunks3 = splitter3.split_text(text)
        print(f"   分块数：{len(chunks3)}")
        print(f"   第一块：{chunks3[0][:80]}...")
    except Exception as e:
        print(f"   ⚠️  需要 jieba 支持：{e}")


def demo_chunking_strategies():
    """演示不同分块策略"""
    print("\n" + "=" * 50)
    print("分块策略对比")
    print("=" * 50)

    # 创建长文本
    text = "贵州茅台是白酒龙头企业。" * 50

    configs = [
        {"chunk_size": 50, "chunk_overlap": 5},
        {"chunk_size": 100, "chunk_overlap": 10},
        {"chunk_size": 200, "chunk_overlap": 20},
    ]

    for config in configs:
        splitter = RecursiveCharacterTextSplitter(**config)
        chunks = splitter.split_text(text)
        print(f"\nchunk_size={config['chunk_size']}, overlap={config['chunk_overlap']}")
        print(f"   分块数：{len(chunks)}")
        print(f"   平均每块长度：{sum(len(c) for c in chunks) / len(chunks):.1f}")


def demo_metadata_management():
    """演示元数据管理"""
    print("\n" + "=" * 50)
    print("元数据管理")
    print("=" * 50)

    # 创建带元数据的文档
    documents = [
        Document(
            page_content="贵州茅台是白酒龙头",
            metadata={"source": "report.pdf", "stock_code": "600519", "year": 2024}
        ),
        Document(
            page_content="五粮液是浓香白酒代表",
            metadata={"source": "report.pdf", "stock_code": "000858", "year": 2024}
        ),
    ]

    # 分块后保留元数据
    splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=5)
    chunks = splitter.split_documents(documents)

    print("\n分块后元数据:")
    for i, chunk in enumerate(chunks):
        print(f"  [{i}] {chunk.metadata}")


def main():
    """主函数"""
    print("=" * 60)
    print("Day 51: 文档加载和分块")
    print("=" * 60)

    # 创建示例文件
    data_dir = create_sample_files()

    # 加载单个文件
    docs = load_single_file(os.path.join(data_dir, "stock_news_1.txt"))

    # 加载目录
    all_docs = load_directory(data_dir)

    # 演示分块器
    demo_text_splitters(all_docs if all_docs else docs)

    # 演示分块策略
    demo_chunking_strategies()

    # 演示元数据管理
    demo_metadata_management()

    print("\n" + "=" * 60)
    print("✅ Day 51 学习完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
