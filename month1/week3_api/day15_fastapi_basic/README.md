# Day 15: FastAPI 基础

**状态：** ✅ 已完成

**完成时间：** 2026-04-08

## 学习目标

掌握 FastAPI 核心概念，能够创建 RESTful API 服务。

## 知识点

### 1. FastAPI 简介

FastAPI 是现代、高性能的 Python Web 框架：
- 基于 Starlette 和 Pydantic
- 自动生成 OpenAPI 文档（Swagger UI）
- 类型提示自动验证
- 异步支持，性能媲美 Go/Node.js

### 2. 基本应用结构

```python
from fastapi import FastAPI

app = FastAPI(
    title="股票分析 API",
    description="提供股票数据查询服务",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Welcome to Stock API"}

# 运行: uvicorn main:app --reload
```

### 3. 路径操作装饰器

```python
@app.get("/stocks/{symbol}")    # GET 查询
@app.post("/stocks")            # POST 创建
@app.put("/stocks/{symbol}")    # PUT 更新
@app.delete("/stocks/{symbol}") # DELETE 删除
@app.patch("/stocks/{symbol}")  # PATCH 部分更新
```

### 4. 路径参数

```python
@app.get("/stocks/{symbol}")
async def get_stock(symbol: str):
    return {"symbol": symbol, "price": 100.50}

# 类型验证自动生效
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}  # item_id 必须是整数
```

### 5. 查询参数

```python
@app.get("/stocks")
async def list_stocks(
    skip: int = 0,           # 默认值
    limit: int = 10,         # 默认值
    sector: str = None       # 可选参数
):
    return {"skip": skip, "limit": limit, "sector": sector}

# 访问: /stocks?skip=0&limit=5&sector=tech
```

### 6. 请求体（Request Body）

```python
from pydantic import BaseModel

class Stock(BaseModel):
    symbol: str
    name: str
    price: float
    sector: str = "unknown"  # 默认值

@app.post("/stocks")
async def create_stock(stock: Stock):
    return {"created": stock.symbol, "price": stock.price}
```

### 7. 响应模型

```python
from typing import List

@app.get("/stocks", response_model=List[Stock])
async def get_stocks():
    return [
        {"symbol": "AAPL", "name": "Apple", "price": 150.0},
        {"symbol": "GOOGL", "name": "Google", "price": 2800.0}
    ]

# 自动过滤响应字段、类型验证
```

### 8. 状态码

```python
from fastapi import HTTPException, status

@app.get("/stocks/{symbol}")
async def get_stock(symbol: str):
    if symbol not in ["AAPL", "GOOGL"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock {symbol} not found"
        )
    return {"symbol": symbol}

# 常用状态码
# 200 OK, 201 Created, 400 Bad Request
# 404 Not Found, 500 Internal Server Error
```

### 9. 启动与运行

```bash
# 安装
pip install fastapi uvicorn

# 开发模式（自动重载）
uvicorn main:app --reload

# 生产模式
uvicorn main:app --host 0.0.0.0 --port 8000

# 访问文档
http://127.0.0.1:8000/docs      # Swagger UI
http://127.0.0.1:8000/redoc     # ReDoc
```

## 练习任务

1. 创建基本 FastAPI 应用
2. 实现 GET/POST/PUT/DELETE 路由
3. 使用路径参数和查询参数
4. 定义请求体模型
5. 处理异常和返回正确状态码
6. 使用 Swagger UI 测试 API

## 股票场景应用

```python
# 模拟股票数据
stocks_db = {
    "AAPL": {"name": "Apple", "price": 150.0, "sector": "Tech"},
    "GOOGL": {"name": "Google", "price": 2800.0, "sector": "Tech"},
    "TSLA": {"name": "Tesla", "price": 750.0, "sector": "Auto"}
}

@app.get("/stocks/{symbol}")
async def get_stock_price(symbol: str):
    if symbol.upper() not in stocks_db:
        raise HTTPException(404, detail="Stock not found")
    return stocks_db[symbol.upper()]

@app.get("/stocks/search")
async def search_stocks(sector: str = None, min_price: float = None):
    results = stocks_db.values()
    if sector:
        results = [s for s in results if s["sector"] == sector]
    if min_price:
        results = [s for s in results if s["price"] >= min_price]
    return results
```

## 运行练习

```bash
# 运行基础练习
python fastapi_basic.py

# 启动 API 服务
uvicorn fastapi_basic:app --reload

# 浏览器访问
http://127.0.0.1:8000/docs
```

## 参考资料

- FastAPI 官方文档：https://fastapi.tiangolo.com/
- B 站：FastAPI 从入门到实战（尚硅谷）
- OpenAPI 规范：https://swagger.io/specification/