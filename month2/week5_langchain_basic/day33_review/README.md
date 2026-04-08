# Day 33: Week 5 复习/补进度

> **日期**: 2026-05-05（周一）  
> **周次**: Week 5 - LangChain 基础  
> **预计耗时**: 2 小时

---

## 今日目标

- [ ] 复习 Day 29-32 的内容
- [ ] 补做未完成的练习
- [ ] 整理 Week 5 知识笔记
- [ ] 代码提交 GitHub

---

## 复习清单

### Day 29: LangChain 介绍
- [ ] LangChain 核心概念理解
- [ ] 环境安装和配置
- [ ] 第一个 LangChain 程序运行成功

### Day 30: Prompt 模板
- [ ] PromptTemplate 使用熟练
- [ ] FewShot Prompting 理解
- [ ] 股票场景 Prompt 设计

### Day 31: Chain
- [ ] SequentialChain 使用
- [ ] LCEL 语法掌握
- [ ] 自定义 Chain 实现

### Day 32: OutputParser
- [ ] StrOutputParser 基础
- [ ] PydanticOutputParser 结构化输出
- [ ] 解析错误处理

---

## 知识整理

### 创建 Week 5 知识脑图

```
LangChain 基础 (Week 5)
├── 核心概念
│   ├── Model (LLM, ChatModel, Embedding)
│   ├── Prompt (Template, FewShot)
│   ├── Chain (Sequential, LCEL)
│   └── OutputParser (Str, Pydantic, JSON)
│
├── 安装配置
│   ├── pip install langchain langchain-openai
│   └── API Key 配置
│
├── 股票场景应用
│   ├── 股票分析 Prompt
│   ├── 结构化分析报告
│   └── 多步骤分析 Chain
│
└── 常见问题
    ├── API 调用失败
    ├── 输出解析错误
    └── Prompt 调试技巧
```

---

## 补做练习

### 未完成的任务
- [ ] Day 29: 练习____
- [ ] Day 30: 练习____
- [ ] Day 31: 练习____
- [ ] Day 32: 练习____

### 额外练习
```python
# 综合练习：创建一个完整的股票分析 Chain
# 输入：股票代码
# 输出：结构化分析报告（包含 PE、PB、投资建议等）
```

---

## 代码整理

```bash
# 确保所有代码文件都已组织好
week5_langchain_basic/
├── day29_langchain_hello/
├── day30_prompt_template/
├── day31_chain/
├── day32_output_parser/
└── day34_stock_assistant/
```

---

## GitHub 提交

```bash
# 提交 Week 5 代码
git add month2/week5_langchain_basic/
git commit -m "feat: Week 5 LangChain 基础完成"
git push
```

---

## 自我评估

| 知识点 | 理解程度 | 需要加强 |
|--------|----------|----------|
| LangChain 架构 | ⬜⬜⬜⬜⬜ | |
| Prompt 设计 | ⬜⬜⬜⬜⬜ | |
| Chain 使用 | ⬜⬜⬜⬜⬜ | |
| OutputParser | ⬜⬜⬜⬜⬜ | |

---

## 下周准备

- 预习 Week 6: Agent + Tool 调用
- 阅读 Agent 相关文档
- 了解 ReAct 模式

---

**💡 Week 5 总结**: 打好基础，LangChain 核心组件已掌握！
