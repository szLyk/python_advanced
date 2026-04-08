"""
Month 2 代码配置文件

使用说明:
1. 将此文件复制为 config.local.py
2. 在 config.local.py 中填入你的真实 API Key
3. config.local.py 已添加到 .gitignore，不会被提交

获取 API Key:
- DeepSeek: https://platform.deepseek.com/
- OpenAI: https://platform.openai.com/
"""

# ============== DeepSeek 配置（推荐）=============
# DeepSeek 价格便宜，效果不错，适合学习使用
DEEPSEEK_API_KEY = "sk-your-deepseek-api-key-here"  # 替换为你的 API Key
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# ============== OpenAI 配置（可选）=============
# 如果有 OpenAI API Key，可以替换下面的值
OPENAI_API_KEY = "sk-your-openai-api-key-here"
OPENAI_BASE_URL = "https://api.openai.com/v1"

# ============== Milvus 配置 ==============
MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"

# ============== 其他配置 ==============
# LLM 模型名称
DEEPSEEK_MODEL = "deepseek-chat"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"

# 默认温度值
DEFAULT_TEMPERATURE = 0.3
