# Day 17: SQLAlchemy ORM

## 学习目标

掌握 SQLAlchemy ORM 操作，实现数据库 CRUD 功能，为 API 提供持久化存储。

## 知识点

### 1. SQLAlchemy 简介

SQLAlchemy 是 Python 最流行的 ORM 框架：
- 提供对象关系映射（ORM）
- 支持多种数据库（MySQL、PostgreSQL、SQLite等）
- 支持原生 SQL 和 ORM 两种方式
- FastAPI 官方推荐搭配

### 2. 连接配置

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite（开发测试）
engine = create_engine("sqlite:///stocks.db")

# MySQL
engine = create_engine(
    "mysql+pymysql://user:pass@localhost:3306/stock_db"
)

# PostgreSQL
engine = create_engine(
    "postgresql://user:pass@localhost:5432/stock_db"
)

# Session 工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### 3. 模型定义

```python
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(5), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    sector = Column(String(50), default="unknown")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### 4. CRUD 操作

```python
# 创建表
Base.metadata.create_all(bind=engine)

# 创建 Session
db = SessionLocal()

# Create（创建）
new_stock = Stock(symbol="AAPL", name="Apple", price=150.0)
db.add(new_stock)
db.commit()
db.refresh(new_stock)  # 获取自增ID等

# Read（读取）
stock = db.query(Stock).filter(Stock.symbol == "AAPL").first()
stocks = db.query(Stock).filter(Stock.price > 100).all()
count = db.query(Stock).count()

# Update（更新）
stock.price = 160.0
db.commit()

# Delete（删除）
db.delete(stock)
db.commit()

# 关闭 Session
db.close()
```

### 5. 查询技巧

```python
from sqlalchemy import and_, or_, desc, func

# 多条件查询
stocks = db.query(Stock).filter(
    and_(Stock.price > 100, Stock.sector == "Tech")
).all()

# 排序
stocks = db.query(Stock).order_by(desc(Stock.price)).all()

# 分页
stocks = db.query(Stock).offset(0).limit(10).all()

# 聚合统计
avg_price = db.query(func.avg(Stock.price)).scalar()
count = db.query(func.count(Stock.id)).scalar()

# 模糊搜索
stocks = db.query(Stock).filter(Stock.name.like("%Apple%")).all()

# IN 查询
symbols = ["AAPL", "GOOGL", "TSLA"]
stocks = db.query(Stock).filter(Stock.symbol.in_(symbols)).all()
```

### 6. 关系映射

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    stocks = relationship("Stock", back_populates="company")

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(5))
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="stocks")
```

### 7. FastAPI 集成

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/stocks")
def list_stocks(db: Session = Depends(get_db)):
    return db.query(Stock).all()

@app.post("/stocks")
def create_stock(stock: StockCreate, db: Session = Depends(get_db)):
    db_stock = Stock(**stock.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock
```

### 8. Pydantic 配合

```python
# Pydantic 模型用于 API
class StockCreate(BaseModel):
    symbol: str
    name: str
    price: float

class StockResponse(BaseModel):
    id: int
    symbol: str
    name: str
    price: float
    created_at: datetime

    class Config:
        from_attributes = True  # 支持从 ORM 模型转换
```

## 练习任务

1. 创建数据库连接和表结构
2. 实现 CRUD 基本操作
3. 练习复杂查询（过滤、排序、分页）
4. 实现 FastAPI + SQLAlchemy 集成
5. 使用 Pydantic 配合 ORM 模型

## 股票场景应用

```python
# 股票数据表设计
class Stock(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True)
    symbol = Column(String(5), unique=True)
    name = Column(String(100))
    price = Column(Float)
    sector = Column(String(50))

class StockHistory(Base):
    __tablename__ = "stock_history"
    id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    date = Column(DateTime)
    open = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    stock = relationship("Stock", backref="history")

# 批量插入历史数据
histories = [
    StockHistory(stock_id=1, date="2026-04-01", open=150, close=152, volume=5000),
    StockHistory(stock_id=1, date="2026-04-02", open=152, close=151, volume=6000),
]
db.add_all(histories)
db.commit()
```

## 运行练习

```bash
python sqlalchemy_crud.py
```

## 参考资料

- SQLAlchemy 官方文档：https://docs.sqlalchemy.org/
- FastAPI 数据库集成：https://fastapi.tiangolo.com/tutorial/sql-databases/