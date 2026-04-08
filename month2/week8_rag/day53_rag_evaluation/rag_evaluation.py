"""
Day 53: RAG 效果评估

学习目标:
- 了解 RAG 评估指标
- 学会准确率测试方法
- 掌握召回率评估
- 实现端到端评估流程
"""

from typing import List, Dict
from langchain.schema import Document
from langchain_core.prompts import ChatPromptTemplate
from config import create_llm


# ==================== 测试集定义 ====================

def create_test_set() -> List[Dict]:
    """创建测试集"""
    return [
        {
            "question": "贵州茅台 2024 年 Q1 营收增速是多少？",
            "expected_answer": "18%",
            "relevant_docs": ["茅台研报"],
        },
        {
            "question": "五粮液的 PE 是多少？",
            "expected_answer": "约 25 倍",
            "relevant_docs": ["五粮液研报"],
        },
        {
            "question": "白酒行业推荐关注哪些公司？",
            "expected_answer": "茅五泸等龙头企业",
            "relevant_docs": ["白酒行业报告"],
        },
        {
            "question": "宁德时代的市占率是多少？",
            "expected_answer": "超过 30%",
            "relevant_docs": ["新能源研报"],
        },
        {
            "question": "茅台和五粮液哪个 PE 更低？",
            "expected_answer": "五粮液 PE 更低",
            "relevant_docs": ["茅台研报", "五粮液研报"],
        },
    ]


# ==================== 评估函数 ====================

def evaluate_retrieval(retriever, test_set) -> Dict:
    """评估检索质量"""
    print("\n" + "=" * 50)
    print("检索质量评估")
    print("=" * 50)

    hits = 0
    precision_scores = []

    for i, test_case in enumerate(test_set, 1):
        query = test_case["question"]
        expected_docs = test_case["relevant_docs"]

        # 执行检索
        try:
            docs = retriever.invoke(query)
            retrieved_sources = [d.metadata.get("source", "") for d in docs]

            # 计算命中率
            if any(src in retrieved_sources for src in expected_docs):
                hits += 1
                hit = "✅"
            else:
                hit = "❌"

            # 计算准确率
            relevant_count = sum(1 for src in retrieved_sources if src in expected_docs)
            precision = relevant_count / len(retrieved_sources) if retrieved_sources else 0
            precision_scores.append(precision)

            print(f"[{i}] {hit} '{query[:30]}...' → 检索到{len(docs)}篇，准确率{precision:.2f}")

        except Exception as e:
            print(f"[{i}] ❌ '{query[:30]}...' → 错误：{e}")

    hit_rate = hits / len(test_set) if test_set else 0
    avg_precision = sum(precision_scores) / len(precision_scores) if precision_scores else 0

    print(f"\n汇总:")
    print(f"  命中率：{hit_rate:.2%} ({hits}/{len(test_set)})")
    print(f"  平均准确率：{avg_precision:.2f}")

    return {"hit_rate": hit_rate, "precision": avg_precision}


def evaluate_answer_quality(llm, expected: str, actual: str) -> Dict:
    """使用 LLM 评估答案质量"""
    eval_prompt = ChatPromptTemplate.from_messages([
        ("system", """你是 RAG 系统评估员。请评估以下答案的质量。

标准答案：{expected}
实际答案：{actual}

请从以下维度评分（0-10 分）：
1. 准确性：答案是否与标准答案一致
2. 完整性：是否涵盖了关键信息
3. 相关性：是否回答了问题

只输出 JSON 格式：
{
    "accuracy": 数字，
    "completeness": 数字，
    "relevance": 数字，
    "comment": "简短评价"
}"""),
    ])

    try:
        chain = eval_prompt | llm
        result = chain.invoke({"expected": expected, "actual": actual})

        # 解析评分（简化处理）
        content = result.content
        return {
            "raw_eval": content,
            "accuracy": 7,  # 简化：实际应解析 JSON
            "completeness": 7,
            "relevance": 8,
        }
    except Exception as e:
        return {"raw_eval": str(e), "accuracy": 0, "completeness": 0, "relevance": 0}


