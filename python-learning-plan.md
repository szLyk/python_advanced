# Python 学习内容规划（AI Agent 工程师方向）

## 📋 学习目标

**目标岗位**：AI Agent 工程师
**学习周期**：120 天（4 个月）
**前置基础**：大数据开发（Java/Scala），Python 懂但不熟悉
**最终能力**：能够独立开发 AI Agent 应用、RAG 系统、多 Agent 协作系统

**当前进度**：Month 1 Week 3 Day 15（2026-04-08）

---

## 📊 整体学习路线

```
第 1 月：Python 核心 + AI 基础
    ↓
第 2 月：LangChain + Agent 基础
    ↓
第 3 月：Agent 进阶 + 项目实战
    ↓
第 4 月：简历 + 面试 + 投递
```

---

## 第 1 月：Python 核心提升

### Week 1: Python 核心语法 ✅ 已完成

| 天数 | 主题 | 学习内容 | 产出 | 状态 |
|------|------|---------|------|------|
| Day 1 | 装饰器 | 装饰器原理、@语法、@wraps | decorator_practice.py | ✅ |
| Day 2 | 生成器 | yield、生成器表达式、迭代器 | generator_practice.py | ✅ |
| Day 3 | 上下文管理器 | with 语句、__enter__/__exit__ | context_manager.py | ✅ |
| Day 4 | 异步编程 | async/await、asyncio | async_basic.py | ✅ |
| Day 5 | 弹性/休息 | 复习/补进度 | - | - |
| Day 6 | 综合项目 | 异步爬虫 | async_crawler.py | ✅ |
| Day 7 | 休息 | - | - | - |

**核心知识点**：
- [x] 装饰器的本质和应用场景
- [x] 生成器 vs 迭代器
- [x] 上下文管理器协议
- [x] 异步编程模型

**推荐资源**：
- B 站：Python 高级编程（黑马程序员）
- 书籍：《Python 编程：从入门到实践》第 8-12 章
- 文档：https://docs.python.org/zh-cn/3/

---

### Week 2: 数据处理库 ✅ 已完成

| 天数 | 主题 | 学习内容 | 产出 | 状态 |
|------|------|---------|------|------|
| Day 8 | numpy 基础 | 数组、索引、切片、广播 | numpy_basic.py | ✅ |
| Day 9 | numpy 进阶 | 线性代数、向量化优化 | numpy_advanced.py | ✅ |
| Day 10 | pandas 基础 | DataFrame、Series、读取 CSV | pandas_basic.py | ✅ |
| Day 11 | pandas 进阶 | 分组、聚合、透视表 | pandas_advanced.py | ✅ |
| Day 12 | 弹性/休息 | 复习/补进度 | - | - |
| Day 13 | 综合项目 | 股票数据分析 | stock_analysis.py | ✅ |
| Day 14 | 休息 | - | - | - |

**核心知识点**：
- [x] numpy 数组操作
- [x] 向量化计算（避免循环）
- [x] pandas DataFrame 操作
- [x] 数据清洗和预处理

**推荐资源**：
- B 站：pandas 从入门到实战（菜鸟教程）
- 书籍：《利用 Python 进行数据分析》
- 文档：https://pandas.pydata.org/docs/

---

### Week 3: API 开发 🔄 进行中

| 天数 | 主题 | 学习内容 | 产出 | 状态 |
|------|------|---------|------|------|
| Day 15 | FastAPI 基础 | 路由、请求、响应 | fastapi_basic.py | 🔄 |
| Day 16 | Pydantic | 数据验证、模型定义 | pydantic_validation.py | ⏳ |
| Day 17 | SQLAlchemy | ORM、数据库连接 | sqlalchemy_crud.py | ⏳ |
| Day 18 | JWT 认证 | OAuth2、Token 认证 | jwt_auth.py | ⏳ |
| Day 19 | 弹性/休息 | 复习/补进度 | - | - |
| Day 20 | 综合项目 | 股票数据 API 服务 | stock_api_service/ | ⏳ |
| Day 21 | 休息 | - | - | - |

