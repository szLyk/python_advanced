"""
Day 20: 股票数据 API 服务 - 综合项目

整合 FastAPI + Pydantic + SQLAlchemy + JWT 认证
"""
import uvicorn
# ============================================
# config.py - 配置
# ============================================

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    DATABASE_URL: str = "sqlite:///./stock_api.db"
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    APP_NAME: str = "股票数据 API 服务"
    APP_VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"


settings = Settings()


# ============================================
# database.py - 数据库连接
# ============================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """获取数据库 Session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库"""
    Base.metadata.create_all(bind=engine)


# ============================================
# models.py - SQLAlchemy 模型
# ============================================

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="user")
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(username={self.username}, role={self.role})>"


class Stock(Base):
    """股票模型"""
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(5), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    sector = Column(String(50), default="unknown")
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    histories = relationship("StockHistory", back_populates="stock")

    def __repr__(self):
        return f"<Stock(symbol={self.symbol}, price={self.price})>"


class StockHistory(Base):
    """股票历史价格模型"""
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

    stock = relationship("Stock", back_populates="histories")

    def __repr__(self):
        return f"<StockHistory(date={self.date.date()}, close={self.close_price})>"


# ============================================
# schemas.py - Pydantic 模型
# ============================================

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


# 用户模型
class UserCreate(BaseModel):
    """用户注册"""
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(..., description="邮箱")
    password: str = Field(min_length=6, max_length=100)

    @field_validator('username')
    @classmethod
    def lowercase(cls, v):
        return v.lower()


class UserUpdate(BaseModel):
    """用户更新"""
    email: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6)


class UserResponse(BaseModel):
    """用户响应"""
    id: int
    username: str
    email: Optional[str]
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# Token 模型
class Token(BaseModel):
    """Token 响应"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token 数据"""
    username: Optional[str] = None
    role: str = "user"


# 股票模型
class StockCreate(BaseModel):
    """股票创建"""
    symbol: str = Field(min_length=1, max_length=5)
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    sector: Optional[str] = Field(default="unknown", max_length=50)
    description: Optional[str] = None

    @field_validator('symbol')
    @classmethod
    def uppercase(cls, v):
        return v.upper()


class StockUpdate(BaseModel):
    """股票更新"""
    name: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    sector: Optional[str] = None
    description: Optional[str] = None


class StockResponse(BaseModel):
    """股票响应"""
    id: int
    symbol: str
    name: str
    price: float
    sector: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class StockList(BaseModel):
    """股票列表响应"""
    total: int
    stocks: List[StockResponse]


# 历史价格模型
class HistoryCreate(BaseModel):
    """历史价格创建"""
    date: datetime
    open_price: float = Field(gt=0)
    close_price: float = Field(gt=0)
    high_price: float = Field(gt=0)
    low_price: float = Field(gt=0)
    volume: int = Field(default=0, ge=0)


class HistoryResponse(BaseModel):
    """历史价格响应"""
    id: int
    date: datetime
    open_price: float
    close_price: float
    high_price: float
    low_price: float
    volume: int

    model_config = {"from_attributes": True}


class HistoryList(BaseModel):
    """历史价格列表"""
    symbol: str
    total: int
    histories: List[HistoryResponse]


# ============================================
# auth.py - JWT 认证
# ============================================

from datetime import timedelta
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    """哈希密码"""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain, hashed)


def create_token(data: dict) -> str:
    """创建 JWT Token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Optional[TokenData]:
    """解码 Token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return TokenData(username=payload.get("sub"), role=payload.get("role", "user"))
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """获取当前用户"""
    token_data = decode_token(token)
    if not token_data:
        raise HTTPException(401, "无效的认证凭据", headers={"WWW-Authenticate": "Bearer"})

    user = db.query(User).filter(User.username == token_data.username).first()
    if not user:
        raise HTTPException(401, "用户不存在")

    if not user.is_active:
        raise HTTPException(403, "用户已禁用")

    return user


async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """获取管理员用户"""
    if current_user.role != "admin":
        raise HTTPException(403, "需要管理员权限")
    return current_user


