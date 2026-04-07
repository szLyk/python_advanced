# Week 2: 数据处理库

**状态：** ✅ 已完成

**完成时间：** 2026-04-08

## 本周目标
- [x] 掌握 NumPy 数组操作
- [x] 学会向量化计算（避免循环）
- [x] 掌握 Pandas DataFrame 操作
- [x] 学会数据清洗和预处理
- [x] 完成股票数据分析项目

## 学习计划

| 天数 | 主题 | 文件 | 状态 |
|------|------|------|------|
| Day 8 | NumPy 基础 | day8_numpy_basic/numpy_basic.py | ✅ |
| Day 9 | NumPy 进阶 | day9_numpy_advanced/numpy_advanced.py | ✅ |
| Day 10 | Pandas 基础 | day10_pandas_basic/pandas_basic.py | ✅ |
| Day 11 | Pandas 进阶 | day11_pandas_advanced/pandas_advanced.py | ✅ |
| Day 12 | 弹性/休息 | - | - |
| Day 13 | 综合项目 | day13_project/stock_analysis.py | ✅ |
| Day 14 | 休息 | - | - |

## 核心知识点

### NumPy
```python
import numpy as np

# 创建数组
arr = np.array([1, 2, 3, 4, 5])

# 数组运算（向量化）
result = arr * 2  # 所有元素乘2

# 广播机制
matrix = np.array([[1, 2], [3, 4]])
vector = np.array([10, 20])
result = matrix + vector  # 自动广播
```
- ndarray 多维数组
- 数组索引和切片
- 广播机制
- 向量化计算

### Pandas
```python
import pandas as pd

# 创建 DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['北京', '上海', '广州']
})

# 数据读取
df = pd.read_csv('data.csv')

# 数据筛选
result = df[df['age'] > 25]
```
- Series 和 DataFrame
- 数据读取和写入
- 数据筛选和过滤
- 分组聚合和透视表

## 学习资源
- B 站：pandas 从入门到实战（菜鸟教程）
- 书籍：《利用 Python 进行数据分析》
- NumPy 文档：https://numpy.org/doc/stable/
- Pandas 文档：https://pandas.pydata.org/docs/

## 学习心得

本周掌握了数据处理的核心技能：
1. NumPy 向量化计算大大提高了数据处理效率
2. Pandas 提供了丰富的数据操作方法
3. 股票数据分析项目巩固了所学知识
4. 为后续 API 开发和 AI 应用打下基础