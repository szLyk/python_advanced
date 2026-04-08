# Day 16: Pydantic 数据验证

**状态：** ✅ 已完成

**完成时间：** 2026-04-09

## 学习目标

掌握 Pydantic 模型定义和数据验证，为 FastAPI 请求/响应提供类型安全保障。

## 知识点

### 1. Pydantic 简介

Pydantic 是 Python 数据验证库：
- 使用 Python 类型提示定义模型
- 自动验证输入数据
- 自动转换数据类型
- 提供详细的错误信息

### 2. BaseModel 基础

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str

# 自动验证和转换
user = User(name="Tom", age="25", email="tom@example.com")
print(user.age)  # 25 (自动转换为 int)

# 验证失败报错
User(name="Tom", age="invalid", email="tom@example.com")
# ValidationError: value is not a valid integer
```

### 3. 字段验证器

```python
from pydantic import BaseModel, Field, validator

class Stock(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=5, description="股票代码")
    price: float = Field(..., gt=0, description="股票价格（必须大于0）")
    volume: int = Field(default=0, ge=0, description="成交量")

    @validator('symbol')
    def symbol_uppercase(cls, v):
        return v.upper()

# Field 参数：
# ... 表示必填
# default 默认值
# gt/lt/ge/le 大于/小于/大于等于/小于等于
# min_length/max_length 字符串长度限制
```

### 4. 类型验证

```python
from typing import List, Optional, Dict, Union
from datetime import datetime

class StockData(BaseModel):
    symbol: str                          # 必填字符串
    name: Optional[str] = None           # 可选字符串
    prices: List[float]                  # 浮点数列表
    metadata: Dict[str, str]             # 字典
    value: Union[int, float]             # 可以是 int 或 float
    timestamp: datetime                  # 日期时间（自动解析）

# 字符串日期自动转换为 datetime
data = StockData(
    symbol="AAPL",
    prices=[150.0, 151.5],
    metadata={"sector": "Tech"},
    timestamp="2026-04-07T10:00:00"
)
```

### 5. 模型配置

```python
from pydantic import BaseModel, ConfigDict

class Stock(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,    # 自动去除空白
        str_to_lower=True,            # 自动转小写
        validate_assignment=True,     # 赋值时也验证
        extra="forbid"                # 禁止额外字段
    )

    symbol: str
    price: float

stock = Stock(symbol="AAPL", price=150.0)
stock.price = 200.0  # validate_assignment=True 会验证
stock.extra = "value"  # extra="forbid" 会报错
```

### 6. 嵌套模型

```python
class Address(BaseModel):
    city: str
    street: str

class Company(BaseModel):
    name: str
    address: Address  # 嵌套模型

# 自动解析嵌套数据
company = Company(
    name="Apple",
    address={"city": "Cupertino", "street": "One Apple Park Way"}
)
```

### 7. 模型方法

```python
class Stock(BaseModel):
    symbol: str
    price: float

    def to_dict(self) -> dict:
        return {"symbol": self.symbol, "price": self.price}

    @property
    def is_high_price(self) -> bool:
        return self.price > 1000

# 使用
stock = Stock(symbol="AAPL", price=150.0)
print(stock.model_dump())      # {"symbol": "AAPL", "price": 150.0}
print(stock.model_dump_json()) # '{"symbol": "AAPL", "price": 150.0}'
print(stock.is_high_price)     # False
```

### 8. 数据转换

```python
# 字典转模型
data = {"symbol": "AAPL", "price": 150.0}
stock = Stock.model_validate(data)

# JSON转模型
json_str = '{"symbol": "AAPL", "price": 150.0}'
stock = Stock.model_validate_json(json_str)

# 模型转字典
stock.model_dump()

# 模型转JSON
stock.model_dump_json()
```

### 9. 错误处理

```python
from pydantic import ValidationError

try:
    Stock(symbol="", price=-10)
except ValidationError as e:
    print(e.json())
    # 详细错误信息，可用于 API 返回
```

## 练习任务

1. 定义带验证器的股票模型
2. 实现嵌套模型（股票+公司信息）
3. 处理验证错误并返回友好信息
4. 实现自定义验证逻辑
5. 使用 model_dump() 和 model_validate()

## 股票场景应用

```python
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional

class StockPrice(BaseModel):
    """单日股价"""
    date: datetime
    open: float = Field(gt=0)
    close: float = Field(gt=0)
    high: float = Field(gt=0)
    low: float = Field(gt=0)
    volume: int = Field(ge=0)

    @validator('high')
    def high_ge_low(cls, v, values):
        if 'low' in values and v < values['low']:
            raise ValueError('high must >= low')
        return v

class Stock(BaseModel):
    """完整股票信息"""
    symbol: str = Field(min_length=1, max_length=5)
    name: str
    sector: Optional[str] = "unknown"
    prices: List[StockPrice] = []

    @validator('symbol')
    def uppercase(cls, v):
        return v.upper()
```

## 运行练习

```bash
python pydantic_validation.py
```

## 参考资料

- Pydantic 官方文档：https://docs.pydantic.dev/
- FastAPI Pydantic 集成：https://fastapi.tiangolo.com/tutorial/body/