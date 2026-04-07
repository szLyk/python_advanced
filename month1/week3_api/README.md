# Week 3: API 开发

**状态：** 🔄 进行中

**当前进度**：Day 15 FastAPI 基础

## 学习目标

掌握 FastAPI Web 开发，能够构建完整的 RESTful API 服务。

## 知识点清单

- [ ] RESTful API 设计原则
- [ ] FastAPI 路由和请求处理
- [ ] Pydantic 数据验证
- [ ] SQLAlchemy ORM 操作
- [ ] JWT 认证机制
- [ ] API 权限控制

## 学习日程

| 天数 | 主题 | 文件 | 状态 |
|------|------|------|------|
| Day 15 | FastAPI 基础 | day15_fastapi_basic/ | 🔄 |
| Day 16 | Pydantic 验证 | day16_pydantic/ | ⏳ |
| Day 17 | SQLAlchemy ORM | day17_sqlalchemy/ | ⏳ |
| Day 18 | JWT 认证 | day18_jwt_auth/ | ⏳ |
| Day 19 | 弹性/休息 | - | - |
| Day 20 | 综合项目 | day20_stock_api_service/ | ⏳ |
| Day 21 | 休息 | - | - |

## 核心概念

### FastAPI 特点
- 现代、高性能 Python Web 框架
- 自动生成 OpenAPI 文档
- 类型提示自动验证
- 原生异步支持

### 技术栈
```
FastAPI（路由）
    ↓
Pydantic（数据验证）
    ↓
SQLAlchemy（数据库）
    ↓
JWT（认证）
```

## 学习资源

- FastAPI 官方文档：https://fastapi.tiangolo.com/
- B 站：FastAPI 从入门到实战（尚硅谷）
- SQLAlchemy 文档：https://docs.sqlalchemy.org/

## 本周产出

- fastapi_basic.py - FastAPI 基础练习
- pydantic_validation.py - Pydantic 验证练习
- sqlalchemy_crud.py - SQLAlchemy ORM 练习
- jwt_auth.py - JWT 认证练习
- stock_api_service/ - 综合项目

## 运行方式

```bash
# Day 15
cd day15_fastapi_basic
uvicorn fastapi_basic:app --reload

# Day 16-17 Python 文件可直接运行
python pydantic_validation.py
python sqlalchemy_crud.py

# Day 18-20 启动 API 服务
uvicorn jwt_auth:app --reload
uvicorn stock_api_service:app --reload
```