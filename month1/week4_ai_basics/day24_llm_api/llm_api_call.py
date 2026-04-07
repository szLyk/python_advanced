"""
Day 24: 大模型 API 调用

学习目标：
1. 掌握 OpenAI/DeepSeek API 调用
2. 实现多轮对话和流式输出
3. 使用 Function Calling
"""

import os
import json
import time
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass


# ============================================
# 1. 配置管理
# ============================================

@dataclass
class APIConfig:
    """API 配置"""
    api_key: str
    base_url: str
    model: str

    @classmethod
    def from_env(cls, provider: str = "openai") -> "APIConfig":
        """从环境变量加载配置"""
        if provider == "openai":
            return cls(
                api_key=os.getenv("OPENAI_API_KEY", ""),
                base_url="https://api.openai.com/v1",
                model="gpt-3.5-turbo"
            )
        elif provider == "deepseek":
            return cls(
                api_key=os.getenv("DEEPSEEK_API_KEY", ""),
                base_url="https://api.deepseek.com/v1",
                model="deepseek-chat"
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")


# ============================================
# 2. 模拟 LLM 客户端（无 API Key 时使用）
# ============================================

class MockLLMClient:
    """
    模拟 LLM 客户端（用于演示）

    实际使用时替换为真实 API：
    from openai import OpenAI
    client = OpenAI(api_key=config.api_key, base_url=config.base_url)
    """

    def __init__(self, config: APIConfig):
        self.config = config
        self.call_count = 0

    def chat_completion(
        self,
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 500,
        stream: bool = False,
        tools: Optional[List] = None
    ) -> Dict:
        """模拟聊天补全"""
        self.call_count += 1

        # 模拟回复（基于消息内容）
        last_user_message = ""
        for msg in reversed(messages):
            if msg["role"] == "user":
                last_user_message = msg["content"]
                break

        # 检查是否有函数调用
        if tools:
            for tool in tools:
                if tool["type"] == "function":
                    func_name = tool["function"]["name"]
                    if func_name == "get_stock_price" and "AAPL" in last_user_message:
                        return {
                            "content": None,
                            "tool_calls": [{
                                "function": {
                                    "name": "get_stock_price",
                                    "arguments": json.dumps({"symbol": "AAPL"})
                                }
                            }]
                        }

        # 模拟不同类型的回复
        system_msg = ""
        for msg in messages:
            if msg["role"] == "system":
                system_msg = msg["content"]
                break

        # 根据系统提示生成模拟回复
        if "股票分析师" in system_msg or "股票" in last_user_message:
            mock_response = self._mock_stock_response(last_user_message)
        elif "摘要" in system_msg or "总结" in last_user_message:
            mock_response = self._mock_summary_response(last_user_message)
        elif "情绪" in system_msg or "分析" in last_user_message:
            mock_response = self._mock_sentiment_response(last_user_message)
        else:
            mock_response = f"收到您的消息：{last_user_message[:50]}... 这是一个模拟回复。"

        if stream:
            return {"stream": True, "content": mock_response}

        return {"content": mock_response}

    def _mock_stock_response(self, query: str) -> str:
        """模拟股票分析回复"""
        return f"""根据查询 '{query}'，以下是模拟分析结果：

股票代码: AAPL
当前价格: $150.25
52周最高: $199.62
52周最低: $124.17
市值: 2.5万亿

分析建议：
- 技术面：短期呈上升趋势
- 基本面：财务状况健康
- 建议：可考虑逢低买入

注：这是模拟数据，实际请调用真实API。"""

    def _mock_summary_response(self, text: str) -> str:
        """模拟摘要回复"""
        return f"摘要：{text[:100]}的核心内容是关于股票市场动态和投资机会。"

    def _mock_sentiment_response(self, text: str) -> str:
        """模拟情绪分析回复"""
        positive_words = ["上涨", "利好", "增长", "新高"]
        negative_words = ["下跌", "利空", "亏损", "暴跌"]

        pos_count = sum(1 for w in positive_words if w in text)
        neg_count = sum(1 for w in negative_words if w in text)

        if pos_count > neg_count:
            return "情绪分析结果：正面"
        elif neg_count > pos_count:
            return "情绪分析结果：负面"
        else:
            return "情绪分析结果：中性"

    def embedding(self, text: str) -> List[float]:
        """模拟 Embedding"""
        # 生成伪向量（仅演示）
        import random
        seed = sum(ord(c) for c in text)
        random.seed(seed)
        return [random.gauss(0, 1) for _ in range(1536)]


# ============================================
# 3. LLM 服务封装
# ============================================

class LLMService:
    """LLM 服务封装"""

    def __init__(self, config: APIConfig, use_mock: bool = True):
        self.config = config
        self.use_mock = use_mock

        if use_mock or not config.api_key:
            self.client = MockLLMClient(config)
            print("使用模拟客户端（无真实API调用）")
        else:
            # 实际使用时导入 OpenAI
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=config.api_key, base_url=config.base_url)
                self.use_mock = False
                print(f"连接真实API: {config.base_url}")
            except ImportError:
                self.client = MockLLMClient(config)
                print("未安装openai库，使用模拟客户端")

    def chat(
        self,
        user_message: str,
        system_message: str = "你是一个有帮助的AI助手",
        history: List[Dict] = None,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """
        单轮对话

        Args:
            user_message: 用户消息
            system_message: 系统提示
            history: 历史对话
            temperature: 温度参数
            max_tokens: 最大输出长度

        Returns:
            AI回复
        """
        messages = [{"role": "system", "content": system_message}]

        if history:
            messages.extend(history)

        messages.append({"role": "user", "content": user_message})

        if self.use_mock:
            response = self.client.chat_completion(messages, temperature, max_tokens)
            return response["content"]
        else:
            # 真实API调用
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content

    def chat_stream(
        self,
        user_message: str,
        system_message: str = "你是一个有帮助的AI助手"
    ) -> str:
        """
        流式对话

        Yields:
            逐块输出的内容
        """
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        if self.use_mock:
            response = self.client.chat_completion(messages, stream=True)
            content = response["content"]
            # 模拟流式输出
            for i in range(0, len(content), 10):
                yield content[i:i+10]
                time.sleep(0.05)
        else:
            stream = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

    def multi_round_chat(
        self,
        messages: List[Dict],
        temperature: float = 0.7
    ) -> str:
        """
        多轮对话

        Args:
            messages: 完整对话历史
            temperature: 温度参数

        Returns:
            AI回复
        """
        if self.use_mock:
            response = self.client.chat_completion(messages, temperature)
            return response["content"]
        else:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content

    def function_call(
        self,
        user_message: str,
        tools: List[Dict],
        system_message: str = "你是一个有帮助的AI助手"
    ) -> Dict:
        """
        函数调用

        Args:
            user_message: 用户消息
            tools: 函数定义列表
            system_message: 系统提示

        Returns:
            函数调用结果或直接回复
        """
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        if self.use_mock:
            response = self.client.chat_completion(messages, tools=tools)
        else:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            if hasattr(response.choices[0].message, 'tool_calls'):
                if response.choices[0].message.tool_calls:
                    return {
                        "type": "tool_call",
                        "tool_calls": response.choices[0].message.tool_calls
                    }
            return {
                "type": "content",
                "content": response.choices[0].message.content
            }

        return response

    def get_embedding(self, text: str) -> List[float]:
        """
        获取文本 Embedding

        Args:
            text: 输入文本

        Returns:
            Embedding 向量
        """
        if self.use_mock:
            return self.client.embedding(text)
        else:
            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding


# ============================================
# 4. 股票分析应用示例
# ============================================

# 定义可调用的函数
def get_stock_price(symbol: str) -> Dict:
    """获取股票价格（模拟）"""
    mock_data = {
        "AAPL": {"price": 150.25, "change": "+2.5%", "volume": 5000000},
        "GOOGL": {"price": 2800.50, "change": "-1.2%", "volume": 2000000},
        "TSLA": {"price": 750.80, "change": "+5.3%", "volume": 8000000},
        "MSFT": {"price": 300.00, "change": "+0.8%", "volume": 3000000}
    }
    return mock_data.get(symbol.upper(), {"error": "Stock not found"})


def analyze_news_sentiment(news: str) -> Dict:
    """分析新闻情绪（模拟）"""
    positive = ["上涨", "利好", "增长", "新高", "突破"]
    negative = ["下跌", "利空", "亏损", "暴跌", "风险"]

    pos_count = sum(1 for w in positive if w in news)
    neg_count = sum(1 for w in negative if w in news)

    if pos_count > neg_count:
        return {"sentiment": "正面", "confidence": 0.85}
    elif neg_count > pos_count:
        return {"sentiment": "负面", "confidence": 0.75}
    else:
        return {"sentiment": "中性", "confidence": 0.60}


def summarize_news(news: str) -> str:
    """摘要新闻（模拟）"""
    return f"核心要点：{news[:50]}... [摘要长度: {len(news)//2}字]"


# 函数定义（用于 Function Calling）
STOCK_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "获取股票当前价格和成交量",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "股票代码，如 AAPL, GOOGL"
                    }
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_news_sentiment",
            "description": "分析财经新闻的情绪倾向",
            "parameters": {
                "type": "object",
                "properties": {
                    "news": {
                        "type": "string",
                        "description": "新闻文本内容"
                    }
                },
                "required": ["news"]
            }
        }
    }
]


