"""
Day 16: Pydantic 数据验证练习

学习内容：数据模型定义、字段验证、嵌套模型、错误处理
"""

from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
    ConfigDict,
    ValidationError
)
from typing import List, Optional, Dict, Union
from datetime import datetime
import json


# ============================================
# 1. 基础模型定义
# ============================================

class StockBasic(BaseModel):
    """基础股票模型"""
    symbol: str
    name: str
    price: float
    volume: int = 0  # 默认值

    # 配置
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True  # 赋值时也验证
    )


# ============================================
# 2. 字段验证器
# ============================================

class StockWithValidation(BaseModel):
    """带字段验证的股票模型"""
    symbol: str = Field(
        ...,
        min_length=1,
        max_length=5,
        description="股票代码（1-5字符）"
    )
    name: str = Field(
        ...,
        min_length=1,
        description="公司名称"
    )
    price: float = Field(
        ...,
        gt=0,
        le=100000,
        description="股票价格（0-100000）"
    )
    sector: Optional[str] = Field(
        default="unknown",
        description="所属行业"
    )
    volume: int = Field(
        default=0,
        ge=0,
        description="成交量（不能为负）"
    )

    @field_validator('symbol')
    @classmethod
    def symbol_uppercase(cls, v: str) -> str:
        """股票代码转大写"""
        return v.upper()

    @field_validator('sector')
    @classmethod
    def validate_sector(cls, v: Optional[str]) -> str:
        """验证行业"""
        valid_sectors = ["Tech", "Finance", "Health", "Auto", "Energy", "unknown"]
        if v and v not in valid_sectors:
            raise ValueError(f"Invalid sector: {v}. Valid: {valid_sectors}")
        return v or "unknown"


# ============================================
# 3. 嵌套模型
# ============================================

class CompanyInfo(BaseModel):
    """公司信息模型"""
    founded: Optional[int] = None
    employees: Optional[int] = None
    headquarters: Optional[str] = None


class StockPriceData(BaseModel):
    """单日价格数据"""
    date: datetime
    open: float = Field(gt=0)
    close: float = Field(gt=0)
    high: float = Field(gt=0)
    low: float = Field(gt=0)
    volume: int = Field(ge=0)

    @model_validator(mode='after')
    def validate_price_range(self):
        """验证最高价 >= 最低价"""
        if self.high < self.low:
            raise ValueError(f"high ({self.high}) must >= low ({self.low})")
        return self

    @property
    def change_pct(self) -> float:
        """涨跌幅"""
        return (self.close - self.open) / self.open * 100


class StockDetailed(BaseModel):
    """详细股票模型（嵌套）"""
    symbol: str = Field(min_length=1, max_length=5)
    name: str
    price: float = Field(gt=0)
    company: Optional[CompanyInfo] = None
    price_history: List[StockPriceData] = []

    @field_validator('symbol')
    @classmethod
    def uppercase(cls, v):
        return v.upper()


# ============================================
# 4. 复合类型验证
# ============================================

class StockAnalysis(BaseModel):
    """股票分析结果"""
    symbol: str
    metrics: Dict[str, float]  # 指标字典
    rating: Union[str, int]    # 可以是字符串或整数
    tags: List[str]            # 标签列表
    timestamp: datetime        # 时间戳（自动解析）

    @field_validator('rating')
    @classmethod
    def normalize_rating(cls, v):
        """统一评分格式"""
        if isinstance(v, int):
            ratings = {1: "Poor", 2: "Fair", 3: "Good", 4: "Excellent", 5: "Outstanding"}
            return ratings.get(v, "Unknown")
        return v


# ============================================
# 5. 模型继承
# ============================================

class StockCreate(BaseModel):
    """创建股票模型"""
    symbol: str = Field(min_length=1, max_length=5)
    name: str
    price: float = Field(gt=0)
    sector: str = "unknown"

    @field_validator('symbol')
    @classmethod
    def uppercase(cls, v):
        return v.upper()


class StockUpdate(BaseModel):
    """更新股票模型（所有字段可选）"""
    name: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    sector: Optional[str] = None


class StockResponse(BaseModel):
    """响应模型"""
    symbol: str
    name: str
    price: float
    sector: str
    created_at: datetime


# ============================================
# 6. 错误处理示例
# ============================================

def handle_validation_error(e: ValidationError) -> dict:
    """处理验证错误，返回友好信息"""
    errors = []
    for error in e.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })
    return {
        "success": False,
        "error_count": len(errors),
        "errors": errors
    }


# ============================================
# 7. 演示代码
# ============================================

