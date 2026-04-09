"""
Day 17: SQLAlchemy ORM 练习

学习内容：数据库连接、模型定义、CRUD操作、查询技巧
"""

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    func,
    and_,
    or_,
    desc,
    select
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    Session,
    relationship
)
from datetime import datetime
from typing import List, Optional
from contextlib import contextmanager

# ============================================
# 1. 数据库配置
# ============================================

# SQLite（本地测试）
DATABASE_URL = "sqlite:///./stocks.db"

# 创建引擎
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite 特殊配置
)

# Session 工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 基类
Base = declarative_base()


# ============================================
# 2. 模型定义
# ============================================

class Stock(Base):
    """股票表"""
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(5), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    sector = Column(String(50), default="unknown")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    histories = relationship("StockHistory", back_populates="stock")

    def __repr__(self):
        return f"<Stock(symbol={self.symbol}, price={self.price})>"


class StockHistory(Base):
    """股票历史价格表"""
    __tablename__ = "stock_history"

    id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    open_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    volume = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    stock = relationship("Stock", back_populates="histories")

    def __repr__(self):
        return f"<StockHistory(date={self.date}, close={self.close_price})>"


# ============================================
# 3. Session 管理
# ============================================

@contextmanager
def get_db():
    """
    获取数据库 Session 的上下文管理器

    使用方式:
        with get_db() as db:
            db.query(Stock).all()
        # 出 with 块后自动 commit() 和 close()

    执行流程:
        ① 创建 Session → ② yield 交出控制权 → ③ with 块执行
        → ④ 回到 yield 继续 → ⑤ commit/rollback → ⑥ close

    异常处理:
        - 正常：yield → commit → close
        - 异常：yield → rollback → close → 抛出异常
    """
    db = SessionLocal()  # 【步骤 1】创建数据库会话连接
    try:
        yield db  # 【步骤 2】把 db 交给 with 块使用，暂停在这里
                  # 【步骤 4】with 块结束后，从这里继续执行
        db.commit()  # 【步骤 5】提交事务（成功时执行）
    except Exception:
        db.rollback()  # 【步骤 5】回滚事务（出错时执行）
        raise  # 重新抛出异常，让调用者知道
    finally:
        db.close()  # 【步骤 6】关闭连接（无论成功失败都执行）


def init_db():
    """初始化数据库（创建表）"""
    Base.metadata.create_all(bind=engine)
    print("数据库表已创建")


# ============================================
# 4. CRUD 操作示例
# ============================================

def create_stock(db: Session, symbol: str, name: str, price: float, sector: str = "unknown") -> Stock:
    """创建股票"""
    stock = Stock(
        symbol=symbol.upper(),
        name=name,
        price=price,
        sector=sector
    )
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock


def get_stock_by_symbol(db: Session, symbol: str) -> Optional[Stock]:
    """按代码查询股票"""
    return db.query(Stock).filter(Stock.symbol == symbol.upper()).first()


def get_stock_by_id(db: Session, stock_id: int) -> Optional[Stock]:
    """按ID查询股票"""
    return db.query(Stock).filter(Stock.id == stock_id).first()


def get_all_stocks(db: Session, skip: int = 0, limit: int = 100) -> List[Stock]:
    """获取所有股票（分页）"""
    return db.query(Stock).offset(skip).limit(limit).all()


def update_stock(db: Session, symbol: str, price: Optional[float] = None, sector: Optional[str] = None) -> Optional[Stock]:
    """更新股票"""
    stock = get_stock_by_symbol(db, symbol)
    if not stock:
        return None

    if price is not None:
        stock.price = price
    if sector is not None:
        stock.sector = sector

    stock.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(stock)
    return stock


def delete_stock(db: Session, symbol: str) -> bool:
    """删除股票"""
    stock = get_stock_by_symbol(db, symbol)
    if not stock:
        return False

    db.delete(stock)
    db.commit()
    return True


# ============================================
# 5. 历史数据操作
# ============================================

