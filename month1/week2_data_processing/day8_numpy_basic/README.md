# Day 8: NumPy 基础

## 学习目标

掌握 NumPy 核心概念，为后续 Pandas 和股票数据分析打下基础。

## 知识点

### 1. ndarray 创建与属性

```python
import numpy as np

# 创建数组
a = np.array([1, 2, 3])           # 一维
b = np.array([[1, 2], [3, 4]])    # 二维

# 常用创建方法
np.zeros((3, 4))      # 全零
np.ones((2, 3))       # 全一
np.arange(0, 10, 2)   # 步长创建 [0, 2, 4, 6, 8]
np.linspace(0, 1, 5)  # 等分 [0, 0.25, 0.5, 0.75, 1]

# 属性
a.shape    # 形状 (3,)
a.dtype    # 数据类型 int64
a.ndim     # 维度数 1
a.size     # 元素总数 3
```

### 2. 数据类型

```python
# 指定类型
np.array([1, 2, 3], dtype=np.float32)
np.array([1, 2, 3], dtype=np.int16)

# 类型转换
a.astype(np.float64)

# 常用类型
# int8, int16, int32, int64
# float16, float32, float64
# bool, complex64, complex128
```

### 3. 形状操作

```python
a = np.arange(12)  # [0..11]

# reshape
a.reshape(3, 4)    # 3行4列
a.reshape(2, 6)    # 2行6列

# flatten
b = a.reshape(3, 4)
b.flatten()        # 展平为一维

# transpose
b.T                # 转置 4行3列
```

### 4. 索引与切片

```python
a = np.array([[1, 2, 3], [4, 5, 6]])

# 基本索引
a[0, 1]      # 第0行第1列 → 2
a[1, :]      # 第1行全部 → [4, 5, 6]
a[:, 0]      # 第0列全部 → [1, 4]

# 布尔索引（股票场景常用）
prices = np.array([10, 15, 8, 20, 12])
prices[prices > 12]   # 筛选大于12 → [15, 20]

# 花式索引
a[[0, 1], [1, 2]]     # 取 (0,1) 和 (1,2) → [2, 6]
```

### 5. 广播机制

```python
a = np.array([[1, 2, 3], [4, 5, 6]])  # 2x3
b = np.array([10, 20, 30])            # 1x3

# 广播：b 自动扩展为 2x3
a + b   # [[11, 22, 33], [14, 25, 36]]

# 规则：
# 1. 维度从右对齐
# 2. 对应维度相等或其中一个为1
# 3. 为1的维度会广播扩展
```

### 6. 数学运算

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# 基本运算（逐元素）
a + b    # [5, 7, 9]
a - b    # [-3, -3, -3]
a * b    # [4, 10, 18]
a / b    # [0.25, 0.4, 0.5]

# 统计函数
a.sum()       # 6
a.mean()      # 2.0
a.max()       # 3
a.min()       # 1
a.std()       # 标准差

# 轴向统计（股票场景常用）
c = np.array([[1, 2, 3], [4, 5, 6]])
c.sum(axis=0)  # 每列求和 → [5, 7, 9]
c.sum(axis=1)  # 每行求和 → [6, 15]

# 数学函数
np.sqrt(a)     # 平方根
np.exp(a)      # 指数
np.log(a)      # 自然对数
np.abs(a)      # 绝对值
```

## 股票场景应用

```python
# 模拟股票价格数据
prices = np.array([10.5, 11.2, 10.8, 12.0, 11.5, 13.0, 12.5])

# 计算涨跌幅
changes = (prices[1:] - prices[:-1]) / prices[:-1] * 100

# 筛选涨幅超过2%的天数
up_days = changes[changes > 2]

# 基础统计
print(f"均价: {prices.mean():.2f}")
print(f"最高: {prices.max():.2f}")
print(f"最低: {prices.min():.2f}")
print(f"波动率(标准差): {prices.std():.2f}")
```

## 练习任务

1. 创建不同形状的数组（一维、二维、三维）
2. 练习 reshape、transpose、flatten
3. 使用布尔索引筛选数据
4. 理解广播机制，写出广播示例
5. 用 NumPy 计算模拟股票数据的基本统计

## 运行练习

```bash
python numpy_basic.py
```

## 参考资料

- NumPy 官方文档：https://numpy.org/doc/stable/
- NumPy 100题练习：https://github.com/rougier/numpy-100