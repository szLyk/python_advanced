"""
Day 15: FastAPI 基础练习

学习内容：路由、请求、响应、状态码
"""

from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# ============================================
# 1. 应用初始化
# ============================================

app = FastAPI(
    title="股票分析 API",
    description="Day 15 学习 - FastAPI 基础",
    version="1.0.0"
)


# ============================================
# 2. 数据模型定义
# ============================================

class Stock(BaseModel):
    """股票数据模型"""
    symbol: str
    name: str
    price: float
    sector: Optional[str] = "unknown"


class StockUpdate(BaseModel):
    """股票更新模型（部分字段可选）"""
    price: Optional[float] = None
    sector: Optional[str] = None


# ============================================
# 3. 模拟数据库
# ============================================

stocks_db: dict = {
    "AAPL": {"symbol": "AAPL", "name": "Apple Inc.", "price": 150.25, "sector": "Tech"},
    "GOOGL": {"symbol": "GOOGL", "name": "Google", "price": 2800.50, "sector": "Tech"},
    "TSLA": {"symbol": "TSLA", "name": "Tesla", "price": 750.80, "sector": "Auto"},
    "MSFT": {"symbol": "MSFT", "name": "Microsoft", "price": 300.00, "sector": "Tech"},
}


# ============================================
# 4. 基本路由示例
# ============================================

@app.get("/")
async def root():
    """根路由 - API 简介"""
    return {
        "message": "Welcome to Stock API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": "2026-04-07"}


# ============================================
# 5. CRUD 操作 - 股票管理
# ============================================

@app.get("/stocks", response_model=List[Stock])
async def list_stocks(
        skip: int = Query(0, ge=0, description="跳过数量"),
        limit: int = Query(10, ge=1, le=100, description="返回数量"),
        sector: Optional[str] = Query(None, description="行业筛选")
):
    """
    获取股票列表

    - skip: 跳过前 N 条记录
    - limit: 返回最多 N 条记录
    - sector: 按行业筛选
    """
    results = list(stocks_db.values())

    # 按行业筛选
    if sector:
        results = [s for s in results if s["sector"] == sector]

    # 分页
    return results[skip:skip + limit]


@app.get("/stocks/{symbol}", response_model=Stock)
async def get_stock(symbol: str):
    """
    获取单个股票信息

    - symbol: 股票代码（如 AAPL）
    """
    symbol = symbol.upper()
    if symbol not in stocks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock '{symbol}' not found"
        )
    return stocks_db[symbol]


@app.post("/stocks", response_model=Stock, status_code=status.HTTP_201_CREATED)
async def create_stock(stock: Stock):
    """
    创建新股票

    - 请求体包含股票完整信息
    """
    symbol = stock.symbol.upper()
    if symbol in stocks_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stock '{symbol}' already exists"
        )
    stocks_db[symbol] = stock.dict()
    return stocks_db[symbol]


@app.put("/stocks/{symbol}", response_model=Stock)
async def update_stock(symbol: str, stock: Stock):
    """
    完整更新股票信息

    - 替换所有字段
    """
    symbol = symbol.upper()
    if symbol not in stocks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock '{symbol}' not found"
        )
    stocks_db[symbol] = stock.dict()
    return stocks_db[symbol]


@app.patch("/stocks/{symbol}", response_model=Stock)
async def partial_update_stock(symbol: str, update: StockUpdate):
    """
    部分更新股票信息

    - 只更新提供的字段
    """
    symbol = symbol.upper()
    if symbol not in stocks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock '{symbol}' not found"
        )

    # 部分更新
    stored = stocks_db[symbol]
    update_data = update.dict(exclude_unset=True)
    for field, value in update_data.items():
        stored[field] = value

    stocks_db[symbol] = stored
    return stored


@app.delete("/stocks/{symbol}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stock(symbol: str):
    """
    删除股票

    - 返回 204 No Content
    """
    symbol = symbol.upper()
    if symbol not in stocks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock '{symbol}' not found"
        )
    del stocks_db[symbol]
    return None


# ============================================
# 6. 搜索功能
# ============================================

@app.get("/stocks/search")
async def search_stocks(
        min_price: Optional[float] = Query(None, ge=0, description="最低价格"),
        max_price: Optional[float] = Query(None, le=10000, description="最高价格"),
        name_contains: Optional[str] = Query(None, description="名称包含")
):
    """
    搜索股票

    - 支持价格范围和名称搜索
    """
    results = list(stocks_db.values())

    if min_price:
        results = [s for s in results if s["price"] >= min_price]

    if max_price:
        results = [s for s in results if s["price"] <= max_price]

    if name_contains:
        results = [s for s in results if name_contains.lower() in s["name"].lower()]

    return {
        "count": len(results),
        "results": results
    }


# ============================================
# 7. 统计接口
# ============================================

@app.get("/stocks/stats")
async def get_stock_stats():
    """获取股票统计信息"""
    prices = [s["price"] for s in stocks_db.values()]
    sectors = [s["sector"] for s in stocks_db.values()]

    return {
        "total_count": len(stocks_db),
        "avg_price": sum(prices) / len(prices),
        "max_price": max(prices),
        "min_price": min(prices),
        "sectors": list(set(sectors))
    }


# ============================================
# 主程序入口
# ============================================

if __name__ == "__main__":
    print("Day 15: FastAPI 基础")
    print("启动服务: uvicorn fastapi_basic:app --reload")
    print("API 文档: http://127.0.0.1:8000/docs")

    # 直接运行开发服务器
    uvicorn.run(app, host="127.0.0.1", port=8000)