def add_stock_history(
    db: Session,
    stock_id: int,
    date: datetime,
    open_price: float,
    close_price: float,
    high_price: float,
    low_price: float,
    volume: int = 0
) -> StockHistory:
    """添加历史数据"""
    history = StockHistory(
        stock_id=stock_id,
        date=date,
        open_price=open_price,
        close_price=close_price,
        high_price=high_price,
        low_price=low_price,
        volume=volume
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


def get_stock_histories(db: Session, stock_id: int, limit: int = 30) -> List[StockHistory]:
    """获取股票历史数据"""
    return db.query(StockHistory).filter(
        StockHistory.stock_id == stock_id
    ).order_by(desc(StockHistory.date)).limit(limit).all()


# ============================================
# 6. 复杂查询示例
# ============================================

def query_by_sector(db: Session, sector: str) -> List[Stock]:
    """按行业查询"""
    return db.query(Stock).filter(Stock.sector == sector).all()


def query_by_price_range(db: Session, min_price: float, max_price: float) -> List[Stock]:
    """按价格范围查询"""
    return db.query(Stock).filter(
        and_(Stock.price >= min_price, Stock.price <= max_price)
    ).all()


def query_top_stocks(db: Session, limit: int = 10) -> List[Stock]:
    """按价格排序（最高）"""
    return db.query(Stock).order_by(desc(Stock.price)).limit(limit).all()


def query_search(db: Session, keyword: str) -> List[Stock]:
    """搜索（名称包含关键词）"""
    return db.query(Stock).filter(
        or_(
            Stock.name.like(f"%{keyword}%"),
            Stock.symbol.like(f"%{keyword}%")
        )
    ).all()


def get_statistics(db: Session) -> dict:
    """统计信息"""
    total_count = db.query(func.count(Stock.id)).scalar()
    avg_price = db.query(func.avg(Stock.price)).scalar()
    max_price = db.query(func.max(Stock.price)).scalar()
    min_price = db.query(func.min(Stock.price)).scalar()

    # 按行业统计
    sector_stats = db.query(
        Stock.sector,
        func.count(Stock.id).label("count"),
        func.avg(Stock.price).label("avg_price")
    ).group_by(Stock.sector).all()

    return {
        "total_count": total_count,
        "avg_price": avg_price,
        "max_price": max_price,
        "min_price": min_price,
        "sector_stats": [
            {"sector": s.sector, "count": s.count, "avg_price": s.avg_price}
            for s in sector_stats
        ]
    }


# ============================================
# 7. FastAPI 集成示例（伪代码）
# ============================================

"""
# FastAPI 中使用 SQLAlchemy

from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/stocks")
def list_stocks(db: Session = Depends(get_db_session)):
    return get_all_stocks(db)

@app.get("/stocks/{symbol}")
def get_stock(symbol: str, db: Session = Depends(get_db_session)):
    stock = get_stock_by_symbol(db, symbol)
    if not stock:
        raise HTTPException(404, detail="Stock not found")
    return stock

@app.post("/stocks")
def create_stock_api(stock_data: StockCreate, db: Session = Depends(get_db_session)):
    existing = get_stock_by_symbol(db, stock_data.symbol)
    if existing:
        raise HTTPException(400, detail="Stock already exists")
    return create_stock(db, **stock_data.dict())
"""


# ============================================
# 8. 演示代码
# ============================================

def demo_basic_crud():
    """演示基本 CRUD"""
    print("\n=== 基本 CRUD ===")

    with get_db() as db:
        # 清空测试数据
        db.query(StockHistory).delete()
        db.query(Stock).delete()
        db.commit()

        # 创建
        apple = create_stock(db, "AAPL", "Apple Inc.", 150.25, "Tech")
        google = create_stock(db, "GOOGL", "Google", 2800.50, "Tech")
        tesla = create_stock(db, "TSLA", "Tesla", 750.80, "Auto")

        print(f"创建股票: {apple.symbol} - {apple.name}")

        # 查询
        found = get_stock_by_symbol(db, "AAPL")
        print(f"查询结果: {found}")

        # 更新
        updated = update_stock(db, "AAPL", price=155.0)
        print(f"更新价格: {updated.price}")

        # 列表
        all_stocks = get_all_stocks(db)
        print(f"所有股票数量: {len(all_stocks)}")


def demo_history():
    """演示历史数据"""
    print("\n=== 历史数据 ===")

    with get_db() as db:
        stock = get_stock_by_symbol(db, "AAPL")
        if stock:
            # 添加历史数据
            from datetime import timedelta
            base_date = datetime(2026, 4, 1)

            for i in range(5):
                add_stock_history(
                    db,
                    stock_id=stock.id,
                    date=base_date + timedelta(days=i),
                    open_price=148 + i,
                    close_price=150 + i,
                    high_price=152 + i,
                    low_price=147 + i,
                    volume=5000000 + i * 100000
                )

            # 查询历史
            histories = get_stock_histories(db, stock.id, limit=5)
            print(f"历史数据数量: {len(histories)}")
            for h in histories[:3]:
                print(f"  {h.date.date()}: 开{h.open_price} 收{h.close_price}")


def demo_queries():
    """演示复杂查询"""
    print("\n=== 复杂查询 ===")

    with get_db() as db:
        # 按行业
        tech_stocks = query_by_sector(db, "Tech")
        print(f"科技股票: {[s.symbol for s in tech_stocks]}")

        # 价格范围
        mid_price = query_by_price_range(db, 100, 500)
        print(f"价格100-500: {[s.symbol for s in mid_price]}")

        # 排序
        top_stocks = query_top_stocks(db, limit=3)
        print(f"最高价格: {[(s.symbol, s.price) for s in top_stocks]}")

        # 搜索
        search_result = query_search(db, "App")
        print(f"搜索'App': {[s.symbol for s in search_result]}")


def demo_statistics():
    """演示统计"""
    print("\n=== 统计信息 ===")

    with get_db() as db:
        stats = get_statistics(db)
        print(f"总数量: {stats['total_count']}")
        print(f"平均价格: {stats['avg_price']:.2f}")
        print(f"最高价格: {stats['max_price']:.2f}")
        print(f"最低价格: {stats['min_price']:.2f}")

        for sector in stats['sector_stats']:
            print(f"行业 {sector['sector']}: {sector['count']} 只, 平均 {sector['avg_price']:.2f}")


# ============================================
# 主程序
# ============================================

if __name__ == "__main__":
    print("Day 17: SQLAlchemy ORM")

    # 初始化数据库
    init_db()

    # 运行演示
    demo_basic_crud()
    demo_history()
    demo_queries()
    demo_statistics()

    print("\n学习完成！")
    print("数据库文件: stocks.db")