"""
Day 9: NumPy 进阶

学习目标：
1. 掌握线性代数运算
2. 学会向量化优化技巧
3. 掌握高级数组操作
4. 理解 NumPy 内存管理

作者：AI Agent 工程师学习者
日期：2026-03-30
"""

import numpy as np


# ============================================================
# 1. 线性代数
# ============================================================

def demo_linear_algebra():
    """演示线性代数运算"""
    print("=" * 50)
    print("1. 线性代数")
    print("=" * 50)

    # 基本矩阵运算
    print("\n--- 基本矩阵运算 ---")
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    print(f"A:\n{A}")
    print(f"B:\n{B}")
    print(f"矩阵乘法 A @ B:\n{A @ B}")
    print(f"矩阵转置 A.T:\n{A.T}")
    print(f"矩阵求逆 inv(A):\n{np.linalg.inv(A)}")
    print(f"行列式 det(A): {np.linalg.det(A)}")

    # 求解线性方程组
    print("\n--- 求解线性方程组 ---")
    # Ax = b
    A = np.array([[3, 1], [1, 2]])
    b = np.array([9, 8])
    x = np.linalg.solve(A, b)
    print(f"A:\n{A}")
    print(f"b: {b}")
    print(f"解 x: {x}")
    print(f"验证 A @ x: {A @ x}")

    # 特征值和特征向量
    print("\n--- 特征值和特征向量 ---")
    A = np.array([[1, 2], [3, 4]])
    eigenvalues, eigenvectors = np.linalg.eig(A)
    print(f"特征值: {eigenvalues}")
    print(f"特征向量:\n{eigenvectors}")

    # SVD 分解
    print("\n--- SVD 分解 ---")
    A = np.array([[1, 2, 3], [4, 5, 6]])
    U, S, Vt = np.linalg.svd(A)
    print(f"U:\n{U}")
    print(f"S: {S}")
    print(f"Vt:\n{Vt}")


# ============================================================
# 2. 高级索引
# ============================================================

def demo_advanced_indexing():
    """演示高级索引"""
    print("\n" + "=" * 50)
    print("2. 高级索引")
    print("=" * 50)

    # 花式索引
    print("\n--- 花式索引 ---")
    arr = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    indices = [0, 2, 4, 6, 8]
    print(f"数组: {arr}")
    print(f"索引: {indices}")
    print(f"arr[indices]: {arr[indices]}")

    # 二维花式索引
    print("\n--- 二维花式索引 ---")
    arr2d = np.arange(12).reshape(3, 4)
    print(f"数组:\n{arr2d}")
    print(f"arr2d[[0, 2], [1, 3]]: {arr2d[[0, 2], [1, 3]]}")

    # np.take
    print("\n--- np.take ---")
    arr = np.array([10, 20, 30, 40, 50])
    print(f"take([0, 2, 4]): {np.take(arr, [0, 2, 4])}")

    # np.put
    print("\n--- np.put ---")
    arr = np.array([10, 20, 30, 40, 50])
    np.put(arr, [0, 2], [100, 300])
    print(f"put后: {arr}")


# ============================================================
# 3. 向量化优化
# ============================================================

def demo_vectorization():
    """演示向量化优化"""
    print("\n" + "=" * 50)
    print("3. 向量化优化")
    print("=" * 50)

    import time

    # 循环 vs 向量化
    print("\n--- 循环 vs 向量化 ---")
    n = 1000000

    # Python 循环
    start = time.time()
    result_loop = [x ** 2 + 2 * x + 1 for x in range(n)]
    time_loop = time.time() - start

    # NumPy 向量化
    start = time.time()
    x = np.arange(n)
    result_vector = x ** 2 + 2 * x + 1
    time_vector = time.time() - start

    print(f"元素数: {n}")
    print(f"循环时间: {time_loop:.4f}s")
    print(f"向量化时间: {time_vector:.4f}s")
    print(f"向量化快了: {time_loop / time_vector:.2f} 倍")

    # np.vectorize
    print("\n--- np.vectorize ---")
    def custom_func(x):
        if x > 0:
            return x ** 2
        return -x

    vec_func = np.vectorize(custom_func)
    arr = np.array([-3, -2, -1, 0, 1, 2, 3])
    print(f"数组: {arr}")
    print(f"向量化后: {vec_func(arr)}")


# ============================================================
# 4. 内存和性能优化
# ============================================================

def demo_memory_optimization():
    """演示内存优化"""
    print("\n" + "=" * 50)
    print("4. 内存和性能优化")
    print("=" * 50)

    # 数据类型优化
    print("\n--- 数据类型优化 ---")
    arr_default = np.array([1, 2, 3, 4, 5])
    arr_int8 = np.array([1, 2, 3, 4, 5], dtype=np.int8)
    arr_int32 = np.array([1, 2, 3, 4, 5], dtype=np.int32)

    print(f"默认 dtype: {arr_default.dtype}, 内存: {arr_default.nbytes} bytes")
    print(f"int8 dtype: {arr_int8.dtype}, 内存: {arr_int8.nbytes} bytes")
    print(f"int32 dtype: {arr_int32.dtype}, 内存: {arr_int32.nbytes} bytes")
    print(f"int8 比 int64 节省: {arr_default.nbytes / arr_int8.nbytes:.0f} 倍")

    # 视图 vs 副本
    print("\n--- 视图 vs 副本 ---")
    arr = np.array([1, 2, 3, 4, 5])
    view = arr[1:4]  # 视图
    copy = arr[1:4].copy()  # 副本

    print(f"原数组: {arr}")
    view[0] = 100
    print(f"修改视图后原数组: {arr}")
    copy[0] = 200
    print(f"修改副本后原数组: {arr}")

    # 检查是否共享内存
    print(f"视图共享内存: {np.shares_memory(arr, view)}")
    print(f"副本共享内存: {np.shares_memory(arr, copy)}")


# ============================================================
# 5. 常用技巧
# ============================================================

def demo_common_tricks():
    """演示常用技巧"""
    print("\n" + "=" * 50)
    print("5. 常用技巧")
    print("=" * 50)

    # np.where 多条件
    print("\n--- np.where 多条件 ---")
    arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    result = np.where(
        arr < 3, 'small',
        np.where(arr < 7, 'medium', 'large')
    )
    print(f"数组: {arr}")
    print(f"分类: {result}")

    # np.select 多条件
    print("\n--- np.select 多条件 ---")
    conditions = [
        arr < 3,
        (arr >= 3) & (arr < 7),
        arr >= 7
    ]
    choices = ['small', 'medium', 'large']
    result = np.select(conditions, choices)
    print(f"select 结果: {result}")

    # np.clip 截断
    print("\n--- np.clip 截断 ---")
    arr = np.array([1, 5, 10, 15, 20])
    clipped = np.clip(arr, 5, 15)
    print(f"原数组: {arr}")
    print(f"clip(5, 15): {clipped}")

    # np.percentile 分位数
    print("\n--- np.percentile 分位数 ---")
    arr = np.random.randn(1000)
    print(f"P25: {np.percentile(arr, 25):.4f}")
    print(f"P50 (median): {np.percentile(arr, 50):.4f}")
    print(f"P75: {np.percentile(arr, 75):.4f}")


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Day 9: NumPy 进阶完整示例")
    print("=" * 60)

    demo_linear_algebra()
    demo_advanced_indexing()
    demo_vectorization()
    demo_memory_optimization()
    demo_common_tricks()

    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)