"""
Day 22: LLM 基础 - Transformer 与 Attention 机制

学习目标：
1. 理解 Transformer 架构
2. 掌握 Attention 机制原理
3. 了解 GPT/BERT 区别
"""

import numpy as np
from typing import List, Tuple


# ============================================
# 1. Attention 机制实现
# ============================================

def softmax(x: np.ndarray) -> np.ndarray:
    """Softmax 函数"""
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))  # 防止溢出
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)


def scaled_dot_product_attention(
    Q: np.ndarray,
    K: np.ndarray,
    V: np.ndarray,
    mask: np.ndarray = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    缩放点积注意力

    Attention(Q, K, V) = softmax(Q·K^T / sqrt(d_k)) · V

    Args:
        Q: 查询矩阵 (seq_len, d_k)
        K: 键矩阵 (seq_len, d_k)
        V: 值矩阵 (seq_len, d_v)
        mask: 可选的掩码矩阵

    Returns:
        output: 注意力输出
        attention_weights: 注意力权重矩阵
    """
    d_k = Q.shape[-1]

    # 计算注意力分数
    scores = np.dot(Q, K.T) / np.sqrt(d_k)

    # 应用掩码（如果有）
    if mask is not None:
        scores = scores + mask * -1e9  # 掩码位置设为极小值

    # Softmax 归一化
    attention_weights = softmax(scores)

    # 加权求和
    output = np.dot(attention_weights, V)

    return output, attention_weights


# ============================================
# 2. Multi-Head Attention 实现
# ============================================

class MultiHeadAttention:
    """多头注意力机制"""

    def __init__(self, num_heads: int = 8, d_model: int = 512):
        """
        Args:
            num_heads: 头的数量
            d_model: 模型维度
        """
        assert d_model % num_heads == 0, "d_model 必须能被 num_heads 整除"

        self.num_heads = num_heads
        self.d_model = d_model
        self.d_k = d_model // num_heads  # 每个头的维度

        # 初始化权重矩阵（简化版，实际需要可训练参数）
        self.W_Q = np.random.randn(d_model, d_model)
        self.W_K = np.random.randn(d_model, d_model)
        self.W_V = np.random.randn(d_model, d_model)
        self.W_O = np.random.randn(d_model, d_model)  # 输出投影

    def forward(self, x: np.ndarray, mask: np.ndarray = None) -> np.ndarray:
        """
        前向传播

        Args:
            x: 输入矩阵 (seq_len, d_model)
            mask: 可选掩码

        Returns:
            output: 多头注意力输出
        """
        seq_len = x.shape[0]

        # 线性投影
        Q = np.dot(x, self.W_Q)  # (seq_len, d_model)
        K = np.dot(x, self.W_K)
        V = np.dot(x, self.W_V)

        # 分割成多个头
        Q = Q.reshape(seq_len, self.num_heads, self.d_k).transpose(1, 0, 2)
        K = K.reshape(seq_len, self.num_heads, self.d_k).transpose(1, 0, 2)
        V = V.reshape(seq_len, self.num_heads, self.d_k).transpose(1, 0, 2)

        # 每个头计算注意力
        heads_output = []
        heads_weights = []

        for i in range(self.num_heads):
            head_out, head_weights = scaled_dot_product_attention(
                Q[i], K[i], V[i], mask
            )
            heads_output.append(head_out)
            heads_weights.append(head_weights)

        # 拼接所有头
        concat = np.concatenate(heads_output, axis=-1)  # (seq_len, d_model)

        # 输出投影
        output = np.dot(concat, self.W_O)

        return output, heads_weights


# ============================================
# 3. 位置编码
# ============================================

def positional_encoding(seq_len: int, d_model: int) -> np.ndarray:
    """
    位置编码（Positional Encoding）

    PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

    Args:
        seq_len: 序列长度
        d_model: 模型维度

    Returns:
        PE: 位置编码矩阵 (seq_len, d_model)
    """
    position = np.arange(seq_len)[:, np.newaxis]  # (seq_len, 1)
    div_term = np.exp(np.arange(0, d_model, 2) * -np.log(10000) / d_model)

    PE = np.zeros((seq_len, d_model))
    PE[:, 0::2] = np.sin(position * div_term)  # 偶数维度
    PE[:, 1::2] = np.cos(position * div_term)  # 奇数维度

    return PE


# ============================================
# 4. 简化的 Transformer Block
# ============================================

class TransformerBlock:
    """简化的 Transformer Block"""

    def __init__(self, d_model: int = 512, num_heads: int = 8, d_ff: int = 2048):
        self.d_model = d_model

        # Multi-Head Attention
        self.attention = MultiHeadAttention(num_heads, d_model)

        # Feed Forward 网络（简化）
        self.W1 = np.random.randn(d_model, d_ff)
        self.W2 = np.random.randn(d_ff, d_model)

    def layer_norm(self, x: np.ndarray, eps: float = 1e-6) -> np.ndarray:
        """Layer Normalization"""
        mean = np.mean(x, axis=-1, keepdims=True)
        std = np.std(x, axis=-1, keepdims=True)
        return (x - mean) / (std + eps)

    def feed_forward(self, x: np.ndarray) -> np.ndarray:
        """前馈网络"""
        return np.dot(np.maximum(0, np.dot(x, self.W1)), self.W2)  # ReLU

    def forward(self, x: np.ndarray, mask: np.ndarray = None) -> np.ndarray:
        """
        前向传播

        结构：
        x → Attention → Add & Norm → Feed Forward → Add & Norm → output
        """
        # Self-Attention + Add & Norm
        attn_output, _ = self.attention.forward(x, mask)
        x = self.layer_norm(x + attn_output)

        # Feed Forward + Add & Norm
        ff_output = self.feed_forward(x)
        x = self.layer_norm(x + ff_output)

        return x


# ============================================
# 5. Token 模拟
# ============================================

class SimpleTokenizer:
    """简单的分词器示例"""

    def __init__(self, vocab: List[str]):
        self.vocab = vocab
        self.token_to_id = {token: i for i, token in enumerate(vocab)}
        self.id_to_token = {i: token for i, token in enumerate(vocab)}

    def encode(self, text: str) -> List[int]:
        """文本转 Token ID"""
        tokens = []
        for char in text:
            if char in self.token_to_id:
                tokens.append(self.token_to_id[char])
            else:
                tokens.append(self.token_to_id.get("<UNK>", 0))
        return tokens

    def decode(self, token_ids: List[int]) -> str:
        """Token ID 转文本"""
        return "".join([self.id_to_token.get(id, "<UNK>") for id in token_ids])


# ============================================
# 6. 演示代码
# ============================================

def demo_attention():
    """演示 Attention 机制"""
    print("\n=== Attention 机制演示 ===")

    # 模拟一个小序列
    seq_len = 4
    d_k = 8

    # 随机生成 Q, K, V
    np.random.seed(42)
    Q = np.random.randn(seq_len, d_k)
    K = np.random.randn(seq_len, d_k)
    V = np.random.randn(seq_len, d_k)

    # 计算 Attention
    output, weights = scaled_dot_product_attention(Q, K, V)

    print(f"输入形状: Q={Q.shape}, K={K.shape}, V={V.shape}")
    print(f"注意力权重矩阵:\n{weights}")
    print(f"权重矩阵解释: 每行表示一个词对其他词的关注程度")
    print(f"输出形状: {output.shape}")

    # 解释权重矩阵
    print("\n权重矩阵含义（假设句子 '我爱编程'）：")
    for i in range(seq_len):
        print(f"  词{i} 最关注: 词{np.argmax(weights[i])} (权重={weights[i][np.argmax(weights[i])]:.3f})")


def demo_multi_head_attention():
    """演示 Multi-Head Attention"""
    print("\n=== Multi-Head Attention 演示 ===")

    seq_len = 6
    d_model = 64
    num_heads = 8

    np.random.seed(42)
    x = np.random.randn(seq_len, d_model)

    mha = MultiHeadAttention(num_heads, d_model)
    output, heads_weights = mha.forward(x)

    print(f"输入形状: {x.shape}")
    print(f"多头数量: {num_heads}")
    print(f"每个头维度: {d_model // num_heads}")
    print(f"输出形状: {output.shape}")

    # 显示第一个头的注意力权重
    print(f"\n第1个头的注意力权重矩阵:\n{heads_weights[0]}")


def demo_positional_encoding():
    """演示位置编码"""
    print("\n=== 位置编码演示 ===")

    seq_len = 10
    d_model = 16

    PE = positional_encoding(seq_len, d_model)

    print(f"位置编码形状: {PE.shape}")
    print(f"位置0的前8维编码: {PE[0, :8]}")
    print(f"位置1的前8维编码: {PE[1, :8]}")

    # 可视化说明
    print("\n位置编码说明:")
    print("- 不同位置有不同的编码")
    print("- 使用 sin/cos 函数保证平滑性")
    print("- 相近位置的编码相似")


def demo_transformer_block():
    """演示 Transformer Block"""
    print("\n=== Transformer Block 演示 ===")

    seq_len = 8
    d_model = 64

    np.random.seed(42)
    x = np.random.randn(seq_len, d_model)

    block = TransformerBlock(d_model, num_heads=8)
    output = block.forward(x)

    print(f"输入形状: {x.shape}")
    print(f"经过一个 Transformer Block")
    print(f"输出形状: {output.shape}")


def demo_tokenizer():
    """演示分词"""
    print("\n=== Tokenizer 演示 ===")

    # 简单词汇表
    vocab = ["<UNK>", "我", "爱", "编", "程", "股", "票", "分", "析"]

    tokenizer = SimpleTokenizer(vocab)

    text = "我爱编程"
    token_ids = tokenizer.encode(text)
    decoded = tokenizer.decode(token_ids)

    print(f"词汇表: {vocab}")
    print(f"原文: {text}")
    print(f"Token IDs: {token_ids}")
    print(f"解码: {decoded}")

    # 股票相关文本
    text2 = "股票分析"
    print(f"\n原文: {text2}")
    print(f"Token IDs: {tokenizer.encode(text2)}")


def demo_llm_concepts():
    """演示 LLM 关键概念"""
    print("\n=== LLM 关键概念 ===")

    concepts = {
        "Token": "文本最小处理单元，如 '股票' → ['股', '票'] 或 ['股票']",
        "Context Window": "模型能处理的最大 token 数，如 GPT-4 = 128K",
        "Temperature": "控制输出随机性，0=确定性，1=正常，2=随机",
        "Top-K": "从概率最高的K个词中选择",
        "Top-P": "从累计概率达P的词中选择（nucleus sampling）",
        "Prompt": "给模型的输入指令和上下文",
        "Few-shot": "在 prompt 中提供几个示例",
        "Fine-tuning": "在特定数据上继续训练模型"
    }

    for name, desc in concepts.items():
        print(f"{name}: {desc}")


def demo_gpt_vs_bert():
    """对比 GPT 和 BERT"""
    print("\n=== GPT vs BERT 对比 ===")

    comparison = """
    ┌─────────────┬──────────────────┬──────────────────┐
    │    特性     │       GPT        │       BERT       │
    ├─────────────┼──────────────────┼──────────────────┤
    │ 架构        │ Decoder-only     │ Encoder-only     │
    │ 方向        │ 单向(从左到右)   │ 双向             │
    │ 任务        │ 文本生成         │ 文本理解         │
    │ 训练方式    │ 预测下一个词     │ MLM + NSP        │
    │ 代表模型    │ ChatGPT, GPT-4   │ BERT, RoBERTa    │
    │ 应用场景    │ 对话、写作       │ 分类、搜索       │
    └─────────────┴──────────────────┴──────────────────┘
    """
    print(comparison)


def demo_prompt_design():
    """演示 Prompt 设计"""
    print("\n=== Prompt 设计示例 ===")

    # 股票分析 Prompt
    stock_prompt = """
【系统指令】
你是一个专业的股票分析师。请根据提供的股票数据进行分析。

【输入数据】
股票代码: AAPL
当前价格: $150.25
52周最高: $199.62
52周最低: $124.17
市值: 2.5万亿

【输出要求】
请以JSON格式返回分析结果，包含以下字段：
- trend: 趋势判断 (上涨/下跌/横盘)
- risk_level: 风险等级 (高/中/低)
- recommendation: 投资建议
- key_points: 关键要点(列表)
"""
    print("股票分析 Prompt:\n", stock_prompt)

    # Few-shot 示例
    few_shot_prompt = """
【示例】
输入: TSLA, 价格$750, 市值800亿
输出: {"trend": "上涨", "risk_level": "中", "recommendation": "持有"}

【实际任务】
输入: NVDA, 价格$280, 市值700亿
输出:
"""
    print("\nFew-shot Prompt:\n", few_shot_prompt)


# ============================================
# 主程序
# ============================================

if __name__ == "__main__":
    print("Day 22: LLM 基础 - Transformer 与 Attention")
    print("=" * 60)

    demo_attention()
    demo_multi_head_attention()
    demo_positional_encoding()
    demo_transformer_block()
    demo_tokenizer()
    demo_llm_concepts()
    demo_gpt_vs_bert()
    demo_prompt_design()

    print("\n" + "=" * 60)
    print("学习要点:")
    print("1. Attention 让每个词关注其他词的重要性")
    print("2. Multi-Head 让模型从多个角度理解语义")
    print("3. 位置编码让模型知道词的位置信息")
    print("4. GPT擅长生成，BERT擅长理解")
    print("5. Prompt设计是使用LLM的关键技能")