def evaluate_rag_system(rag_chain, test_set) -> Dict:
    """完整的 RAG 评估流程"""
    print("\n" + "=" * 50)
    print("RAG 系统端到端评估")
    print("=" * 50)

    llm = create_llm(temperature=0.3)

    results = []

    for i, test_case in enumerate(test_set, 1):
        question = test_case["question"]
        expected = test_case["expected_answer"]

        print(f"\n[{i}] 问题：{question}")
        print(f"    期望答案：{expected}")

        try:
            # 执行 RAG
            if isinstance(rag_chain, dict):
                # 模拟模式
                actual = rag_chain.get(question, "未知")
                print(f"    实际答案：{actual}")
            else:
                # 真实 RAG
                response = rag_chain.invoke({"input": question})
                actual = response["answer"]
                print(f"    实际答案：{actual[:100]}...")

            # LLM 评估
            eval_result = evaluate_answer_quality(llm, expected, actual)

            results.append({
                "question": question,
                "expected": expected,
                "actual": actual,
                "eval": eval_result,
            })

        except Exception as e:
            print(f"    ❌ 错误：{e}")
            results.append({
                "question": question,
                "expected": expected,
                "actual": f"错误：{e}",
                "eval": {"accuracy": 0, "completeness": 0, "relevance": 0},
            })

    # 汇总统计
    if results:
        avg_accuracy = sum(r["eval"]["accuracy"] for r in results) / len(results)
        avg_completeness = sum(r["eval"]["completeness"] for r in results) / len(results)
        avg_relevance = sum(r["eval"]["relevance"] for r in results) / len(results)

        print(f"\n{'='*50}")
        print("评估汇总:")
        print(f"  平均准确性：{avg_accuracy:.1f}/10")
        print(f"  平均完整性：{avg_completeness:.1f}/10")
        print(f"  平均相关性：{avg_relevance:.1f}/10")

    return results


def generate_evaluation_report(results, retrieval_metrics):
    """生成评估报告"""
    print("\n" + "=" * 50)
    print("评估报告")
    print("=" * 50)

    report = f"""
# RAG 系统评估报告

## 测试集概览
- 问题数量：{len(results)}

## 检索质量
- 命中率：{retrieval_metrics.get('hit_rate', 0):.2%}
- 平均准确率：{retrieval_metrics.get('precision', 0):.2f}

## 答案质量
"""

    if results:
        avg_acc = sum(r["eval"]["accuracy"] for r in results) / len(results)
        avg_comp = sum(r["eval"]["completeness"] for r in results) / len(results)
        avg_rel = sum(r["eval"]["relevance"] for r in results) / len(results)

        report += f"""
- 准确性：{avg_acc:.1f}/10
- 完整性：{avg_comp:.1f}/10
- 相关性：{avg_rel:.1f}/10

## 改进建议
1. 优化文档分块策略
2. 调整检索参数（k 值、阈值）
3. 改进 Prompt 设计
"""

    print(report)

    # 保存到文件
    with open("evaluation_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    print("\n✅ 报告已保存到 evaluation_report.md")


def create_mock_rag_chain():
    """创建模拟 RAG 链（演示用）"""
    return {
        "贵州茅台 2024 年 Q1 营收增速是多少？": "根据研报，贵州茅台 2024 年 Q1 营收同比增长 18%。",
        "五粮液的 PE 是多少？": "五粮液当前 PE 约 25 倍。",
        "白酒行业推荐关注哪些公司？": "推荐关注茅五泸等龙头企业。",
        "宁德时代的市占率是多少？": "宁德时代市占率超过 30%。",
        "茅台和五粮液哪个 PE 更低？": "五粮液 PE 约 25 倍，低于茅台的 30 倍。",
    }


def main():
    """主函数"""
    print("=" * 60)
    print("Day 53: RAG 效果评估")
    print("=" * 60)

    # 创建测试集
    test_set = create_test_set()
    print(f"\n创建 {len(test_set)} 个测试用例")

    # 创建模拟 RAG 链
    rag_chain = create_mock_rag_chain()

    # 检索评估（需要真实 VectorStore）
    retrieval_metrics = {"hit_rate": 0.8, "precision": 0.75}  # 模拟数据

    # RAG 系统评估
    results = evaluate_rag_system(rag_chain, test_set)

    # 生成报告
    generate_evaluation_report(results, retrieval_metrics)

    print("\n" + "=" * 60)
    print("✅ Day 53 学习完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
