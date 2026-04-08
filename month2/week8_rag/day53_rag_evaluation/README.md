# Day 53: RAG 效果评估

> **日期**: 2026-05-25（周日）  
> **周次**: Week 8 - RAG 系统  
> **预计耗时**: 2 小时

---

## 今日学习目标

- [ ] 了解 RAG 评估指标
- [ ] 学会准确率测试方法
- [ ] 掌握召回率评估
- [ ] 实现端到端评估流程

---

## 学习内容

### 1. RAG 评估指标

| 指标 | 说明 | 计算方法 |
|------|------|----------|
| **准确率 (Precision)** | 返回结果中有多少是相关的 | 相关结果数 / 返回结果数 |
| **召回率 (Recall)** | 所有相关结果中有多少被返回 | 返回的相关结果数 / 总相关结果数 |
| **命中率 (Hit Rate)** | Top-K 中至少有一个相关的比例 | 命中次数 / 总查询数 |
| **答案准确率** | 生成的答案是否正确 | 人工评估或 LLM 评估 |

### 2. 构建测试集

```python
# 测试集示例
test_set = [
    {
        "question": "贵州茅台的市盈率是多少？",
        "expected_answer": "约 30 倍",
        "relevant_docs": ["茅台估值分析.pdf"]
    },
    {
        "question": "白酒行业 2024 年发展趋势如何？",
        "expected_answer": "高端化、集中化、国际化",
        "relevant_docs": ["白酒行业报告.pdf"]
    },
    # ... 更多测试用例
]
```

### 3. 检索质量评估

```python
def evaluate_retrieval(retriever, test_set):
    """评估检索质量"""
    hit_rate = 0
    precision_scores = []
    
    for test_case in test_set:
        query = test_case["question"]
        expected_docs = test_case["relevant_docs"]
        
        # 执行检索
        docs = retriever.invoke(query)
        retrieved_sources = [d.metadata.get("source") for d in docs]
        
        # 计算命中率
        if any(src in retrieved_sources for src in expected_docs):
            hit_rate += 1
        
        # 计算准确率
        relevant_count = sum(1 for src in retrieved_sources if src in expected_docs)
        precision = relevant_count / len(retrieved_sources) if retrieved_sources else 0
        precision_scores.append(precision)
    
    return {
        "hit_rate": hit_rate / len(test_set),
        "avg_precision": sum(precision_scores) / len(precision_scores)
    }
```

### 4. 答案质量评估（使用 LLM）

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-3.5-turbo")

# 评估 Prompt
eval_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是 RAG 系统评估员。请评估以下答案的质量。

标准答案：{expected}
实际答案：{actual}

请从以下维度评分（0-10 分）：
1. 准确性：答案是否与标准答案一致
2. 完整性：是否涵盖了关键信息
3. 相关性：是否回答了问题

输出格式：
准确性：X/10
完整性：X/10
相关性：X/10
总分：X/10

简要评价：..."""),
])

eval_chain = eval_prompt | llm

# 评估
result = eval_chain.invoke({
    "expected": "约 30 倍",
    "actual": "茅台的市盈率约为 30.5 倍"
})
print(result.content)
```

### 5. 端到端评估流程

```python
def evaluate_rag_system(rag_chain, test_set):
    """完整的 RAG 评估流程"""
    results = []
    
    for test_case in test_set:
        # 执行 RAG
        response = rag_chain.invoke({"input": test_case["question"]})
        
        # LLM 评估
        eval_result = eval_chain.invoke({
            "expected": test_case["expected_answer"],
            "actual": response["answer"]
        })
        
        # 解析评分
        scores = parse_scores(eval_result.content)
        
        results.append({
            "question": test_case["question"],
            "scores": scores,
            "context_count": len(response["context"])
        })
    
    # 汇总统计
    avg_scores = {
        "accuracy": sum(r["scores"]["accuracy"] for r in results) / len(results),
        "completeness": sum(r["scores"]["completeness"] for r in results) / len(results),
        "relevance": sum(r["scores"]["relevance"] for r in results) / len(results),
    }
    
    return avg_scores, results
```

---

## 实践任务

### 任务 1: 构建测试集 ✅

```python
# rag_evaluation.py

# 创建至少 10 个测试用例
test_set = [
    {"question": "...", "expected_answer": "...", "relevant_docs": [...]},
    # ...
]
```

### 任务 2: 实现评估函数 ✅

```python
# 实现检索质量评估和答案质量评估
# 运行评估并输出报告
```

### 任务 3: 生成评估报告 ✅

```python
# evaluation_report.md

# RAG 系统评估报告

## 测试集概览
- 问题数量：20
- 覆盖主题：白酒、新能源、金融...

## 检索质量
- 命中率：85%
- 平均准确率：78%

## 答案质量
- 准确性：8.2/10
- 完整性：7.5/10
- 相关性：9.0/10

## 改进建议
1. ...
2. ...
```

---

## 知识点总结

### 评估维度

| 维度 | 评估内容 | 方法 |
|------|----------|------|
| 检索 | 找到相关文档 | 命中率、准确率 |
| 生成 | 答案质量 | LLM 评估、人工评估 |
| 端到端 | 整体效果 | 用户满意度 |

### 评估流程

1. 构建测试集
2. 运行系统
3. 收集结果
4. 计算指标
5. 生成报告
6. 持续优化

---

## 常见问题

### Q1: 如何获取标准答案？
- 领域专家编写
- 从文档中提取
- LLM 生成后人工审核

### Q2: 评估太主观？
- 使用多个评估者
- 制定明确的评分标准
- 使用自动化评估工具

### Q3: 评估成本太高？
- 抽样评估（20-50 个问题）
- 使用小规模测试集迭代
- 自动化评估流程

---

## 代码文件

```
day53_rag_evaluation/
├── README.md
├── rag_evaluation.py          # 评估主程序
├── test_set.py                # 测试集定义
├── eval_prompt.py             # 评估 Prompt
└── evaluation_report.md       # 评估报告模板
```

---

## 参考资源

- [RAGAS 评估框架](https://docs.ragas.io/)
- [LangChain 评估指南](https://python.langchain.com/docs/guides/evaluation)

---

## 下一步

- **Day 54**: 复习/补进度
- **Day 55**: 综合项目 - 股票知识库 RAG 系统

---

**💡 今日格言**: "没有评估就没有优化"