# ============================================
# 5. 演示代码
# ============================================

def demo_basic_chat():
    """演示基本对话"""
    print("\n=== 基本对话演示 ===")

    config = APIConfig.from_env("openai")
    llm = LLMService(config, use_mock=True)

    # 单轮对话
    response = llm.chat("你好，请介绍一下自己")
    print(f"用户: 你好，请介绍一下自己")
    print(f"AI: {response[:100]}...")

    # 股票分析对话
    response = llm.chat(
        "请分析苹果公司的股票",
        system_message="你是一个专业的股票分析师"
    )
    print(f"\n用户: 请分析苹果公司的股票")
    print(f"AI: {response[:200]}...")


def demo_stream_chat():
    """演示流式对话"""
    print("\n=== 流式对话演示 ===")

    config = APIConfig.from_env("openai")
    llm = LLMService(config, use_mock=True)

    print("用户: 请简单介绍股票投资")
    print("AI: ", end="")

    for chunk in llm.chat_stream("请简单介绍股票投资"):
        print(chunk, end="", flush=True)
    print()


def demo_multi_round():
    """演示多轮对话"""
    print("\n=== 多轮对话演示 ===")

    config = APIConfig.from_env("openai")
    llm = LLMService(config, use_mock=True)

    messages = [
        {"role": "system", "content": "你是股票分析助手"},
        {"role": "user", "content": "AAPL 这只股票怎么样？"},
        {"role": "assistant", "content": "AAPL 是苹果公司的股票，目前表现良好。"},
        {"role": "user", "content": "它的市值是多少？"}
    ]

    response = llm.multi_round_chat(messages)
    print("对话历史:")
    for msg in messages[1:]:
        print(f"  {msg['role']}: {msg['content'][:50]}...")
    print(f"AI回复: {response[:100]}...")


