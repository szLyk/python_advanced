# Month 2 代码配置说明

## ⚠️ 敏感信息警告

**不要将 API Key 等敏感信息直接写入代码文件中！**

---

## 正确做法

### 1. 创建 .env 文件

复制 `.env.example` 为 `.env`：

```bash
cp .env.example .env
```

### 2. 填写真实 API Key

编辑 `.env` 文件：

```bash
# DeepSeek API Key
DEEPSEEK_API_KEY=sk-你的真实 DeepSeek API Key
DEEPSEEK_BASE_URL=https://api.deepseek.com

# OpenAI API Key（可选）
OPENAI_API_KEY=sk-你的真实 OpenAI API Key
OPENAI_BASE_URL=https://api.openai.com/v1

# Milvus 配置
MILVUS_HOST=localhost
MILVUS_PORT=19530

# 其他配置
DEFAULT_TEMPERATURE=0.3
```

### 3. 在代码中使用

```python
from config import get_config, create_llm, create_embeddings

# 方式 1: 获取配置
config = get_config()
api_key = config["deepseek"]["api_key"]

# 方式 2: 直接创建 LLM
llm = create_llm(temperature=0.3)

# 方式 3: 创建 Embedding
embeddings = create_embeddings()
```

---

## .gitignore 已配置

以下文件**不会被提交到 Git**：

| 文件 | 说明 |
|------|------|
| `.env` | 包含真实 API Key 的配置文件 |
| `.env.local` | 本地环境配置 |
| `config.local.py` | 本地 Python 配置 |
| `api_key.txt` | API Key 文件 |
| `credentials.json` | 凭证文件 |
| `milvus_data/` | Milvus 数据目录 |
| `evaluation_report.md` | 评估报告 |

可以提交的文件：

| 文件 | 说明 |
|------|------|
| `.env.example` | 配置模板（不含真实 Key） |
| `config.py` | 配置读取代码（不含真实 Key） |
| `config_template.py` | 配置模板 |

---

## 获取 API Key

### DeepSeek（推荐）
1. 访问 https://platform.deepseek.com/
2. 注册/登录账号
3. 进入 API Keys 页面
4. 创建新的 API Key
5. 充值（新用户有优惠）

### OpenAI
1. 访问 https://platform.openai.com/
2. 注册/登录账号
3. 进入 API Keys 页面
4. 创建新的 API Key

---

## 安全检查

提交代码前运行：

```bash
# 检查 Git 状态
git status

# 检查是否有敏感文件
python scripts/check_sensitive.py
```

确保 `.env` 文件不在提交列表中：

```bash
# 确认 .env 没有被追踪
git ls-files | grep .env
# 应该只显示 .env.example，不显示 .env
```

---

## 环境变量优先级

配置读取优先级：

1. **系统环境变量**（最高优先级）
2. **.env 文件**
3. **默认占位符**（仅用于测试，需要替换）

设置系统环境变量：

```bash
# Windows PowerShell
$env:DEEPSEEK_API_KEY="sk-xxx"

# Linux/Mac
export DEEPSEEK_API_KEY="sk-xxx"
```

---

## 项目结构

```
python_advanced/
├── .env                    # ⚠️ 敏感！不要提交
├── .env.example            # ✅ 可以提交的模板
├── .gitignore              # ✅ Git 忽略配置
├── config.py               # ✅ 配置读取代码
├── config_template.py      # ✅ 配置模板
├── month2/
│   ├── week5_.../
│   │   └── day29_.../
│   │       ├── README.md
│   │       └── code.py     # 代码中使用 config.py
│   └── ...
└── scripts/
    └── check_sensitive.py  # 敏感信息检查脚本
```

---

## 快速开始

```bash
# 1. 复制配置模板
cp .env.example .env

# 2. 编辑 .env 填入 API Key
# 使用你喜欢的编辑器打开 .env

# 3. 安装依赖
pip install python-dotenv

# 4. 运行代码
python month2/week5_langchain_basic/day29_langchain_hello/langchain_hello.py
```

---

## 常见问题

### Q: 为什么不能用 config.local.py？
A: 也可以，但使用 `.env` 是更标准的做法，被更多项目采用。

### Q: 忘记把 .env 加入白名单怎么办？
A: 运行 `git rm --cached .env` 从 Git 历史中移除，然后确保 `.gitignore` 中有 `.env`。

### Q: 已经提交了敏感信息怎么办？
A: 
1. 立即删除该文件
2. 使用 `git filter-branch` 或 BFG 清理 Git 历史
3. 更换所有泄露的 API Key