**核心知识点**：
- [ ] RESTful API 设计
- [ ] 请求验证和响应序列化
- [ ] 数据库 ORM 操作
- [ ] JWT 认证流程

**推荐资源**：
- B 站：FastAPI 从入门到实战（尚硅谷）
- 官方文档：https://fastapi.tiangolo.com/
- SQLAlchemy 文档：https://www.sqlalchemy.org/

---

### Week 4: AI 基础概念

| 天数 | 主题 | 学习内容 | 产出 | 状态 |
|------|------|---------|------|------|
| Day 22 | LLM 基础 | Transformer、Attention | llm_basic.py | ⏳ |
| Day 23 | Embedding | 词向量、句向量 | embedding_concept.py | ⏳ |
| Day 24 | 大模型 API | OpenAI/DeepSeek 调用 | llm_api_call.py | ⏳ |
| Day 25 | 第 1 月复习 | 整理知识体系 | month1_review.md | ⏳ |
| Day 26 | 弹性/休息 | 复习/补进度 | - | - |
| Day 27 | 月度项目 | Python 股票分析系统 | python_stock_system/ | ⏳ |
| Day 28 | 休息 | - | - | - |

**核心知识点**：
- [ ] LLM 工作原理
- [ ] Embedding 生成和应用
- [ ] 大模型 API 调用
- [ ] Prompt 基础

**推荐资源**：
- B 站：Transformer 详解
- OpenAI 文档：https://platform.openai.com/docs/
- DeepSeek 文档：https://platform.deepseek.com/

---

## 第 2 月：LangChain + Agent 基础

### Week 5: LangChain 基础

| 天数 | 主题 | 学习内容 | 产出 |
|------|------|---------|------|
| Day 29 | LangChain 介绍 | 安装、核心概念 | langchain_hello.py |
| Day 30 | Prompt 模板 | PromptTemplate、FewShot | prompt_template.py |
| Day 31 | Chain | SequentialChain、链式调用 | sequential_chain.py |
| Day 32 | OutputParser | 结构化输出解析 | output_parser.py |
| Day 33 | 弹性/休息 | 复习/补进度 | - |
| Day 34 | 综合项目 | 股票分析助手（基础版） | stock_assistant_basic.py |
| Day 35 | 休息 | - | - |

**核心知识点**：
- [ ] LangChain 核心组件
- [ ] Prompt 设计技巧
- [ ] Chain 链式调用
- [ ] 输出解析和结构化

**推荐资源**：
- B 站：LangChain 从入门到精通（卢菁博士）
- 官方文档：https://python.langchain.com/

---

### Week 6: Agent + Tool 调用

| 天数 | 主题 | 学习内容 | 产出 |
|------|------|---------|------|
| Day 36 | Agent 基础 | ReAct 模式、Agent 类型 | agent_basic.py |
| Day 37 | Tool 定义 | 自定义工具、@tool 装饰器 | custom_tools.py |
| Day 38 | Function Calling | API 调用、外部工具集成 | function_calling.py |
| Day 39 | 记忆管理 | ConversationBufferMemory | agent_memory.py |
| Day 40 | 弹性/休息 | 复习/补进度 | - |
| Day 41 | 综合项目 | 股票查询 Agent | stock_query_agent.py |
| Day 42 | 休息 | - | - |

**核心知识点**：
- [ ] Agent 工作原理（ReAct）
- [ ] Tool 定义和注册
- [ ] Function Calling 机制
- [ ] 多轮对话记忆

**推荐资源**：
- LangChain Agent 文档：https://python.langchain.com/docs/modules/agents/
- B 站：LangChain Agent 实战

---

### Week 7: 向量数据库（精简版）