def demo_basic_model():
    """演示基础模型"""
    print("\n=== 基础模型 ===")

    # 正常创建
    stock = StockBasic(symbol="AAPL", name="Apple", price=150.0)
    print(f"创建成功: {stock}")
    print(f"转字典: {stock.model_dump()}")

    # 自动类型转换
    stock2 = StockBasic(symbol="GOOGL", name="Google", price="2800")  # price 字符串
    print(f"自动转换: {stock2.price} (type: {type(stock2.price).__name__})")

    # 赋值验证
    stock.price = 200.0  # OK
    print(f"更新价格: {stock.price}")
    try:
        stock.price = "invalid"
    except ValidationError as e:
        print(f"赋值验证失败: {e.errors()[0]['msg']}")


def demo_field_validation():
    """演示字段验证"""
    print("\n=== 字段验证 ===")

    # 正常创建
    stock = StockWithValidation(
        symbol="aapl",  # 自动转大写
        name="Apple Inc.",
        price=150.0,
        sector="Tech"
    )
    print(f"验证成功: symbol={stock.symbol}")

    # 验证失败示例
    test_cases = [
        {"symbol": "", "name": "Test", "price": 100},  # symbol 太短
        {"symbol": "AAPL", "name": "Apple", "price": -10},  # price 负数
        {"symbol": "AAPL", "name": "Apple", "price": 100, "sector": "Invalid"},  # 无效行业
    ]

    for data in test_cases:
        try:
            StockWithValidation(**data)
        except ValidationError as e:
            print(f"验证失败: {data} -> {e.errors()[0]['msg']}")


def demo_nested_model():
    """演示嵌套模型"""
    print("\n=== 嵌套模型 ===")

    # 创建嵌套模型
    stock = StockDetailed(
        symbol="AAPL",
        name="Apple Inc.",
        price=150.0,
        company={
            "founded": 1976,
            "employees": 150000,
            "headquarters": "Cupertino, CA"
        },
        price_history=[
            {
                "date": "2026-04-05",
                "open": 148.0,
                "close": 150.5,
                "high": 151.0,
                "low": 147.5,
                "volume": 5000000
            },
            {
                "date": "2026-04-06",
                "open": 150.5,
                "close": 149.0,
                "high": 152.0,
                "low": 148.5,
                "volume": 6000000
            }
        ]
    )

    print(f"股票: {stock.symbol} - {stock.name}")
    print(f"公司: 成立于 {stock.company.founded}")
    print(f"历史价格数量: {len(stock.price_history)}")

    # 访问嵌套属性
    first_day = stock.price_history[0]
    print(f"第一天涨跌幅: {first_day.change_pct:.2f}%")

    # 价格范围验证失败
    try:
        StockPriceData(
            date="2026-04-07",
            open=100,
            close=105,
            high=95,  # high < low 会报错
            low=100,
            volume=1000
        )
    except ValidationError as e:
        print(f"价格验证失败: {e.errors()[0]['msg']}")


def demo_complex_types():
    """演示复杂类型"""
    print("\n=== 复杂类型 ===")

    analysis = StockAnalysis(
        symbol="AAPL",
        metrics={"pe_ratio": 25.5, "market_cap": 2.5e12},
        rating=4,  # 自动转 "Excellent"
        tags=["Tech", "Large Cap", "Blue Chip"],
        timestamp="2026-04-07T10:30:00"  # 自动解析
    )

    print(f"评级: {analysis.rating}")  # Excellent
    print(f"指标: {analysis.metrics}")
    print(f"时间戳: {analysis.timestamp}")
    print(f"标签: {analysis.tags}")


def demo_json_conversion():
    """演示 JSON 转换"""
    print("\n=== JSON 转换 ===")

    # 从 JSON 创建
    json_data = '{"symbol": "AAPL", "name": "Apple", "price": 150.0}'
    stock = StockBasic.model_validate_json(json_data)
    print(f"从JSON创建: {stock}")

    # 转 JSON
    json_output = stock.model_dump_json()
    print(f"转JSON: {json_output}")

    # 字典转换
    data = {"symbol": "GOOGL", "name": "Google", "price": 2800.0}
    stock2 = StockBasic.model_validate(data)
    print(f"从字典创建: {stock2}")


def demo_error_handling():
    """演示错误处理"""
    print("\n=== 错误处理 ===")

    try:
        StockWithValidation(
            symbol="TOOLONGSYMBOL",  # 超长
            name="Test",
            price=-100  # 负数
        )
    except ValidationError as e:
        error_info = handle_validation_error(e)
        print(f"错误数量: {error_info['error_count']}")
        for err in error_info['errors']:
            print(f"  - {err['field']}: {err['message']}")


# ============================================
# 主程序
# ============================================

if __name__ == "__main__":
    print("Day 16: Pydantic 数据验证")

    demo_basic_model()
    demo_field_validation()
    demo_nested_model()
    demo_complex_types()
    demo_json_conversion()
    demo_error_handling()

    print("\n学习完成！")