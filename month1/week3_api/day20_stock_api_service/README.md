# Day 20: 综合项目 - 股票数据 API 服务

## 学习目标

将 Week 3 学习内容整合，构建完整的股票数据 API 服务。

## 项目概述

构建一个功能完整的股票数据 REST API 服务，包含：
- FastAPI 路由设计
- Pydantic 数据验证
- SQLAlchemy 数据持久化
- JWT 用户认证
- 完整的 CRUD 操作

## 项目结构

```
stock_api_service/
├── main.py              # FastAPI 主应用
├── config.py            # 配置文件
├── database.py          # 数据库连接
├── models.py            # SQLAlchemy 模型
├── schemas.py           # Pydantic 模型
├── auth.py              # JWT 认证
├── routers/
│   ├── stocks.py        # 股票路由
│   ├── users.py         # 用户路由
│   └── auth.py          # 认证路由
├── services/
│   └── stock_service.py # 股票业务逻辑
│   └── user_service.py  # 用户业务逻辑
├── requirements.txt     # 依赖包
└── README.md            # 项目说明
```

## API 功能

### 公开接口
- `GET /stocks` - 获取股票列表
- `GET /stocks/{symbol}` - 获取股票详情
- `GET /stocks/search` - 搜索股票

### 认证接口
- `POST /auth/login` - 用户登录
- `POST /auth/register` - 用户注册

### 用户接口（需认证）
- `GET /users/me` - 获取当前用户
- `PUT /users/me` - 更新用户信息

### 股票管理（需 admin 权限）
- `POST /stocks` - 创建股票
- `PUT /stocks/{symbol}` - 更新股票
- `DELETE /stocks/{symbol}` - 删除股票

### 历史数据（需认证）
- `GET /stocks/{symbol}/history` - 获取历史价格
- `POST /stocks/{symbol}/history` - 添加历史数据

## 数据库设计

### 用户表 (users)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| username | VARCHAR(50) | 用户名（唯一）|
| email | VARCHAR(100) | 邮箱 |
| hashed_password | VARCHAR(255) | 哈希密码 |
| role | VARCHAR(20) | 角色（user/admin）|
| created_at | DATETIME | 创建时间 |

### 股票表 (stocks)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| symbol | VARCHAR(5) | 股票代码（唯一）|
| name | VARCHAR(100) | 公司名称 |
| price | FLOAT | 当前价格 |
| sector | VARCHAR(50) | 所属行业 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### 历史价格表 (stock_history)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| stock_id | INTEGER | 股票ID（外键）|
| date | DATETIME | 日期 |
| open_price | FLOAT | 开盘价 |
| close_price | FLOAT | 收盘价 |
| high_price | FLOAT | 最高价 |
| low_price | FLOAT | 最低价 |
| volume | INTEGER | 成交量 |

## 技术要点

### 1. 项目配置
```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./stock.db"
    SECRET_KEY: str = "change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE: int = 30

    class Config:
        env_file = ".env"
```

### 2. 依赖注入
```python
# database.py
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 3. 路由组织
```python
# main.py
from fastapi import FastAPI
from routers import stocks, users, auth

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(stocks.router)
```

### 4. 错误处理
```python
from fastapi import HTTPException

class StockNotFound(HTTPException):
    def __init__(self, symbol):
        super().__init__(404, detail=f"Stock {symbol} not found")

class DuplicateStock(HTTPException):
    def __init__(self, symbol):
        super().__init__(400, detail=f"Stock {symbol} already exists")
```

## 运行方式

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn main:app --reload

# 访问文档
http://127.0.0.1:8000/docs
```

## 测试要点

1. 注册用户并登录获取 token
2. 使用 token 访问认证接口
3. 测试权限控制（user vs admin）
4. 测试 CRUD 操作
5. 测试错误处理

## 参考资料

- FastAPI 官方文档：https://fastapi.tiangolo.com/
- SQLAlchemy 文档：https://docs.sqlalchemy.org/
- 项目结构参考：https://github.com/tiangolo/full-stack-fastapi-template