| 天数 | 主题 | 学习内容 | 产出 |
|------|------|---------|------|
| Day 43 | 向量数据库概念 | Embedding、相似度计算 | embedding_basic.py |
| Day 44 | Milvus 安装 | Docker 部署、配置 | milvus_installed.txt |
| Day 45 | Milvus 操作 | Collection、CRUD | milvus_crud.py |
| Day 46 | LangChain 集成 | VectorStore、检索 | langchain_vectorstore.py |
| Day 47 | 弹性/休息 | 复习/补进度 | - |
| Day 48 | 综合项目 | 股票研报检索系统 | stock_report_search.py |
| Day 49 | 休息 | - | - |

**核心知识点**：
- [ ] 向量数据库概念
- [ ] Milvus 基本操作
- [ ] LangChain VectorStore 集成
- [ ] 语义检索

**推荐资源**：
- Milvus 文档：https://milvus.io/docs
- B 站：Milvus 向量数据库入门

---

### Week 8: RAG 系统

| 天数 | 主题 | 学习内容 | 产出 |
|------|------|---------|------|
| Day 50 | RAG 原理 | 检索增强生成流程 | rag_basic.py |
| Day 51 | 文档加载 | DocumentLoader、分块 | document_chunking.py |
| Day 52 | 检索 + 生成 | RAG 完整流程 | rag_pipeline.py |
| Day 53 | 效果评估 | 准确率、召回率测试 | rag_evaluation.py |
| Day 54 | 弹性/休息 | 复习/补进度 | - |
| Day 55 | 综合项目 | 股票知识库 RAG 系统 | stock_knowledge_rag/ |
| Day 56 | 休息 | - | - |

**核心知识点**：
- [ ] RAG 工作流程
- [ ] 文档加载和分块策略
- [ ] 检索和生成配合
- [ ] 效果评估方法

**推荐资源**：
- B 站：RAG 系统实战
- LangChain RAG 文档：https://python.langchain.com/docs/use_cases/question_answering/

---

## 第 3 月：Agent 进阶 + 项目实战

### Week 9: AutoGen 多 Agent 协作

| 天数 | 主题 | 学习内容 | 产出 |
|------|------|---------|------|
| Day 57 | AutoGen 基础 | 安装、核心概念 | autogen_hello.py |
| Day 58 | 多 Agent 对话 | 对话编排、角色定义 | multi_agent_chat.py |
| Day 59 | 任务分解 | 复杂任务处理 | task_decomposition.py |
| Day 60 | 代码生成 | Agent 自动写代码 | code_generation.py |
| Day 61 | 弹性/休息 | 复习/补进度 | - |
| Day 62 | 综合项目 | 多 Agent 股票分析系统 | multi_agent_stock_analysis/ |
| Day 63 | 休息 | - | - |

**核心知识点**：
- [ ] AutoGen 架构
- [ ] 多 Agent 对话模式
- [ ] 任务分解策略
- [ ] 代码生成能力

**推荐资源**：
- AutoGen 文档：https://microsoft.github.io/autogen/
- B 站：AutoGen 多 Agent 协作

---

### Week 10: CrewAI 任务编排

| 天数 | 主题 | 学习内容 | 产出 |
|------|------|---------|------|
| Day 64 | CrewAI 基础 | 角色定义、Agent 创建 | crewai_basic.py |
| Day 65 | 任务定义 | Task 配置、期望输出 | crewai_task.py |
| Day 66 | 流程编排 | Sequential 流程 | crewai_sequential.py |
| Day 67 | 工具集成 | 自定义工具、API 集成 | crewai_tools.py |
| Day 68 | 弹性/休息 | 复习/补进度 | - |
| Day 69 | 综合项目 | CrewAI 工作流系统 | crewai_workflow/ |
| Day 70 | 休息 | - | - |

**核心知识点**：
- [ ] CrewAI 角色和任务
- [ ] 流程编排模式
- [ ] 工具集成方法
- [ ] 工作流设计

**推荐资源**：
- CrewAI 文档：https://docs.crewai.com/
- B 站：CrewAI 从入门到实战

---

### Week 11-12: 综合项目

**项目：AI 股票分析助手（完整版）**

