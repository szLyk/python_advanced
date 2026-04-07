# Day 18: JWT 认证

## 学习目标

掌握 JWT 认证机制，实现安全的 API 用户认证和授权。

## 知识点

### 1. JWT 简介

JWT (JSON Web Token) 是一种开放标准（RFC 7519）：
- 用于安全传输信息的令牌
- 由三部分组成：Header.Payload.Signature
- 自包含：携带用户信息
- 无状态：服务器不需要存储 session

### 2. JWT 结构

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

分解：
Header:    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
Payload:   eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ
Signature: SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

### 3. JWT 使用流程

```
1. 用户登录 → 服务器验证
2. 服务器生成 JWT → 返回给客户端
3. 客户端存储 JWT（localStorage/cookie）
4. 后续请求携带 JWT（Authorization: Bearer <token>）
5. 服务器验证 JWT → 处理请求
```

### 4. Python JWT 库

```python
from datetime import datetime, timedelta
import jwt

# 配置
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 创建 Token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 验证 Token
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token 过期
    except jwt.InvalidTokenError:
        return None  # Token 无效
```

### 5. FastAPI JWT 集成

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return payload.get("sub")

@app.get("/protected")
async def protected_route(user: str = Depends(get_current_user)):
    return {"user": user}
```

### 6. OAuth2 密码模式

```python
from fastapi.security import OAuth2PasswordRequestForm

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 验证用户
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(401, detail="Invalid credentials")

    # 生成 Token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
```

### 7. 密码哈希

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 哈希密码
hashed_password = pwd_context.hash("plain_password")

# 验证密码
is_valid = pwd_context.verify("plain_password", hashed_password)
```

### 8. 完整认证流程

```python
# 用户表
class User(BaseModel):
    username: str
    hashed_password: str
    disabled: bool = False

users_db = {
    "alice": {
        "username": "alice",
        "hashed_password": pwd_context.hash("secret"),
        "disabled": False
    }
}

# 认证流程
def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if not user:
        return False
    if not pwd_context.verify(password, user["hashed_password"]):
        return False
    return user
```

### 9. 权限控制

```python
from typing import List

class TokenData(BaseModel):
    username: str
    roles: List[str] = []

def check_role(required_role: str):
    async def role_checker(user: dict = Depends(get_current_user)):
        if required_role not in user.get("roles", []):
            raise HTTPException(403, detail="Not enough permissions")
        return user
    return role_checker

@app.get("/admin-only")
async def admin_route(user = Depends(check_role("admin"))):
    return {"message": "Admin dashboard"}
```

## 练习任务

1. 创建用户模型和密码哈希
2. 实现 Token 生成和验证
3. 实现登录接口
4. 实现认证中间件
5. 实现角色权限控制

## 安全注意事项

- SECRET_KEY 必须保密，生产环境使用强随机字符串
- Token 设置合理的过期时间
- 使用 HTTPS 传输
- 密码必须哈希存储
- 重要操作使用二次验证

## 运行练习

```bash
python jwt_auth.py
# 启动后访问 http://127.0.0.1:8000/docs 测试
```

## 参考资料

- JWT 官网：https://jwt.io/
- FastAPI 安全教程：https://fastapi.tiangolo.com/tutorial/security/
- OAuth2 规范：https://oauth.net/2/