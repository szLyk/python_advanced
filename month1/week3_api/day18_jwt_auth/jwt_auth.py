"""
Day 18: JWT 认证练习

学习内容：JWT 生成/验证、密码哈希、OAuth2 集成、权限控制
"""

from datetime import datetime, timedelta
from typing import Optional, List
import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn


# ============================================
# 1. 配置
# ============================================

SECRET_KEY = "your-secret-key-change-in-production"  # 生产环境必须用强密钥
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ============================================
# 2. 密码哈希
# ============================================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """哈希密码"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


# ============================================
# 3. 模型定义
# ============================================

class User(BaseModel):
    """用户模型"""
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: bool = False
    roles: List[str] = ["user"]


class UserInDB(User):
    """数据库用户模型（含密码）"""
    hashed_password: str


class Token(BaseModel):
    """Token 响应模型"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token 数据模型"""
    username: Optional[str] = None
    roles: List[str] = []


# ============================================
# 4. 模拟用户数据库
# ============================================

fake_users_db = {
    "alice": {
        "username": "alice",
        "email": "alice@example.com",
        "full_name": "Alice Smith",
        "disabled": False,
        "roles": ["user", "admin"],
        "hashed_password": hash_password("alice123")
    },
    "bob": {
        "username": "bob",
        "email": "bob@example.com",
        "full_name": "Bob Johnson",
        "disabled": False,
        "roles": ["user"],
        "hashed_password": hash_password("bob456")
    },
    "inactive": {
        "username": "inactive",
        "email": "inactive@example.com",
        "disabled": True,
        "roles": ["user"],
        "hashed_password": hash_password("secret")
    }
}


# ============================================
# 5. JWT 操作
# ============================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建 Access Token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str) -> Optional[TokenData]:
    """解码并验证 Token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        roles: List[str] = payload.get("roles", [])

        if username is None:
            return None

        return TokenData(username=username, roles=roles)

    except jwt.ExpiredSignatureError:
        print("Token 已过期")
        return None
    except jwt.InvalidTokenError:
        print("Token 无效")
        return None


# ============================================
# 6. 用户认证函数
# ============================================

def get_user(db: dict, username: str) -> Optional[UserInDB]:
    """获取用户"""
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None


def authenticate_user(db: dict, username: str, password: str) -> Optional[UserInDB]:
    """认证用户"""
    user = get_user(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# ============================================
# 7. FastAPI 应用
# ============================================

app = FastAPI(
    title="JWT 认证示例",
    description="Day 18 学习 - JWT 认证",
    version="1.0.0"
)

# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ============================================
# 8. 认证依赖
# ============================================

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """获取当前用户"""
    token_data = decode_access_token(token)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """获取当前活跃用户"""
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已禁用"
        )
    return current_user


# ============================================
# 9. 权限检查
# ============================================

def require_role(required_role: str):
    """角色权限检查装饰器"""
    async def role_checker(current_user: User = Depends(get_current_active_user)):
        if required_role not in current_user.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"需要 {required_role} 权限"
            )
        return current_user
    return role_checker


# ============================================
# 10. API 路由
# ============================================

@app.get("/")
async def root():
    """根路由"""
    return {"message": "JWT 认证示例 API", "docs": "/docs"}


@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    用户登录

    - username: 用户名
    - password: 密码
    - 返回: access_token
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # 创建 Token（包含用户名和角色）
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "roles": user.roles},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    获取当前用户信息

    - 需要认证
    """
    return current_user


@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    """
    获取用户自己的数据

    - 需要认证
    """
    return [
        {"item_id": 1, "owner": current_user.username},
        {"item_id": 2, "owner": current_user.username}
    ]


@app.get("/admin/dashboard")
async def admin_dashboard(admin_user: User = Depends(require_role("admin"))):
    """
    管理员仪表盘

    - 需要 admin 角色
    """
    return {
        "message": "管理员仪表盘",
        "admin": admin_user.username,
        "total_users": len(fake_users_db),
        "users": list(fake_users_db.keys())
    }


