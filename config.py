"""
统一配置模块

从 .env 文件读取 API Key 等敏感配置
config.py 可以安全提交到 Git
敏感信息在 .env 中，.env 已添加到 .gitignore
"""

import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()


def get_config():
    """
    获取配置信息

    优先级：环境变量 > .env 文件 > 默认占位符

    使用方法:
    1. 创建 .env 文件（不要提交到 Git）
    2. 在 .env 中填写 API Key
    3. 代码中调用 get_config() 获取配置
    """

    # 从环境变量或 .env 读取
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "sk-your-deepseek-api-key")
    deepseek_base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

    openai_api_key = os.getenv("OPENAI_API_KEY", "sk-your-openai-api-key")
    openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    milvus_host = os.getenv("MILVUS_HOST", "localhost")
    milvus_port = os.getenv("MILVUS_PORT", "19530")

    deepseek_model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    openai_embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "BAAI/bge-m3")

    temperature = float(os.getenv("DEFAULT_TEMPERATURE", "0.3"))

    return {
        "deepseek": {
            "api_key": deepseek_api_key,
            "base_url": deepseek_base_url,
            "model": deepseek_model,
        },
        "openai": {
            "api_key": openai_api_key,
            "base_url": openai_base_url,
            "embedding_model": openai_embedding_model,
        },
        "milvus": {
            "host": milvus_host,
            "port": milvus_port,
        },
        "temperature": temperature,
    }


def create_llm(temperature=0.3):
    """创建 LLM 实例"""
    from langchain_openai import ChatOpenAI

    config = get_config()
    return ChatOpenAI(
        model=config["deepseek"]["model"],
        base_url=config["deepseek"]["base_url"],
        api_key=config["deepseek"]["api_key"],
        temperature=temperature,
    )


def create_embeddings():
    """创建 Embedding 模型实例"""
    from langchain_openai import OpenAIEmbeddings

    config = get_config()
    return OpenAIEmbeddings(
        model=config["openai"]["embedding_model"],
        base_url=config["deepseek"]["base_url"],
        api_key=config["deepseek"]["api_key"],
    )


# 快捷访问
config = get_config()
