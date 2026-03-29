# Day 8: NumPy 基础

## 学习目标
- [ ] 理解 NumPy ndarray 数组
- [ ] 掌握数组创建方法
- [ ] 学会数组索引和切片
- [ ] 理解广播机制
- [ ] 掌握基本数组运算

---

## 目录

- [1. NumPy 简介](#1-numpy-简介)
- [2. 创建数组](#2-创建数组)
- [3. 数组属性](#3-数组属性)
- [4. 数组索引和切片](#4-数组索引和切片)
- [5. 数组运算](#5-数组运算)
- [6. 广播机制](#6-广播机制)
- [7. 数组形状操作](#7-数组形状操作)
- [8. 实用函数](#8-实用函数)

---

## 1. NumPy 简介

### 什么是 NumPy？

NumPy 是 Python 科学计算的基础库，提供：
- **ndarray**：高效的多维数组对象
- **向量化运算**：避免 Python 循环，大幅提升性能
- **广播机制**：不同形状数组间的运算
- **数学函数**：线性代数、随机数、傅里叶变换等

### 为什么用 NumPy？

```python
# Python 列表 - 需要循环
list_data = [1, 2, 3, 4, 5]
result = [x * 2 for x in list_data]

# NumPy - 向量化运算（快 10-100 倍）
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
result = arr * 2  # 一行代码，所有元素乘2
```

---

## 2. 创建数组

### 从列表创建

```python
import numpy as np

# 一维数组
arr1 = np.array([1, 2, 3, 4, 5])

# 二维数组
arr2 = np.array([[1, 2, 3], [4, 5, 6]])

# 三维数组
arr3 = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
```

### 使用内置函数创建

```python
# 全零数组
zeros = np.zeros((3, 4))  # 3行4列

# 全一数组
ones = np.ones((2, 3))  # 2行3列

# 单位矩阵
eye = np.eye(3)  # 3x3 单位矩阵

# 等差数组
arange = np.arange(0, 10, 2)  # [0, 2, 4, 6, 8]

# 等分数组
linspace = np.linspace(0, 1, 5)  # [0, 0.25, 0.5, 0.75, 1]

# 随机数组
random_arr = np.random.rand(3, 3)  # 0-1 随机数
random_int = np.random.randint(0, 10, size=(3, 3))  # 整数随机数
```

### 创建特定类型数组

```python
# 指定数据类型
arr_int = np.array([1, 2, 3], dtype=np.int32)
arr_float = np.array([1, 2, 3], dtype=np.float64)

# 常用数据类型
# int8, int16, int32, int64
# float16, float32, float64
# bool, complex
```

---

## 3. 数组属性

```python
arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])

# 形状 (行数, 列数)
print(arr.shape)  # (2, 4)

# 维度数
print(arr.ndim)  # 2

# 元素总数
print(arr.size)  # 8

# 数据类型
print(arr.dtype)  # int64

# 每个元素大小（字节）
print(arr.itemsize)  # 8

# 总大小（字节）
print(arr.nbytes)  # 64 (8 elements * 8 bytes)
```

---

## 4. 数组索引和切片

### 一维数组索引

```python
arr = np.array([10, 20, 30, 40, 50])

# 单个元素
print(arr[0])   # 10
print(arr[-1])  # 50

# 切片
print(arr[1:4])   # [20, 30, 40]
print(arr[:3])    # [10, 20, 30]
print(arr[2:])    # [30, 40, 50]
print(arr[::2])   # [10, 30, 50] (步长为2)
```

### 二维数组索引

```python
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# 单个元素
print(arr[0, 0])  # 1
print(arr[1, 2])  # 6
print(arr[-1, -1])  # 9

# 行切片
print(arr[0])     # [1, 2, 3] (第一行)
print(arr[1, :])  # [4, 5, 6] (第二行)

# 列切片
print(arr[:, 0])  # [1, 4, 7] (第一列)
print(arr[:, 1])  # [2, 5, 8] (第二列)

# 区域切片
print(arr[0:2, 1:3])  # [[2, 3], [5, 6]]
```

### 布尔索引

```python
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# 条件筛选
print(arr[arr > 5])   # [6, 7, 8, 9, 10]
print(arr[arr % 2 == 0])  # [2, 4, 6, 8, 10]

# 多条件
print(arr[(arr > 3) & (arr < 8)])  # [4, 5, 6, 7]
```

---

## 5. 数组运算

### 基本运算（向量化）

```python
arr = np.array([1, 2, 3, 4, 5])

# 算术运算（所有元素）
print(arr + 10)   # [11, 12, 13, 14, 15]
print(arr - 1)    # [0, 1, 2, 3, 4]
print(arr * 2)    # [2, 4, 6, 8, 10]
print(arr / 2)    # [0.5, 1., 1.5, 2., 2.5]
print(arr ** 2)   # [1, 4, 9, 16, 25]

# 数组间运算
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
print(arr1 + arr2)  # [5, 7, 9]
print(arr1 * arr2)  # [4, 10, 18]
```

### 数学函数

```python
arr = np.array([1, 2, 3, 4, 5])

# 常用函数
print(np.sqrt(arr))   # 平方根
print(np.exp(arr))    # 指数
print(np.log(arr))    # 自然对数
print(np.log10(arr))  # 10为底对数

# 三角函数
angles = np.array([0, np.pi/2, np.pi])
print(np.sin(angles))
print(np.cos(angles))

# 绝对值、取整
arr = np.array([-1.5, -0.5, 0.5, 1.5])
print(np.abs(arr))      # [1.5, 0.5, 0.5, 1.5]
print(np.round(arr))    # [-2, -1, 0, 2]
print(np.floor(arr))    # [-2, -1, 0, 1]
print(np.ceil(arr))     # [-1, 0, 1, 2]
```

### 统计函数

```python
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# 基本统计
print(np.sum(arr))     # 55
print(np.mean(arr))    # 5.5
print(np.std(arr))     # 标准差
print(np.var(arr))     # 方差

# 最大最小
print(np.max(arr))     # 10
print(np.min(arr))     # 1
print(np.argmax(arr))  # 9 (最大值索引)
print(np.argmin(arr))  # 0 (最小值索引)

# 累积运算
print(np.cumsum(arr))  # [1, 3, 6, 10, 15, 21, 28, 36, 45, 55]
print(np.cumprod(arr)) # [1, 2, 6, 24, 120, ...]
```

---

## 6. 广播机制

### 广播规则

当运算两个不同形状的数组时，NumPy 会自动扩展较小的数组：

1. 比较维度，从后往前
2. 维度相等或其中一个为 1，可以广播
3. 维度不相等且都不为 1，报错

### 示例

```python
# 二维 + 一维
matrix = np.array([[1, 2, 3], [4, 5, 6]])  # shape: (2, 3)
vector = np.array([10, 20, 30])            # shape: (3,)

# vector 自动扩展为 (2, 3)
result = matrix + vector
# [[11, 22, 33], [14, 25, 36]]

# 行广播
matrix = np.array([[1, 2, 3], [4, 5, 6]])  # shape: (2, 3)
row = np.array([[10], [20]])               # shape: (2, 1)

result = matrix + row
# [[11, 12, 13], [24, 25, 26]]
```

---

## 7. 数组形状操作

### reshape - 改变形状

```python
arr = np.arange(12)  # [0, 1, 2, ..., 11]

# 改为 3x4
reshaped = arr.reshape(3, 4)

# 改为 2x6
reshaped = arr.reshape(2, 6)

# 自动计算某一维度
reshaped = arr.reshape(3, -1)  # -1 表示自动计算

# 展平
flattened = arr.reshape(-1)  # 或 arr.flatten()
```

### transpose - 转置

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

# 转置
transposed = arr.T  # 或 arr.transpose()
# [[1, 4], [2, 5], [3, 6]]
```

### flatten vs ravel

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

# flatten - 返回副本
flat = arr.flatten()

# ravel - 返回视图（尽可能）
rav = arr.ravel()
```

---

## 8. 实用函数

### where - 条件选择

```python
arr = np.array([1, 2, 3, 4, 5])

# 条件替换
result = np.where(arr > 3, arr, 0)
# [0, 0, 0, 4, 5]

# 多条件
result = np.where(arr > 3, '大', '小')
# ['小', '小', '小', '大', '大']
```

### unique - 唯一值

```python
arr = np.array([1, 2, 2, 3, 3, 3, 4, 4, 5])

# 唯一值
unique = np.unique(arr)  # [1, 2, 3, 4, 5]

# 返回索引
unique, indices = np.unique(arr, return_index=True)

# 返回计数
unique, counts = np.unique(arr, return_counts=True)
```

### sort - 排序

```python
arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])

# 排序（返回副本）
sorted_arr = np.sort(arr)  # [1, 1, 2, 3, 4, 5, 6, 9]

# 排序索引
indices = np.argsort(arr)  # [1, 3, 6, 0, 2, 4, 7, 5]

# 多维数组排序
arr2d = np.array([[3, 1, 4], [1, 5, 9]])
sorted_2d = np.sort(arr2d, axis=1)  # 按行排序
```

### concatenate - 数组连接

```python
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# 一维连接
combined = np.concatenate([arr1, arr2])  # [1, 2, 3, 4, 5, 6]

# 二维连接
arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6]])

# 按行连接（axis=0）
row_combined = np.concatenate([arr1, arr2], axis=0)
# [[1, 2], [3, 4], [5, 6]]

# 按列连接（axis=1）
arr2 = np.array([[5], [6]])
col_combined = np.concatenate([arr1, arr2], axis=1)
# [[1, 2, 5], [3, 4, 6]]
```

---

## 练习题

1. 创建一个 5x5 的矩阵，值为 1-25
2. 提取矩阵的第 2 行和第 3 列
3. 找出矩阵中大于 10 的所有元素
4. 计算矩阵的行平均值和列平均值
5. 将矩阵转置后与原矩阵相乘

---

## 学习资源
- NumPy 官方文档：https://numpy.org/doc/stable/
- B 站：NumPy 从入门到精通

## 今日产出
- [ ] numpy_basic.py（待完成）
- [ ] 学习笔记