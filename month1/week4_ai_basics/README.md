# Week 4: AI 基础概念

**状态：** 🔄 学习中

## 学习目标

理解 LLM 和 Embedding 基础概念，掌握大模型 API 调用，为 Month 2 的 LangChain 学习打下基础。

## 知识点清单

- [ ] Transformer 架构原理
- [ ] Attention 机制理解
- [ ] GPT vs BERT 区别
- [ ] Embedding 概念和应用
- [ ] 向量相似度计算
- [ ] LLM API 调用
- [ ] Function Calling
- [ ] Prompt 工程基础

## 学习日程

| 天数 | 主题 | 文件 | 状态 |
|------|------|------|------|
| Day 22 | LLM 基础 | day22_llm_basic/ | ⏳ |
| Day 23 | Embedding | day23_embedding/ | ⏳ |
| Day 24 | 大模型 API | day24_llm_api/ | ⏳ |
| Day 25 | 第1月复习 | month1_review.md | ⏳ |
| Day 26 | 弹性/休息 | - | - |
| Day 27 | 月度项目 | day27_stock_analysis_system/ | ⏳ |
| Day 28 | 休息 | - | - |

## 核心概念

### LLM 基础
```
Transformer 架构
├── Encoder（理解）
│   └── Self-Attention
├── Decoder（生成）
│   └── Masked Attention
└── 位置编码
```

### Embedding
```
文本 → 向量转换
├── Word2Vec（词向量）
├── BERT（上下文嵌入）
├── BGE（中文优化）
└── 应用：语义搜索、RAG
```

### LLM API
```
调用流程
├── 配置 API Key
├── 构建消息（system/user/assistant）
├── 设置参数（temperature、max_tokens）
├── 流式输出（stream=True）
└── Function Calling
```

## 学习资源

- Transformer 论文：Attention Is All You Need
- B 站：Transformer 详解视频
- OpenAI 文档：https://platform.openai.com/docs/
- DeepSeek 文档：https://platform.deepseek.com/

## 本周产出

- llm_basic.py - Transformer/Attention 实现
- embedding_concept.py - Embedding 示例
- llm_api_call.py - API 调用封装
- stock_system.py - 月度综合项目

## 运行方式

```bash
# Day 22-24
python llm_basic.py
python embedding_concept.py
python llm_api_call.py

# Day 27 综合项目
python stock_system.py
python stock_system.py --serve  # 启动API服务
```

## Month 1 学习回顾

### Week 1: Python 核心
- 装饰器、生成器、上下文管理器、异步编程

### Week 2: 数据处理
- NumPy、Pandas、数据分析实战

### Week 3: API 开发
- FastAPI、Pydantic、SQLAlchemy、JWT认证

### Week 4: AI 基础
- LLM 原理、Embedding、API 调用

### 综合能力
能够使用 Python + AI API 构建数据分析应用，为 Month 2 LangChain 学习做好准备。