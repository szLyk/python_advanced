# Day 22: LLM 基础

## 学习目标

理解大语言模型（LLM）的核心原理，为后续 AI Agent 开发打下理论基础。

## 知识点

### 1. LLM 发展历程

```
2017: Transformer 论文（Google）
      ↓
2018: BERT / GPT-1
      ↓
2019: GPT-2
      ↓
2020: GPT-3 (175B 参数)
      ↓
2022: ChatGPT 发布
      ↓
2023: GPT-4 / Claude / LLaMA
      ↓
2024: Claude 3 / GPT-4o / DeepSeek
```

### 2. Transformer 架构

Transformer 是现代 LLM 的基础架构：

```
输入文本
    ↓
Tokenization（分词）
    ↓
Embedding（词嵌入）
    ↓
位置编码（Positional Encoding）
    ↓
┌─────────────────────────┐
│   Encoder（编码器）       │  ← 理解输入
│   - Self-Attention      │
│   - Multi-Head Attention│
│   - Layer Normalization │
│   - Feed Forward        │
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│   Decoder（解码器）       │  ← 生成输出
│   - Masked Attention    │
│   - Cross Attention     │
│   - Feed Forward        │
└─────────────────────────┘
    ↓
Softmax → 输出 Token
```

### 3. Attention 机制

Attention 是 Transformer 的核心：

```python
# Attention 公式（简化理解）
Attention(Q, K, V) = softmax(Q · K^T / sqrt(d_k)) · V

# 其中：
# Q (Query) = 查询向量 - "我想找什么"
# K (Key)   = 键向量   - "这里有什么"
# V (Value) = 值向量   - "实际内容是什么"

# 通俗理解：
# 在阅读句子时，每个词都在"询问"其他词的重要性
# 比如 "银行" 会更关注 "钱"、"存"、"取" 等词
```

### 4. Self-Attention 示例

```python
import numpy as np

def self_attention(Q, K, V):
    """
    简化的 Self-Attention 计算

    Q: 查询矩阵 (seq_len, d_model)
    K: 键矩阵 (seq_len, d_model)
    V: 值矩阵 (seq_len, d_model)
    """
    d_k = Q.shape[-1]

    # 计算注意力分数
    scores = np.dot(Q, K.T) / np.sqrt(d_k)

    # Softmax 归一化
    attention_weights = np.exp(scores) / np.sum(np.exp(scores), axis=-1, keepdims=True)

    #加权求和
    output = np.dot(attention_weights, V)

    return output, attention_weights

# 示例：句子 "我爱编程"
# 每个词有对应的 Q、K、V 向量
seq_len = 4
d_model = 8

Q = np.random.randn(seq_len, d_model)
K = np.random.randn(seq_len, d_model)
V = np.random.randn(seq_len, d_model)

output, weights = self_attention(Q, K, V)
print(f"注意力权重矩阵形状: {weights.shape}")  # (4, 4)
print(f"输出形状: {output.shape}")  # (4, 8)
```

### 5. Multi-Head Attention

```python
# Multi-Head Attention = 多个独立的 Attention 头并行计算
# 每个头关注不同的语义信息

class MultiHeadAttention:
    def __init__(self, num_heads=8, d_model=512):
        self.num_heads = num_heads
        self.d_model = d_model
        self.d_k = d_model // num_heads  # 每个头的维度

    def forward(self, Q, K, V):
        # 分割成多个头
        # 每个头独立计算 attention
        # 最后拼接所有头的输出

        heads = []
        for i in range(self.num_heads):
            q_i = Q[:, i*self.d_k:(i+1)*self.d_k]
            k_i = K[:, i*self.d_k:(i+1)*self.d_k]
            v_i = V[:, i*self.d_k:(i+1)*self.d_k]

            head_output = self_attention(q_i, k_i, v_i)
            heads.append(head_output)

        # 拼接所有头
        concat = np.concatenate(heads, axis=-1)
        return concat
```

### 6. GPT vs BERT

| 特性 | GPT | BERT |
|------|-----|------|
| 方向 | 单向（从左到右）| 双向 |
| 架构 | Decoder-only | Encoder-only |
| 任务 | 文本生成 | 文本理解 |
| 训练 | 预测下一个词 | 预测被遮蔽的词 |
| 应用 | ChatGPT、对话 | 分类、搜索 |

### 7. LLM 关键概念

```python
# Token（词元）
# 文本被分割成最小的处理单元
text = "我爱编程"
tokens = ["我", "爱", "编", "程"]  # 中文通常按字分词

# Token ID
# 每个 token 对应一个唯一数字
token_ids = [101, 234, 567, 890]

# Context Window（上下文窗口）
# 模型能处理的最大 token 数量
# GPT-4: 128K tokens
# Claude 3: 200K tokens

# Temperature（温度参数）
# 控制输出的随机性
# temperature=0: 最确定性输出
# temperature=1: 较随机
# temperature=2: 非常随机

# Top-K / Top-P（采样策略）
# top_k=50: 只从概率最高的50个词中选择
# top_p=0.9: 从累计概率达90%的词中选择
```

### 8. Prompt 工程基础

```python
# Prompt 结构
prompt = """
[系统指令]
你是一个股票分析助手，帮助用户分析股票数据。

[用户输入]
请分析 AAPL 的股票走势。

[输出格式]
请以结构化 JSON 格式返回分析结果。
"""

# Prompt 设计技巧
# 1. 明确角色定义
# 2. 提供具体任务描述
# 3. 指定输出格式
# 4. 给出示例（Few-shot）
# 5. 分步骤引导
```

### 9. LLM 应用场景

```
1. 文本生成
   - 写作、翻译、摘要

2. 问答系统
   - 知识问答、客服

3. 代码生成
   - 写代码、调试、解释

4. 数据分析
   - 报告生成、趋势分析

5. Agent 系统
   - 自主决策、工具调用
```

## 练习任务

1. 理解 Transformer 架构图
2. 手动计算简单的 Attention 权重
3. 理解 GPT 和 BERT 的区别
4. 编写简单的 Prompt 示例
5. 了解常用 LLM 模型的特点

## 股票场景思考

```
LLM 在股票分析中的应用：

1. 新闻摘要
   - 输入：多条财经新闻
   - 输出：关键信息摘要

2. 情绪分析
   - 输入：新闻标题
   - 输出：正面/负面/中性情绪

3. 报告生成
   - 输入：股票数据
   - 输出：分析报告文本

4. 智能问答
   - 输入："AAPL最近表现如何？"
   - 输出：基于数据的回答
```

## 参考资料

- Transformer 论文：Attention Is All You Need (2017)
- B 站：Transformer 详解视频
- Jay Alammar 博客：The Illustrated Transformer
- OpenAI 文档：https://platform.openai.com/docs