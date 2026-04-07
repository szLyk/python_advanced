# Month 1 复习总结

## 📋 学习进度

| Week | 主题 | 状态 | 完成度 |
|------|------|------|--------|
| Week 1 | Python 核心语法 | ✅ 已完成 | 100% |
| Week 2 | 数据处理库 | ✅ 已完成 | 100% |
| Week 3 | API 开发 | ✅ 已完成 | 100% |
| Week 4 | AI 基础概念 | ✅ 已完成 | 100% |

---

## Week 1: Python 核心语法

### 核心知识点

#### 1. 装饰器 (Decorator)
```python
@timer
@cache_result(expire_seconds=60)
def fetch_stock_price(symbol):
    # 函数逻辑
    pass

# 装饰器本质：func = decorator(func)
```
- 用途：计时、缓存、日志、权限控制
- 带参数装饰器：三层嵌套函数
- 类装饰器：使用 __call__ 方法

#### 2. 生成器 (Generator)
```python
def stock_price_generator(prices):
    for price in prices:
        yield price

# 惰性计算，节省内存
```
- yield 关键字生成值
- 生成器表达式：`(x for x in data)`
- 适用：大数据流处理

#### 3. 上下文管理器
```python
with open('file.txt') as f:
    data = f.read()

# 自动管理资源（打开/关闭）
```
- __enter__ / __exit__ 方法
- contextlib.contextmanager 装饰器
- 适用：文件、数据库连接、锁

#### 4. 异步编程
```python
async def fetch_data():
    await asyncio.sleep(1)
    return data

# 并发执行，提高效率
```
- async/await 关键字
- asyncio.gather() 并发执行
- aiohttp 异步 HTTP 请求

---

## Week 2: 数据处理库

### NumPy 核心操作
```python
import numpy as np

# 数组创建
arr = np.array([1, 2, 3])
zeros = np.zeros((3, 4))

# 索引切片
arr[0], arr[:2], arr[arr > 5]

# 数学运算
np.mean(arr), np.std(arr), arr * 2

# 广播机制
a = np.array([[1, 2], [3, 4]])
b = np.array([10, 20])
a + b  # 自动广播
```

### Pandas 核心操作
```python
import pandas as pd

# DataFrame 创建
df = pd.DataFrame({'price': [100, 150, 200]})

# 数据读取
df = pd.read_csv('stocks.csv')

# 数据筛选
df[df['price'] > 100]
df.loc[0:5, ['price', 'date']]

# 分组聚合
df.groupby('sector').mean()

# 技术指标计算
df['ma_5'] = df['close'].rolling(5).mean()
df['change_pct'] = df['close'].pct_change()
```

---

## Week 3: API 开发

### FastAPI 路由
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/stocks/{symbol}")
async def get_stock(symbol: str):
    return {"symbol": symbol}

@app.post("/stocks")
async def create_stock(stock: StockCreate):
    # 创建逻辑
    return stock
```

### Pydantic 验证
```python
from pydantic import BaseModel, Field

class Stock(BaseModel):
    symbol: str = Field(min_length=1, max_length=5)
    price: float = Field(gt=0)

    @field_validator('symbol')
    def uppercase(cls, v):
        return v.upper()
```

### SQLAlchemy ORM
```python
class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(5), unique=True)
    price = Column(Float)

# CRUD 操作
stock = db.query(Stock).filter(Stock.symbol == "AAPL").first()
```

### JWT 认证
```python
# 创建 Token
token = jwt.encode({"sub": username}, SECRET_KEY)

# 验证 Token
payload = jwt.decode(token, SECRET_KEY)

# OAuth2 流程
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm):
    # 验证用户，返回 token
```

---

## Week 4: AI 基础概念

### Transformer 架构
```
输入 → Embedding → 位置编码
         ↓
    Self-Attention
         ↓
    Multi-Head Attention
         ↓
    Feed Forward
         ↓
    输出 Token
```

### Attention 公式
```python
Attention(Q, K, V) = softmax(Q · K^T / sqrt(d_k)) · V

# Q: 查询向量
# K: 键向量
# V: 值向量
```

### Embedding 应用
```python
# 文本转向量
embedding = model.encode("股票上涨")

# 相似度计算
similarity = cosine_similarity(vec_a, vec_b)

# 语义搜索
results = search_engine.search("科技股")
```

### LLM API 调用
```python
from openai import OpenAI

client = OpenAI(api_key="...")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "你是股票分析师"},
        {"role": "user", "content": "分析AAPL"}
    ],
    temperature=0.7
)

# Function Calling
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    tools=[{"type": "function", "function": {...}}]
)
```

---

## 综合项目总结

### 股票分析系统架构
```
数据采集(异步) → 数据处理(Pandas) → 数据存储(SQLite)
       ↓              ↓                  ↓
数据分析(NumPy) → AI分析(LLM) → API服务(FastAPI)
```

### 技术栈整合
- 装饰器：计时、缓存、重试
- 异步：数据采集、API调用
- Pandas：数据处理、技术指标
- NumPy：数值计算、统计分析
- FastAPI：RESTful API服务
- SQLAlchemy：数据库操作
- LLM API：新闻摘要、情绪分析

---

## 学习心得

### 掌握的技能
1. Python 高级语法应用
2. 数据处理和分析能力
3. Web API 开发能力
4. AI API 调用和集成
5. 项目架构设计能力

### 需要加强
1. 异步编程实战经验
2. 大规模数据处理优化
3. API 安全和性能
4. LLM Prompt 工程
5. 项目部署和运维

---

## Month 2 预热

### 下月学习方向
- LangChain 框架
- Agent 开发
- RAG 系统
- 向量数据库

### 准备工作
- [ ] 复习 Python 异步编程
- [ ] 深入理解 LLM API 调用
- [ ] 安装 LangChain 环境
- [ ] 了解向量数据库概念

---

## 学习资源汇总

### 官方文档
- Python: https://docs.python.org/zh-cn/3/
- NumPy: https://numpy.org/doc/stable/
- Pandas: https://pandas.pydata.org/docs/
- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- OpenAI: https://platform.openai.com/docs/

### 推荐书籍
- 《Python编程：从入门到实践》
- 《利用Python进行数据分析》
- 《FastAPI入门到实战》

---

**Month 1 完成！准备进入 Month 2 LangChain 学习！** 🎉