# ============================================
# services.py - 业务逻辑
# ============================================

from sqlalchemy import func, and_, or_, desc
from sqlalchemy.orm import Session


class UserService:
    """用户服务"""

    @staticmethod
    def create(db: Session, user_data: UserCreate) -> User:
        """创建用户"""
        # 检查用户名是否存在
        if db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(400, "用户名已存在")

        # 检查邮箱是否存在
        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(400, "邮箱已存在")

        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            role="user"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate(db: Session, username: str, password: str) -> Optional[User]:
        """认证用户"""
        user = db.query(User).filter(User.username == username.lower()).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def update(db: Session, user: User, update_data: UserUpdate) -> User:
        """更新用户"""
        if update_data.email:
            user.email = update_data.email
        if update_data.password:
            user.hashed_password = hash_password(update_data.password)
        db.commit()
        db.refresh(user)
        return user


class StockService:
    """股票服务"""

    @staticmethod
    def create(db: Session, stock_data: StockCreate) -> Stock:
        """创建股票"""
        if db.query(Stock).filter(Stock.symbol == stock_data.symbol).first():
            raise HTTPException(400, f"股票 {stock_data.symbol} 已存在")

        stock = Stock(**stock_data.dict())
        db.add(stock)
        db.commit()
        db.refresh(stock)
        return stock

    @staticmethod
    def get_by_symbol(db: Session, symbol: str) -> Stock:
        """获取股票"""
        stock = db.query(Stock).filter(Stock.symbol == symbol.upper()).first()
        if not stock:
            raise HTTPException(404, f"股票 {symbol} 不存在")
        return stock

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100,
             sector: Optional[str] = None, min_price: Optional[float] = None) -> List[Stock]:
        """股票列表"""
        query = db.query(Stock)

        if sector:
            query = query.filter(Stock.sector == sector)
        if min_price:
            query = query.filter(Stock.price >= min_price)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def count(db: Session, sector: Optional[str] = None) -> int:
        """统计数量"""
        query = db.query(func.count(Stock.id))
        if sector:
            query = query.filter(Stock.sector == sector)
        return query.scalar()

    @staticmethod
    def update(db: Session, symbol: str, update_data: StockUpdate) -> Stock:
        """更新股票"""
        stock = StockService.get_by_symbol(db, symbol)
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(stock, field, value)
        db.commit()
        db.refresh(stock)
        return stock

    @staticmethod
    def delete(db: Session, symbol: str) -> bool:
        """删除股票"""
        stock = StockService.get_by_symbol(db, symbol)
        db.delete(stock)
        db.commit()
        return True

    @staticmethod
    def search(db: Session, keyword: str) -> List[Stock]:
        """搜索股票"""
        return db.query(Stock).filter(
            or_(
                Stock.symbol.like(f"%{keyword}%"),
                Stock.name.like(f"%{keyword}%")
            )
        ).all()


class HistoryService:
    """历史价格服务"""

    @staticmethod
    def add(db: Session, stock_id: int, history_data: HistoryCreate) -> StockHistory:
        """添加历史数据"""
        history = StockHistory(stock_id=stock_id, **history_data.dict())
        db.add(history)
        db.commit()
        db.refresh(history)
        return history

    @staticmethod
    def list(db: Session, stock_id: int, limit: int = 30) -> List[StockHistory]:
        """获取历史数据"""
        return db.query(StockHistory).filter(
            StockHistory.stock_id == stock_id
        ).order_by(desc(StockHistory.date)).limit(limit).all()


# ============================================
# main.py - FastAPI 应用
# ============================================

from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Day 20 综合项目 - FastAPI + Pydantic + SQLAlchemy + JWT"
)


# 初始化数据库
@app.on_event("startup")
async def startup():
    init_db()


# === 认证路由 ===