def demo_function_call():
    """演示函数调用"""
    print("\n=== Function Calling 演示 ===")

    config = APIConfig.from_env("openai")
    llm = LLMService(config, use_mock=True)

    # 查询股价
    result = llm.function_call(
        "请查询 AAPL 的股价",
        STOCK_TOOLS,
        "你是股票查询助手，可以帮助用户查询股价信息"
    )

    print("用户: 请查询 AAPL 的股价")

    if "tool_calls" in result:
        tool_call = result["tool_calls"][0]
        func_name = tool_call["function"]["name"]
        args = json.loads(tool_call["function"]["arguments"])

        print(f"模型决定调用函数: {func_name}")
        print(f"参数: {args}")

        # 执行函数
        if func_name == "get_stock_price":
            stock_data = get_stock_price(args["symbol"])
            print(f"函数执行结果: {stock_data}")
    else:
        print(f"直接回复: {result.get('content', '')[:100]}...")


def demo_embedding():
    """演示 Embedding"""
    print("\n=== Embedding 演示 ===")

    config = APIConfig.from_env("openai")
    llm = LLMService(config, use_mock=True)

    texts = [
        "苹果公司股价上涨",
        "特斯拉市值创新高",
        "科技股普遍下跌"
    ]

    print("获取文本 Embedding:")
    for text in texts:
        embedding = llm.get_embedding(text)
        print(f"  '{text}' → 向量维度: {len(embedding)}")


def demo_stock_analysis():
    """演示股票分析应用"""
    print("\n=== 股票分析应用演示 ===")

    config = APIConfig.from_env("openai")
    llm = LLMService(config, use_mock=True)

    # 1. 新闻摘要
    news = "苹果公司今日发布新产品，股价大涨5%，市值突破历史新高，投资者情绪高涨。"
    summary = llm.chat(
        news,
        system_message="请用一句话总结这条财经新闻的核心内容"
    )
    print(f"原始新闻: {news[:50]}...")
    print(f"摘要: {summary}")

    # 2. 情绪分析
    sentiment_result = analyze_news_sentiment(news)
    print(f"\n情绪分析: {sentiment_result}")

    # 3. 投资建议
    stock_data = {
        "symbol": "AAPL",
        "price": 150.25,
        "52w_high": 199.62,
        "52w_low": 124.17
    }

    prompt = f"""
    请根据以下数据给出简要投资建议：
    股票代码: {stock_data['symbol']}
    当前价格: ${stock_data['price']}
    52周最高: ${stock_data['52w_high']}
    52周最低: ${stock_data['52w_low']}
    """

    advice = llm.chat(prompt, system_message="你是投资顾问，给出简洁的建议")
    print(f"\n投资建议: {advice[:100]}...")


