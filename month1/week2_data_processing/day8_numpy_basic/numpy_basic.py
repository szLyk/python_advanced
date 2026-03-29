"""
Day 8: NumPy 基础

学习目标：
1. 理解 NumPy ndarray 数组
2. 掌握数组创建方法
3. 学会数组索引和切片
4. 理解广播机制
5. 掌握基本数组运算

作者：AI Agent 工程师学习者
日期：2026-03-30
"""

import numpy as np


# ============================================================
# 1. 创建数组
# ============================================================

def demo_array_creation():
    """演示数组创建"""
    print("=" * 50)
    print("1. 数组创建")
    print("=" * 50)

    # 从列表创建
    print("\n--- 从列表创建 ---")
    arr1 = np.array([1, 2, 3, 4, 5])
    arr2 = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"一维数组: {arr1}")
    print(f"二维数组:\n{arr2}")

    # 内置函数创建
    print("\n--- 内置函数创建 ---")
    zeros = np.zeros((3, 4))
    ones = np.ones((2, 3))
    eye = np.eye(3)
    print(f"zeros(3,4):\n{zeros}")
    print(f"ones(2,3):\n{ones}")
    print(f"eye(3):\n{eye}")

    # 等差/等分
    print("\n--- 等差/等分 ---")
    arange_arr = np.arange(0, 10, 2)
    linspace_arr = np.linspace(0, 1, 5)
    print(f"arange(0,10,2): {arange_arr}")
    print(f"linspace(0,1,5): {linspace_arr}")

    # 随机数组
    print("\n--- 随机数组 ---")
    random_arr = np.random.rand(3, 3)
    random_int = np.random.randint(0, 10, size=(3, 3))
    print(f"rand(3,3):\n{random_arr}")
    print(f"randint(0,10,3,3):\n{random_int}")


# ============================================================
# 2. 数组属性
# ============================================================

def demo_array_attributes():
    """演示数组属性"""
    print("\n" + "=" * 50)
    print("2. 数组属性")
    print("=" * 50)

    arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])

    print(f"数组:\n{arr}")
    print(f"shape (形状): {arr.shape}")
    print(f"ndim (维度数): {arr.ndim}")
    print(f"size (元素总数): {arr.size}")
    print(f"dtype (数据类型): {arr.dtype}")
    print(f"itemsize (元素字节): {arr.itemsize}")
    print(f"nbytes (总字节): {arr.nbytes}")


# ============================================================
# 3. 数组索引和切片
# ============================================================

def demo_indexing():
    """演示索引和切片"""
    print("\n" + "=" * 50)
    print("3. 数组索引和切片")
    print("=" * 50)

    # 一维数组索引
    print("\n--- 一维数组 ---")
    arr = np.array([10, 20, 30, 40, 50])
    print(f"数组: {arr}")
    print(f"arr[0]: {arr[0]}")
    print(f"arr[-1]: {arr[-1]}")
    print(f"arr[1:4]: {arr[1:4]}")
    print(f"arr[::2]: {arr[::2]}")

    # 二维数组索引
    print("\n--- 二维数组 ---")
    arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(f"数组:\n{arr}")
    print(f"arr[0, 0]: {arr[0, 0]}")
    print(f"arr[1, 2]: {arr[1, 2]}")
    print(f"arr[:, 0] (第一列): {arr[:, 0]}")
    print(f"arr[0, :] (第一行): {arr[0, :]}")
    print(f"arr[0:2, 1:3]:\n{arr[0:2, 1:3]}")

    # 布尔索引
    print("\n--- 布尔索引 ---")
    arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(f"数组: {arr}")
    print(f"arr > 5: {arr[arr > 5]}")
    print(f"偶数: {arr[arr % 2 == 0]}")
    print(f"3-8之间: {arr[(arr > 3) & (arr < 8)]}")


# ============================================================
# 4. 数组运算
# ============================================================

def demo_operations():
    """演示数组运算"""
    print("\n" + "=" * 50)
    print("4. 数组运算")
    print("=" * 50)

    # 基本运算
    print("\n--- 基本运算 ---")
    arr = np.array([1, 2, 3, 4, 5])
    print(f"数组: {arr}")
    print(f"arr + 10: {arr + 10}")
    print(f"arr * 2: {arr * 2}")
    print(f"arr ** 2: {arr ** 2}")

    # 数组间运算
    print("\n--- 数组间运算 ---")
    arr1 = np.array([1, 2, 3])
    arr2 = np.array([4, 5, 6])
    print(f"arr1: {arr1}, arr2: {arr2}")
    print(f"arr1 + arr2: {arr1 + arr2}")
    print(f"arr1 * arr2: {arr1 * arr2}")

    # 数学函数
    print("\n--- 数学函数 ---")
    arr = np.array([1, 2, 3, 4, 5])
    print(f"sqrt: {np.sqrt(arr)}")
    print(f"exp: {np.exp(arr)}")
    print(f"log: {np.log(arr)}")

    # 统计函数
    print("\n--- 统计函数 ---")
    arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(f"数组: {arr}")
    print(f"sum: {np.sum(arr)}")
    print(f"mean: {np.mean(arr)}")
    print(f"std: {np.std(arr):.4f}")
    print(f"max: {np.max(arr)}, min: {np.min(arr)}")
    print(f"argmax: {np.argmax(arr)}, argmin: {np.argmin(arr)}")
    print(f"cumsum: {np.cumsum(arr)}")


