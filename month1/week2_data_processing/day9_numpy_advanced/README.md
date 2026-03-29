# Day 9: NumPy 进阶

## 学习目标
- [ ] 掌握线性代数运算
- [ ] 学会向量化优化技巧
- [ ] 掌握高级数组操作
- [ ] 理解 NumPy 内存管理

---

## 目录

- [1. 线性代数](#1-线性代数)
- [2. 高级索引](#2-高级索引)
- [3. 向量化优化](#3-向量化优化)
- [4. 内存和性能优化](#4-内存和性能优化)

---

## 1. 线性代数

### 矩阵运算

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# 矩阵乘法
print(np.dot(A, B))     # 或 A @ B
# [[19, 22], [43, 50]]

# 矩阵转置
print(A.T)

# 矩阵求逆
print(np.linalg.inv(A))

# 行列式
print(np.linalg.det(A))

# 矩阵秩
print(np.linalg.matrix_rank(A))
```

### 矩阵分解

```python
# 特征值和特征向量
eigenvalues, eigenvectors = np.linalg.eig(A)

# SVD 分解
U, S, Vt = np.linalg.svd(A)

# QR 分解
Q, R = np.linalg.qr(A)

# Cholesky 分解（正定矩阵）
L = np.linalg.cholesky(A)
```

### 求解线性方程组

```python
# Ax = b
A = np.array([[1, 2], [3, 4]])
b = np.array([5, 6])

x = np.linalg.solve(A, b)
# 验证
print(np.allclose(A @ x, b))  # True
```

---

## 2. 高级索引

### 花式索引

```python
arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

# 选择特定索引
indices = [0, 2, 4, 6]
print(arr[indices])  # [10, 30, 50, 70]

# 二维花式索引
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(arr2d[[0, 2], [1, 2]])  # [2, 9]
```

### np.take 和 np.put

```python
arr = np.array([10, 20, 30, 40, 50])

# take - 按索引取值
print(np.take(arr, [0, 2, 4]))

# put - 按索引放值
np.put(arr, [0, 2], [100, 300])
print(arr)  # [100, 20, 300, 40, 50]
```

---

## 3. 向量化优化

### 避免循环

```python
# 不推荐
result = []
for i in range(1000):
    result.append(i ** 2)

# 推荐
result = np.arange(1000) ** 2
```

### np.vectorize

```python
def my_func(x):
    if x > 0:
        return x ** 2
    return x

# 向量化包装
vec_func = np.vectorize(my_func)
arr = np.array([-1, 2, -3, 4])
print(vec_func(arr))  # [-1, 4, -3, 16]
```

### np.fromiter

```python
# 从迭代器创建数组
def generate_data(n):
    for i in range(n):
        yield i ** 2

arr = np.fromiter(generate_data(10), dtype=np.int64)
```

---

## 4. 内存和性能优化

### 数据类型优化

```python
# 默认 int64 (8字节)
arr = np.array([1, 2, 3])  # dtype: int64

# 使用更小的类型
arr_int8 = np.array([1, 2, 3], dtype=np.int8)  # 1字节
arr_int32 = np.array([1, 2, 3], dtype=np.int32)  # 4字节

# 节省 75% 内存
```

### 视图 vs 副本

```python
arr = np.array([1, 2, 3, 4, 5])

# 视图（不复制数据，节省内存）
view = arr[1:3]

# 副本（复制数据）
copy = arr[1:3].copy()

# 修改视图会影响原数组
view[0] = 100
print(arr)  # [1, 100, 3, 4, 5]
```

---

## 练习题

1. 计算两个矩阵的乘积
2. 求解线性方程组
3. 使用向量化替代循环
4. 优化数组内存使用

## 学习资源
- NumPy 线性代数文档：https://numpy.org/doc/stable/reference/routines.linalg.html

## 今日产出
- [ ] numpy_advanced.py（待完成）
- [ ] 学习笔记