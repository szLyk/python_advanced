# Day 24: 大模型 API 调用

## 学习目标

掌握 OpenAI / DeepSeek 等大模型 API 的调用方法，为 AI Agent 开发打好基础。

## 知识点

### 1. 大模型 API 概览

```
主流 API 服务：
├── OpenAI (GPT-4, GPT-3.5)
│   - 最成熟、功能最全
│   - 价格较高
│   - 国际用户需代理
│
├── DeepSeek
│   - 国产优秀模型
│   - 价格实惠
│   - 中文能力强
│
├── Anthropic (Claude)
│   - 安全性优秀
│   - 长文本能力强
│   - API 简洁
│
├── 国产其他
│   - 阿里通义千问
│   - 百度文心一言
│   - 讯飞星火
```

### 2. OpenAI API 基础

```python
from openai import OpenAI

# 初始化客户端
client = OpenAI(api_key="your-api-key")

# 基本调用
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "你是一个股票分析师"},
        {"role": "user", "content": "分析 AAPL 的投资价值"}
    ]
)

# 获取回复
answer = response.choices[0].message.content
print(answer)
```

### 3. DeepSeek API

```python
from openai import OpenAI

# DeepSeek 使用兼容 OpenAI 的接口
client = OpenAI(
    api_key="your-deepseek-key",
    base_url="https://api.deepseek.com/v1"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "你好"}
    ]
)
```

### 4. 消息格式

```python
messages = [
    # 系统角色：定义 AI 的行为
    {"role": "system", "content": "你是一个专业的股票分析师"},

    # 用户消息：用户的输入
    {"role": "user", "content": "请分析苹果公司"},

    # AI 回复（用于多轮对话）
    {"role": "assistant", "content": "苹果公司是一家..."},

    # 继续提问
    {"role": "user", "content": "它的股价表现如何？"}
]
```

### 5. 参数配置

```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,

    # 温度参数（0-2）
    temperature=0.7,  # 0=确定性，1=正常，2=随机

    # 最大输出长度
    max_tokens=500,

    # Top-P 采样
    top_p=0.9,

    # 停止词
    stop=["END", "\n\n"],

    # 流式输出
    stream=True
)
```

### 6. 流式输出

```python
# 流式输出（实时显示）
stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    stream=True  # 开启流式
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### 7. Function Calling

```python
# 定义函数
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "获取股票当前价格",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "股票代码，如 AAPL"
                    }
                },
                "required": ["symbol"]
            }
        }
    }
]

# 调用
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# 处理函数调用
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    # 执行函数
    if function_name == "get_stock_price":
        result = get_stock_price(arguments["symbol"])
```

### 8. Embedding API

```python
# 获取文本 Embedding
response = client.embeddings.create(
    model="text-embedding-ada-002",
    input="苹果公司股价上涨"
)

embedding = response.data[0].embedding
print(f"向量维度: {len(embedding)}")  # 1536
```

### 9. 错误处理

```python
from openai import APIError, RateLimitError, AuthenticationError

try:
    response = client.chat.completions.create(...)
except AuthenticationError:
    print("API Key 无效")
except RateLimitError:
    print("请求频率超限，请稍后重试")
except APIError as e:
    print(f"API 错误: {e}")
```

### 10. 成本计算

```
OpenAI 价格（2024）：
- GPT-4: 输入 $0.03/1K tokens, 输出 $0.06/1K tokens
- GPT-3.5-turbo: 输入 $0.0015/1K tokens, 输出 $0.002/1K tokens

DeepSeek 价格：
- deepseek-chat: 输入 ¥1/百万tokens, 输出 ¥2/百万tokens

成本优化建议：
1. 使用更便宜的模型处理简单任务
2. 控制 max_tokens 限制输出长度
3. 缓存常用问答结果
4. 使用本地模型处理敏感数据
```

## 练习任务

1. 注册并获取 API Key
2. 完成基本的对话调用
3. 实现多轮对话
4. 尝试流式输出
5. 使用 Function Calling
6. 获取文本 Embedding

## 股票场景应用

```python
# 股票新闻摘要
def summarize_news(news_text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是财经新闻摘要专家"},
            {"role": "user", "content": f"请用一句话总结这条新闻：\n{news_text}"}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content

# 股票情绪分析
def analyze_sentiment(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "分析文本情绪，返回：正面/负面/中性"},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

# 投资建议生成
def generate_recommendation(stock_data: dict) -> str:
    prompt = f"""
    根据以下股票数据，给出投资建议：
    - 股票代码: {stock_data['symbol']}
    - 当前价格: {stock_data['price']}
    - 52周最高: {stock_data['52w_high']}
    - 52周最低: {stock_data['52w_low']}
    - 市盈率: {stock_data['pe_ratio']}
    """
    ...
```

## 运行练习

```bash
# 设置环境变量
export OPENAI_API_KEY="your-key"
export DEEPSEEK_API_KEY="your-key"

# 运行
python llm_api_call.py
```

## API Key 获取

- OpenAI: https://platform.openai.com/api-keys
- DeepSeek: https://platform.deepseek.com/api_keys
- Anthropic: https://console.anthropic.com/

## 参考资料

- OpenAI 文档：https://platform.openai.com/docs
- DeepSeek 文档：https://platform.deepseek.com/docs
- Function Calling：https://platform.openai.com/docs/guides/function-calling