def demo_cost_estimation():
    """演示成本估算"""
    print("\n=== API 成本估算 ===")

    costs = """
    OpenAI 价格参考（2024）：
    ┌─────────────────┬──────────────┬──────────────┐
    │ 模型            │ 输入价格     │ 输出价格     │
    ├─────────────────┼──────────────┼──────────────┤
    │ GPT-4           │ $0.03/1K     │ $0.06/1K     │
    │ GPT-3.5-turbo   │ $0.0015/1K   │ $0.002/1K    │
    │ Embedding       │ $0.0001/1K   │ -            │
    └─────────────────┴──────────────┴──────────────┘

    DeepSeek 价格参考：
    ┌─────────────────┬──────────────┬──────────────┐
    │ 模型            │ 输入价格     │ 输出价格     │
    ├─────────────────┼──────────────┼──────────────┤
    │ deepseek-chat   │ ¥1/百万      │ ¥2/百万      │
    └─────────────────┴──────────────┴──────────────┘

    成本计算示例：
    - 1000次对话（每次约500 tokens）: ~$1-2
    - 每日新闻分析100条: ~$0.5

    省钱技巧：
    1. 使用 GPT-3.5 处理简单任务
    2. 限制 max_tokens
    3. 缓存常见问答
    4. 使用 DeepSeek 等国产模型
    """
    print(costs)


def demo_error_handling():
    """演示错误处理"""
    print("\n=== 错误处理示例 ===")

    error_code = """
    from openai import APIError, RateLimitError, AuthenticationError

    try:
        response = client.chat.completions.create(...)
    except AuthenticationError:
        print("API Key 无效，请检查配置")
    except RateLimitError:
        print("请求频率超限，等待后重试")
        time.sleep(60)
    except APIError as e:
        print(f"API 错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")

    # 重试机制
    def call_with_retry(func, max_retries=3):
        for i in range(max_retries):
            try:
                return func()
            except RateLimitError:
                if i < max_retries - 1:
                    time.sleep(10)
                else:
                    raise
    """
    print(error_code)


def demo_prompt_design():
    """演示 Prompt 设计"""
    print("\n=== Prompt 设计技巧 ===")

    prompts = """
    1. 角色定义
       system: "你是专业的股票分析师，擅长基本面和技术面分析"

    2. 任务明确
       user: "请分析 AAPL 的投资价值，从财务、技术、行业三个角度"

    3. 格式约束
       user: "请以 JSON 格式返回分析结果，包含 symbol, trend, recommendation"

    4. Few-shot 示例
       示例输入: "分析 GOOGL"
       示例输出: {"trend": "上涨", "recommendation": "买入"}

    5. 分步骤引导
       "请按以下步骤分析：
        1. 收集基本面数据
        2. 分析技术指标
        3. 评估行业前景
        4. 给出综合建议"

    6. 输出长度控制
       "请用不超过100字简要回答"
    """
    print(prompts)


# ============================================
# 主程序
# ============================================

if __name__ == "__main__":
    print("Day 24: 大模型 API 调用")
    print("=" * 60)

    demo_basic_chat()
    demo_stream_chat()
    demo_multi_round()
    demo_function_call()
    demo_embedding()
    demo_stock_analysis()
    demo_cost_estimation()
    demo_error_handling()
    demo_prompt_design()

    print("\n" + "=" * 60)
    print("学习要点:")
    print("1. OpenAI/DeepSeek API 使用兼容接口")
    print("2. messages 格式: system/user/assistant")
    print("3. temperature 控制输出随机性")
    print("4. stream=True 实现流式输出")
    print("5. Function Calling 让模型调用函数")
    print("6. Embedding 用于语义检索")
    print("\n实际使用:")
    print("1. 设置 API Key: export OPENAI_API_KEY='your-key'")
    print("2. 安装依赖: pip install openai")
    print("3. 将 use_mock=False 启用真实API")