| 天数 | 任务 | 产出 |
|------|------|------|
| Day 71 | 项目架构设计 | 技术文档 |
| Day 72 | 数据库设计 | Schema 设计 |
| Day 73 | FastAPI 后端 | API 接口 |
| Day 74 | RAG 系统集成 | 研报检索 |
| Day 75 | 弹性/休息 | - |
| Day 76 | Agent 工具开发 | 股票分析工具 |
| Day 77 | 休息 | - |
| Day 78 | Streamlit 前端 | 用户界面 |
| Day 79 | 系统集成 | 模块联调 |
| Day 80 | 性能优化 | 响应速度 |
| Day 81 | 测试 | 单元测试 |
| Day 82 | 弹性/休息 | - |
| Day 83 | 文档编写 | README |
| Day 84 | 项目演示 | 录制视频 |

**技术栈**：
- Streamlit（前端）
- FastAPI（后端 API）
- LangChain（Agent）
- Milvus（向量数据库）
- MySQL（业务数据）

---

## 第 4 月：简历 + 面试 + 投递

### Week 13: 简历优化

| 天数 | 主题 | 学习内容 | 产出 |
|------|------|---------|------|
| Day 85 | 简历结构 | 研究优秀模板 | resume_v1.md |
| Day 86 | 项目描述 | STAR 法则 | resume_v2.md |
| Day 87 | 技能包装 | 匹配 JD 关键词 | resume_v3.md |
| Day 88 | GitHub 整理 | 优化项目展示 | GitHub 优化完成 |
| Day 89 | 弹性/休息 | 复习/补进度 | - |
| Day 90 | 简历定稿 | 生成 PDF 版本 | resume_final.pdf |
| Day 91 | 休息 | - | - |

---

### Week 14: 面试准备

| 天数 | 主题 | 学习内容 | 产出 |
|------|------|---------|------|
| Day 92 | Python 题库 | 30 道面试题 | python_questions.md |
| Day 93 | LangChain 题库 | 20 道面试题 | langchain_questions.md |
| Day 94 | Agent 题库 | 20 道面试题 | agent_questions.md |
| Day 95 | RAG/向量库 | 15 道面试题 | rag_questions.md |
| Day 96 | 弹性/休息 | 复习/补进度 | - |
| Day 97 | 项目深挖 | 准备话术 | project_talks.md |
| Day 98 | 休息 | - | - |

---

### Week 15: 模拟面试

| 天数 | 主题 | 学习内容 | 产出 |
|------|------|---------|------|
| Day 99 | 技术面模拟 | 朋友/在线模拟 | interview_practice.md |
| Day 100 | HR 面模拟 | 行为问题准备 | hr_questions.md |
| Day 101 | 项目介绍 | 5 分钟演讲 | project_presentation.md |
| Day 102 | 弱点准备 | 如何回答缺点 | weakness_answer.md |
| Day 103 | 弹性/休息 | 复习/补进度 | - |
| Day 104 | 全真模拟 | 完整面试流程 | mock_interview.md |
| Day 105 | 休息 | - | - |

---

### Week 16: 开始投递

| 天数 | 主题 | 学习内容 | 产出 |
|------|------|---------|------|
| Day 106 | 公司调研 | 列出目标公司 | target_companies.md |
| Day 107 | 第一批投递 | 5 家公司 | application_log.xlsx |
| Day 108 | 第二批投递 | 5 家公司 | application_log.xlsx |
| Day 109 | 面试复盘 | 总结经验 | interview_review.md |
| Day 110 | 弹性/休息 | 复习/补进度 | - |
| Day 111 | 继续投递 | 5-10 家公司 | application_log.xlsx |
| Day 112 | 休息 | - | - |

---

## 📚 推荐学习资源