@app.post("/auth/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    return UserService.create(db, user_data)


@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """用户登录"""
    user = UserService.authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(401, "用户名或密码错误", headers={"WWW-Authenticate": "Bearer"})

    token = create_token({"sub": user.username, "role": user.role})
    return Token(access_token=token)


# === 用户路由 ===

@app.get("/users/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """获取当前用户"""
    return current_user


@app.put("/users/me", response_model=UserResponse)
def update_me(update_data: UserUpdate, current_user: User = Depends(get_current_user),
              db: Session = Depends(get_db)):
    """更新用户信息"""
    return UserService.update(db, current_user, update_data)


# === 股票路由（公开）===

@app.get("/stocks", response_model=StockList)
def list_stocks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sector: Optional[str] = None,
    min_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """股票列表"""
    stocks = StockService.list(db, skip, limit, sector, min_price)
    total = StockService.count(db, sector)
    return StockList(total=total, stocks=stocks)


@app.get("/stocks/search")
def search_stocks(keyword: str, db: Session = Depends(get_db)):
    """搜索股票"""
    return {"results": StockService.search(db, keyword)}


@app.get("/stocks/{symbol}", response_model=StockResponse)
def get_stock(symbol: str, db: Session = Depends(get_db)):
    """获取股票详情"""
    return StockService.get_by_symbol(db, symbol)


# === 股票路由（需认证）===

@app.get("/stocks/{symbol}/history", response_model=HistoryList)
def get_history(symbol: str, limit: int = 30,
                current_user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    """获取历史价格"""
    stock = StockService.get_by_symbol(db, symbol)
    histories = HistoryService.list(db, stock.id, limit)
    return HistoryList(symbol=stock.symbol, total=len(histories), histories=histories)


@app.post("/stocks/{symbol}/history", response_model=HistoryResponse, status_code=201)
def add_history(symbol: str, history_data: HistoryCreate,
                admin_user: User = Depends(get_admin_user),
                db: Session = Depends(get_db)):
    """添加历史数据（管理员）"""
    stock = StockService.get_by_symbol(db, symbol)
    return HistoryService.add(db, stock.id, history_data)


# === 股票管理（管理员）===

@app.post("/stocks", response_model=StockResponse, status_code=201)
def create_stock(stock_data: StockCreate, admin_user: User = Depends(get_admin_user),
                 db: Session = Depends(get_db)):
    """创建股票"""
    return StockService.create(db, stock_data)


@app.put("/stocks/{symbol}", response_model=StockResponse)
def update_stock(symbol: str, update_data: StockUpdate,
                 admin_user: User = Depends(get_admin_user),
                 db: Session = Depends(get_db)):
    """更新股票"""
    return StockService.update(db, symbol, update_data)


@app.delete("/stocks/{symbol}")
def delete_stock(symbol: str, admin_user: User = Depends(get_admin_user),
                 db: Session = Depends(get_db)):
    """删除股票"""
    StockService.delete(db, symbol)
    return {"deleted": symbol}


# === 统计接口 ===

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """统计信息"""
    total_stocks = db.query(func.count(Stock.id)).scalar()
    total_users = db.query(func.count(User.id)).scalar()
    avg_price = db.query(func.avg(Stock.price)).scalar()

    sector_stats = db.query(
        Stock.sector, func.count(Stock.id)
    ).group_by(Stock.sector).all()

    return {
        "total_stocks": total_stocks,
        "total_users": total_users,
        "avg_price": avg_price,
        "sectors": {s[0]: s[1] for s in sector_stats}
    }


# ============================================
# 主程序入口
# ============================================

if __name__ == "__main__":
    print("Day 20: 股票数据 API 服务")
    print("=" * 50)
    print(f"项目: {settings.APP_NAME}")
    print(f"版本: {settings.APP_VERSION}")
    print("=" * 50)
    print("\n启动服务...")
    print("API 文档: http://127.0.0.1:8000/docs")
    print("\n使用步骤:")
    print("1. 注册用户: POST /auth/register")
    print("2. 登录获取 Token: POST /auth/login")
    print("3. 使用 Token 访问认证接口")
    print("4. 管理员可创建/管理股票")

    uvicorn.run(app, host="127.0.0.1", port=8000)