# ============================================================
# 5. 广播机制
# ============================================================

def demo_broadcasting():
    """演示广播机制"""
    print("\n" + "=" * 50)
    print("5. 广播机制")
    print("=" * 50)

    # 二维 + 一维
    print("\n--- 二维 + 一维 ---")
    matrix = np.array([[1, 2, 3], [4, 5, 6]])
    vector = np.array([10, 20, 30])
    print(f"matrix shape: {matrix.shape}")
    print(f"vector shape: {vector.shape}")
    result = matrix + vector
    print(f"结果:\n{result}")

    # 行广播
    print("\n--- 行广播 ---")
    matrix = np.array([[1, 2, 3], [4, 5, 6]])
    row = np.array([[10], [20]])
    print(f"matrix shape: {matrix.shape}")
    print(f"row shape: {row.shape}")
    result = matrix + row
    print(f"结果:\n{result}")

    # 列广播
    print("\n--- 列广播 ---")
    matrix = np.array([[1, 2, 3], [4, 5, 6]])
    col = np.array([100, 200])
    result = matrix + col.reshape(2, 1)
    print(f"结果:\n{result}")


# ============================================================
# 6. 数组形状操作
# ============================================================

def demo_shape_operations():
    """演示形状操作"""
    print("\n" + "=" * 50)
    print("6. 数组形状操作")
    print("=" * 50)

    # reshape
    print("\n--- reshape ---")
    arr = np.arange(12)
    print(f"原数组: {arr}")
    reshaped = arr.reshape(3, 4)
    print(f"reshape(3,4):\n{reshaped}")
    reshaped_auto = arr.reshape(2, -1)
    print(f"reshape(2,-1):\n{reshaped_auto}")

    # transpose
    print("\n--- transpose ---")
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"原数组:\n{arr}")
    print(f"转置:\n{arr.T}")

    # flatten vs ravel
    print("\n--- flatten vs ravel ---")
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    flat = arr.flatten()
    rav = arr.ravel()
    print(f"flatten: {flat}")
    print(f"ravel: {rav}")


# ============================================================
# 7. 实用函数
# ============================================================

def demo_utility_functions():
    """演示实用函数"""
    print("\n" + "=" * 50)
    print("7. 实用函数")
    print("=" * 50)

    # where
    print("\n--- where ---")
    arr = np.array([1, 2, 3, 4, 5])
    result = np.where(arr > 3, arr, 0)
    print(f"arr > 3 替换为 arr, 否则 0: {result}")

    # unique
    print("\n--- unique ---")
    arr = np.array([1, 2, 2, 3, 3, 3, 4, 4, 5])
    unique, counts = np.unique(arr, return_counts=True)
    print(f"唯一值: {unique}")
    print(f"计数: {counts}")

    # sort
    print("\n--- sort ---")
    arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])
    sorted_arr = np.sort(arr)
    indices = np.argsort(arr)
    print(f"原数组: {arr}")
    print(f"排序后: {sorted_arr}")
    print(f"排序索引: {indices}")

    # concatenate
    print("\n--- concatenate ---")
    arr1 = np.array([1, 2, 3])
    arr2 = np.array([4, 5, 6])
    combined = np.concatenate([arr1, arr2])
    print(f"arr1: {arr1}, arr2: {arr2}")
    print(f"连接: {combined}")


# ============================================================
# 8. 性能对比
# ============================================================

def demo_performance():
    """演示 NumPy vs Python 列表性能"""
    print("\n" + "=" * 50)
    print("8. 性能对比: NumPy vs Python 列表")
    print("=" * 50)

    import time

    n = 1000000

    # Python 列表
    start = time.time()
    py_list = list(range(n))
    py_result = [x * 2 for x in py_list]
    py_time = time.time() - start

    # NumPy
    start = time.time()
    np_arr = np.arange(n)
    np_result = np_arr * 2
    np_time = time.time() - start

    print(f"元素数量: {n}")
    print(f"Python 列表时间: {py_time:.4f}s")
    print(f"NumPy 数组时间: {np_time:.4f}s")
    print(f"NumPy 快了: {py_time / np_time:.2f} 倍")


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Day 8: NumPy 基础完整示例")
    print("=" * 60)

    demo_array_creation()
    demo_array_attributes()
    demo_indexing()
    demo_operations()
    demo_broadcasting()
    demo_shape_operations()
    demo_utility_functions()
    demo_performance()

    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)