# Day 29: LangChain 介绍

> **日期**: 2026-05-01（周四）  
> **周次**: Week 5 - LangChain 基础  
> **预计耗时**: 2 小时

---

## 今日学习目标

- [ ] 理解 LangChain 的核心概念
- [ ] 完成 LangChain 安装和配置
- [ ] 编写第一个 LangChain 程序
- [ ] 了解 LLM 封装和调用方式

---

## 学习内容

### 1. LangChain 是什么？

LangChain 是一个用于开发由语言模型驱动的应用程序的框架，它提供了：

- **组件化**: 将 AI 应用拆解为可复用的模块
- **链式调用**: 将多个组件串联成完整流程
- **Agent 支持**: 让 LLM 能够调用工具和做出决策
- **记忆管理**: 处理多轮对话的上下文

### 2. LangChain 核心组件

```
┌─────────────────────────────────────────────────────────┐
│                    LangChain 架构                        │
├─────────────────────────────────────────────────────────┤
│  Model（模型）                                          │
│  ├── LLM (大语言模型)                                   │
│  ├── ChatModel (对话模型)                               │
│  └── Embedding (嵌入模型)                               │
├─────────────────────────────────────────────────────────┤
│  Prompt（提示）                                         │
│  ├── PromptTemplate (提示模板)                          │
│  └── FewShotPrompt (少样本提示)                         │
├─────────────────────────────────────────────────────────┤
│  Chain（链）                                            │
│  ├── SequentialChain (顺序链)                           │
│  └── TransformChain (转换链)                            │
├─────────────────────────────────────────────────────────┤
│  Agent（智能体）                                        │
│  ├── ReAct Agent                                        │
│  └── Tool (工具)                                        │
├─────────────────────────────────────────────────────────┤
│  Memory（记忆）                                         │
│  ├── BufferMemory (缓冲记忆)                            │
│  └── SummaryMemory (摘要记忆)                           │
└─────────────────────────────────────────────────────────┘
```

### 3. 安装配置

```bash
# 激活虚拟环境（如果使用）
source venv/Scripts/activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 安装 LangChain 核心包
pip install langchain langchain-community

# 安装 OpenAI 集成（如果使用 OpenAI API）
pip install langchain-openai

# 验证安装
python -c "import langchain; print(langchain.__version__)"
```

### 4. 第一个 LangChain 程序

```python
"""
Day 29: LangChain 入门 - Hello LangChain
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# 1. 初始化 LLM 模型
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key="your-api-key"  # 或使用环境变量 OPENAI_API_KEY
)

# 2. 创建消息并调用
message = HumanMessage(content="你好，请介绍一下自己")
response = llm.invoke([message])

# 3. 输出响应
print(response.content)
```

### 5. 使用 DeepSeek 等国产模型

```python
from langchain_openai import ChatOpenAI

# 使用 DeepSeek API（兼容 OpenAI 接口）
llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key="your-deepseek-api-key"
)
```

---

## 实践任务

### 任务 1: 环境搭建 ✅

- [ ] 安装 LangChain
- [ ] 配置 API Key（环境变量或代码中）
- [ ] 运行测试代码

### 任务 2: 基础调用 ✅

```python
# 创建 langchain_hello.py 并完成以下练习

# 1. 调用 LLM 进行简单对话
# 2. 修改 temperature 参数观察输出变化
# 3. 尝试不同的模型（GPT-3.5, GPT-4, DeepSeek 等）
```

### 任务 3: 股票场景初探 ✅

```python
# 用 LLM 回答股票相关问题
question = "什么是市盈率（PE）？如何用它评估股票？"
```

---

## 知识点总结

| 概念 | 说明 |
|------|------|
| LLM | 大语言模型，如 GPT-4、DeepSeek |
| ChatModel | 专门用于对话的模型 |
| temperature | 控制输出随机性，0=确定，1=随机 |
| invoke() | 调用模型的方法 |
| HumanMessage | 用户消息类型 |
| AIMessage | AI 响应消息类型 |

---

## 常见问题

### Q1: API Key 如何配置？

```bash
# 方式 1: 使用 .env 文件（推荐，参考项目根目录配置）
# 1. 复制 .env.example 为 .env
cp .env.example .env
# 2. 编辑 .env 填入 API Key
DEEPSEEK_API_KEY=sk-your-api-key
# 3. 在代码中使用
from config import create_llm
llm = create_llm(temperature=0.7)

# 方式 2: 环境变量
export OPENAI_API_KEY="sk-xxx"  # Linux/Mac
set OPENAI_API_KEY=sk-xxx  # Windows CMD
$env:OPENAI_API_KEY="sk-xxx"  # Windows PowerShell
```

### Q2: 国内无法访问 OpenAI 怎么办？

- 使用 DeepSeek、通义千问等国产模型
- 使用代理服务器
- 使用国内镜像 API 服务

### Q3: 安装失败怎么办？

```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像
pip install langchain -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 代码文件

```
day29_langchain_hello/
├── README.md                 # 本文件
├── langchain_hello.py        # 主程序
├── langchain_stock_test.py   # 股票场景测试
└── requirements.txt          # 依赖清单
```

---

## 参考资源

- [LangChain 官方文档](https://python.langchain.com/)
- [LangChain 中文网](https://www.langchain.com.cn/)
- [OpenAI API 文档](https://platform.openai.com/docs/)
- [DeepSeek API 文档](https://platform.deepseek.com/)

---

## 下一步

完成今日学习后，继续：

- **Day 30**: Prompt 模板（PromptTemplate、FewShot）
- **明日任务**: 学习如何设计和优化 Prompt

---

**💡 今日格言**: "好的 Prompt 是成功的一半"