@app.get("/admin/users")
async def list_users(admin_user: User = Depends(require_role("admin"))):
    """
    用户列表

    - 需要 admin 角色
    """
    users = []
    for username, data in fake_users_db.items():
        users.append({
            "username": username,
            "email": data.get("email"),
            "disabled": data.get("disabled"),
            "roles": data.get("roles")
        })
    return {"users": users}


# ============================================
# 11. 股票 API（需要认证）
# ============================================

# 模拟股票数据
stocks_db = {
    "AAPL": {"symbol": "AAPL", "name": "Apple", "price": 150.0},
    "GOOGL": {"symbol": "GOOGL", "name": "Google", "price": 2800.0},
    "TSLA": {"symbol": "TSLA", "name": "Tesla", "price": 750.0}
}


@app.get("/stocks", dependencies=[Depends(get_current_active_user)])
async def list_stocks():
    """
    获取股票列表

    - 需要认证
    """
    return {"stocks": list(stocks_db.values())}


@app.get("/stocks/{symbol}", dependencies=[Depends(get_current_active_user)])
async def get_stock(symbol: str):
    """
    获取股票详情

    - 需要认证
    """
    symbol = symbol.upper()
    if symbol not in stocks_db:
        raise HTTPException(404, detail="股票不存在")
    return stocks_db[symbol]


@app.post("/stocks")
async def create_stock(
    symbol: str,
    name: str,
    price: float,
    admin_user: User = Depends(require_role("admin"))
):
    """
    创建股票

    - 需要 admin 权限
    """
    symbol = symbol.upper()
    if symbol in stocks_db:
        raise HTTPException(400, detail="股票已存在")

    stocks_db[symbol] = {"symbol": symbol, "name": name, "price": price}
    return {"created": stocks_db[symbol], "by": admin_user.username}


# ============================================
# 12. 演示函数（非 API）
# ============================================

def demo_jwt_operations():
    """演示 JWT 操作"""
    print("\n=== JWT 操作演示 ===")

    # 创建 Token
    token = create_access_token(
        data={"sub": "alice", "roles": ["user", "admin"]}
    )
    print(f"生成的 Token: {token[:50]}...")

    # 解码 Token
    token_data = decode_access_token(token)
    print(f"Token 数据: username={token_data.username}, roles={token_data.roles}")

    # 过期 Token
    expired_token = create_access_token(
        data={"sub": "test"},
        expires_delta=timedelta(seconds=-1)
    )
    expired_data = decode_access_token(expired_token)
    print(f"过期 Token 验证结果: {expired_data}")


def demo_password_hash():
    """演示密码哈希"""
    print("\n=== 密码哈希演示 ===")

    password = "my_secret_password"
    hashed = hash_password(password)
    print(f"原始密码: {password}")
    print(f"哈希密码: {hashed}")

    # 验证
    is_valid = verify_password(password, hashed)
    print(f"验证正确密码: {is_valid}")

    is_invalid = verify_password("wrong_password", hashed)
    print(f"验证错误密码: {is_invalid}")


def demo_authenticate():
    """演示用户认证"""
    print("\n=== 用户认证演示 ===")

    # 正确认证
    user = authenticate_user(fake_users_db, "alice", "alice123")
    print(f"认证成功: {user.username}, roles={user.roles}")

    # 错误密码
    user = authenticate_user(fake_users_db, "alice", "wrong")
    print(f"错误密码认证: {user}")

    # 用户不存在
    user = authenticate_user(fake_users_db, "unknown", "pass")
    print(f"用户不存在认证: {user}")


# ============================================
# 主程序
# ============================================

if __name__ == "__main__":
    print("Day 18: JWT 认证")

    # 演示 JWT 操作
    demo_jwt_operations()
    demo_password_hash()
    demo_authenticate()

    # 启动 API 服务
    print("\n启动 API 服务...")
    print("API 文档: http://127.0.0.1:8000/docs")
    print("\n测试步骤:")
    print("1. 访问 /login（用户名: alice, 密码: alice123）")
    print("2. 获取 access_token")
    print("3. 点击 Authorize 按钮，输入 token")
    print("4. 访问 /users/me 查看用户信息")
    print("5. 访问 /admin/dashboard（alice 有 admin 权限）")

    uvicorn.run(app, host="127.0.0.1", port=8000)