### B 站课程
| 课程 | UP 主 | 时长 | 优先级 |
|------|------|------|--------|
| Python 高级编程 | 黑马程序员 | 20h | ⭐⭐⭐⭐⭐ |
| pandas 数据分析 | 菜鸟教程 | 15h | ⭐⭐⭐⭐⭐ |
| FastAPI 从入门到实战 | 尚硅谷 | 12h | ⭐⭐⭐⭐ |
| LangChain 从入门到精通 | 卢菁博士 | 15h | ⭐⭐⭐⭐⭐ |
| AutoGen 多 Agent 协作 | 微软中国 | 8h | ⭐⭐⭐⭐ |

### 书籍
| 书籍 | 优先级 | 阅读时间 |
|------|--------|---------|
| 《Python 编程：从入门到实践》 | ⭐⭐⭐⭐ | 第 1 月 |
| 《利用 Python 进行数据分析》 | ⭐⭐⭐⭐ | 第 2 月 |
| 《LangChain 实战》 | ⭐⭐⭐ | 第 2 月 |
| 《检索增强生成 (RAG) 实战》 | ⭐⭐⭐ | 第 2 月 |

### 官方文档
- Python: https://docs.python.org/zh-cn/3/
- LangChain: https://python.langchain.com/
- Milvus: https://milvus.io/docs
- FastAPI: https://fastapi.tiangolo.com/
- AutoGen: https://microsoft.github.io/autogen/
- CrewAI: https://docs.crewai.com/

---

## 🎯 项目清单

### 必做项目（6 个）
- [ ] 股票数据 API 服务（Week 3）
- [ ] 股票分析助手（Week 5-6）
- [ ] 股票研报检索系统（Week 7）
- [ ] 股票知识库 RAG 系统（Week 8）
- [ ] 多 Agent 股票分析系统（Week 9）
- [ ] AI 股票分析助手完整版（Week 11-12）

### 选做项目（3 个）
- [ ] 技术博客（2-3 篇）
- [ ] GitHub 开源项目
- [ ] 参与社区活动

---

## 📊 学习进度追踪

### 月度检查点

| 月份 | 目标 | 检查项 | 状态 |
|------|------|--------|------|
| 第 1 月 | Python 提升 | ✅ 掌握装饰器/异步 ✅ 完成 3 个项目 | 🔄 |
| 第 2 月 | Agent 基础 | □ 掌握 LangChain □ 完成 RAG 系统 | □ |
| 第 3 月 | 项目实战 | □ 完成综合项目 □ GitHub 有作品 | □ |
| 第 4 月 | 求职投递 | □ 简历完成 □ 投递 15+ 公司 | □ |

### 周度检查点

每周日复盘：
- [x] 本周计划完成度
- [x] 遇到的问题
- [x] 下周调整计划
- [x] 代码提交 GitHub

### 每日检查点

每天学习后：
- [x] 完成今日任务
- [x] 代码已保存
- [x] 笔记已整理
- [x] 问题已记录

---

## 💡 学习建议

### ✅ 建议
1. **每天坚持**：工作日 2 小时，周末 6-8 小时
2. **动手优先**：视频 1.5 倍速，70% 时间写代码
3. **项目驱动**：每个周完成一个小项目
4. **及时复习**：每周日复盘，每月总结
5. **建立连接**：加入学习群，找人讨论

### ❌ 避免
1. 只看不练（眼高手低）
2. 追求完美（完成比完美重要）
3. 死磕难题（超过 1 小时就问）
4. 不写笔记（好记性不如烂笔头）
5. 孤军奋战（加入社区）

---

## 🚀 下一步行动

### 本周（Week 3）
- [ ] 完成 Day 15-18 的学习
- [ ] 完成股票数据 API 服务项目
- [ ] 掌握 FastAPI + SQLAlchemy + JWT

### 本月（Month 1）
- [x] 完成 Python 核心提升
- [x] 完成 4 个小项目
- [ ] 建立 AI 基础认知
- [ ] 加入学习社区

---

**120 天后，你就是 AI Agent 工程师！加油！💪**

**最后更新**：2026-04-08
**版本**：v1.1
**作者**：AI Transition Coach