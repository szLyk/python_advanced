"""
Day 8: NumPy 基础练习

练习内容：
1. ndarray 创建与属性
2. 数据类型与形状操作
3. 索引与切片
4. 广播机制
5. 数学运算
6. 股票场景应用
"""

import numpy as np


def section_1_array_creation():
    """练习 1: ndarray 创建与属性
    API:
    - np.array(): 从列表创建 NumPy 数组
    - shape: 数组形状 (如 (5,) 表示一维 5 个元素，(2,3) 表示 2 行 3 列)
    - dtype: 数据类型 (int32/int64/float32 等)
    - ndim: 维度数
    - size: 元素总数
    - np.zeros(): 创建全 0 数组
    - np.ones(): 创建全 1 数组
    - np.arange(): 生成等差数列 [start, stop)，步长 step
    - np.linspace(): 在区间内生成 num 个等间距点
    - np.random.rand(): [0,1) 均匀分布随机数
    - np.random.randn(): 标准正态分布随机数
    - np.random.randint(): 随机整数 [low, high)
    """
    print("=" * 50)
    print("练习 1: ndarray 创建与属性")
    print("=" * 50)

    # np.array: 从 Python list 创建数组
    a = np.array([1, 2, 3, 4, 5])  # 一维数组，shape=(5,)
    print(f"一维数组：{a}")
    print(f"  shape: {a.shape} (5 个元素的一维数组)")
    print(f"  dtype: {a.dtype} (整数类型)")
    print(f"  ndim: {a.ndim} (1 维)")
    print(f"  size: {a.size} (共 5 个元素)")

    # 二维数组：嵌套列表
    b = np.array([[1, 2, 3], [4, 5, 6]])  # shape=(2,3) 表示 2 行 3 列
    print(f"二维数组:\n{b}")
    print(f"  shape: {b.shape} (2 行 3 列)")
    print(f"  dtype: {b.dtype}")
    print(f"  ndim: {b.ndim} (2 维)")
    print(f"  size: {b.size} (共 6 个元素)")

    # np.zeros: 创建指定形状的全 0 数组
    print(f"\nnp.zeros((3, 4)): 创建 3 行 4 列的全 0 矩阵")
    print(np.zeros((3, 4)))

    # np.ones: 创建指定形状的全 1 数组
    print(f"\nnp.ones((2, 3)): 创建 2 行 3 列的全 1 矩阵")
    print(np.ones((2, 3)))

    # np.arange: 类似 range，生成 [start, stop) 步长为 step 的数组
    print(f"\nnp.arange(0, 10, 2): 生成 [0,10) 步长为 2 的数组")
    print(np.arange(0, 10, 2))  # [0, 2, 4, 6, 8]

    # np.linspace: 在 [start, stop] 区间生成 num 个等间距点
    print(f"\nnp.linspace(0, 1, 5): 在 [0,1] 区间生成 5 个等间距点")
    print(np.linspace(0, 1, 5))  # [0. , 0.25, 0.5 , 0.75, 1. ]

    # 随机数生成
    print(f"\nnp.random.rand(3, 2): 生成 3x2 的 [0,1) 均匀分布随机数")
    print(np.random.rand(3, 2))

    print(f"\nnp.random.randn(3): 生成 3 个标准正态分布 (均值=0, 方差=1) 随机数")
    print(np.random.randn(3))

    print(f"\nnp.random.randint(0, 100, 5): 生成 5 个 [0,100) 的随机整数")
    print(np.random.randint(0, 100, 5))


def section_2_dtype_and_shape():
    """练习 2: 数据类型与形状操作
    API:
    - dtype: 创建时指定数据类型 (float32, int32, float64 等)
    - astype(): 类型转换，返回新数组
    - reshape(): 改变数组形状，返回视图 (不修改原数组)
    - flatten(): 展平为一维数组，返回副本
    - .T: 转置 (行列互换)
    - resize(): 改变数组形状，直接修改原数组
    """
    print("\n" + "=" * 50)
    print("练习 2: 数据类型与形状操作")
    print("=" * 50)

    # 指定数据类型
    a = np.array([1, 2, 3], dtype=np.float32)  # 强制使用 float32
    print(f"指定 dtype=float32: {a}, dtype: {a.dtype}")

    b = np.array([1.5, 2.7, 3.9], dtype=np.int32)  # 浮点转整数会截断小数
    print(f"指定 dtype=int32 (浮点截断): {b}, dtype: {b.dtype}")

    # astype: 类型转换
    c = np.array([1, 2, 3])
    d = c.astype(np.float64)  # 转为 float64
    print(f"astype(float64): {d}, dtype: {d.dtype}")

    # reshape: 改变形状 (元素总数必须一致)
    e = np.arange(12)  # [0,1,2,...,11], shape=(12,)
    print(f"\n原始数组：{e}, shape: {e.shape}")

    f = e.reshape(3, 4)  # 变成 3 行 4 列
    print(f"reshape(3, 4):\n{f}")

    g = e.reshape(2, 6)  # 变成 2 行 6 列
    print(f"reshape(2, 6):\n{g}")

    # flatten: 展平为一维
    h = f.flatten()  # 返回副本
    print(f"flatten: {h}")

    # .T: 转置
    print(f"\n原始 3x4:\n{f}")
    print(f"f.T (转置为 4x3):\n{f.T}")

    # resize vs reshape
    print(f"\nreshape 只返回视图，resize 直接修改原数组")
    i = np.arange(6)  # [0,1,2,3,4,5]
    i.resize(2, 3)  # 直接修改 i
    print(f"resize(2,3) 后：{i}")


def section_3_indexing_and_slicing():
    """练习 3: 索引与切片
    API:
    - arr[i, j]: 访问第 i 行第 j 列元素
    - arr[i, :]: 取第 i 行全部
    - arr[:, j]: 取第 j 列全部
    - arr[start:end, start:end]: 切片
    - 布尔索引：arr[条件] 筛选满足条件的元素
    - 花式索引：arr[[i,j], [k,l]] 取指定位置
    """
    print("\n" + "=" * 50)
    print("练习 3: 索引与切片")
    print("=" * 50)

    a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    print(f"数组 (3 行 4 列):\n{a}")

    # 基本索引
    print(f"\na[0, 1]: 第 0 行第 1 列 = {a[0, 1]}")
    print(f"a[2, 3]: 第 2 行第 3 列 = {a[2, 3]}")

    # 切片
    print(f"\na[0, :]: 第 0 行全部 = {a[0, :]}")
    print(f"a[:, 0]: 第 0 列全部 = {a[:, 0]}")
    print(f"a[1:3, 1:3]: 行 1-2, 列 1-2 =\n{a[1:3, 1:3]}")

    # 布尔索引 (股票分析常用)
    prices = np.array([10, 15, 8, 20, 12, 25, 18])
    print(f"\n价格数组：{prices}")
    print(f"prices > 15: 筛选价格>15 = {prices[prices > 15]}")
    print(f"prices < 12: 筛选价格<12 = {prices[prices < 12]}")
    print(f"prices[(p>=12) & (p<=20)]: 12-20 之间 = {prices[(prices >= 12) & (prices <= 20)]}")

    # 花式索引
    print(f"\na[[0, 2], [1, 3]]: 取 (0,1) 和 (2,3) 位置 = {a[[0, 2], [1, 3]]}")
    print(f"a[[0, 1], :]: 取第 0 和第 1 行:\n{a[[0, 1], :]}")


def section_4_broadcasting():
    """练习 4: 广播机制
    广播规则:
    1. 维度从右对齐
    2. 对应维度相等或其中一个为 1 时可广播
    3. 为 1 的维度会自动扩展
    """
    print("\n" + "=" * 50)
    print("练习 4: 广播机制")
    print("=" * 50)

    # 案例 1: 二维 + 一维
    # a shape=(2,3), b shape=(3,) → b 广播到 (2,3)
    a = np.array([[1, 2, 3], [4, 5, 6]])  # shape: (2, 3)
    b = np.array([10, 20, 30])            # shape: (3,)
    print(f"a (2x3):\n{a}")
    print(f"b (3,): {b}")
    print(f"a + b (b 广播到每行):\n{a + b}")

    # 案例 2: 列向量广播
    # c shape=(3,1), d shape=(2,) → 广播到 (3,2)
    c = np.array([[1], [2], [3]])  # shape: (3, 1)
    d = np.array([10, 20])         # shape: (2,)
    print(f"\nc (3x1):\n{c}")
    print(f"d (2,): {d}")
    print(f"c + d (广播到 3x2):\n{c + d}")

    # 案例 3: 标量广播
    e = np.array([1, 2, 3, 4, 5])
    print(f"\ne: {e}")
    print(f"e * 10 (标量 10 广播到每个元素): {e * 10}")
    print(f"e + 100: {e + 100}")


def section_5_math_operations():
    """练习 5: 数学运算
    API:
    - 基本运算：+, -, *, /, ** (逐元素)
    - 统计：.sum(), .mean(), .max(), .min(), .std(), .var()
    - 轴向统计：axis=0 按列，axis=1 按行
    - 数学函数：np.sqrt(), np.exp(), np.log(), np.abs()
    - 比较运算：>, <, ==, &, | (返回布尔数组)
    """
    print("\n" + "=" * 50)
    print("练习 5: 数学运算")
    print("=" * 50)

    a = np.array([1, 2, 3, 4, 5])
    b = np.array([10, 20, 30, 40, 50])

    print(f"a: {a}")
    print(f"b: {b}")
    print(f"a + b (逐元素相加): {a + b}")
    print(f"a - b: {a - b}")
    print(f"a * b: {a * b}")
    print(f"a / b: {a / b}")
    print(f"a ** 2 (平方): {a ** 2}")

    # 统计函数
    c = np.array([10, 15, 12, 18, 14, 20, 16])
    print(f"\n数据：{c}")
    print(f"sum(): 总和 = {c.sum()}")
    print(f"mean(): 平均值 = {c.mean():.2f}")
    print(f"max(): 最大值 = {c.max()}")
    print(f"min(): 最小值 = {c.min()}")
    print(f"std(): 标准差 (波动程度) = {c.std():.2f}")
    print(f"var(): 方差 = {c.var():.2f}")

    # 轴向统计
    d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(f"\n二维数组:\n{d}")
    print(f"sum(axis=0): 每列求和 = {d.sum(axis=0)}")
    print(f"sum(axis=1): 每行求和 = {d.sum(axis=1)}")
    print(f"mean(axis=0): 每列均值 = {d.mean(axis=0)}")

    # 数学函数
    e = np.array([1, 2, 3, 4])
    print(f"\n数学函数:")
    print(f"np.sqrt(e): 平方根 = {np.sqrt(e)}")
    print(f"np.exp(e): e 的幂 = {np.exp(e)}")
    print(f"np.log(e): 自然对数 = {np.log(e)}")
    print(f"np.abs([-1,-2,-3]): 绝对值 = {np.abs(np.array([-1, -2, -3]))}")

    # 比较运算
    f = np.array([10, 15, 12, 18, 14])
    print(f"\n比较运算:")
    print(f"f > 13: {f > 13}")
    print(f"f == 12: {f == 12}")
    print(f"(f > 12) & (f < 16): {[(f > 12) & (f < 16)]}")


def section_6_stock_application():
    """练习 6: 股票场景应用
    实际应用示例:
    - 涨跌幅计算：(今日 - 昨日) / 昨日 * 100
    - 条件筛选：大涨 (>2%)、大跌 (<-2%)
    - 统计分析：均价、最高/最低、波动率
    - 成交量分析：高成交量对应的股价
    """
    print("\n" + "=" * 50)
    print("练习 6: 股票场景应用")
    print("=" * 50)

    # 模拟 7 天股价
    prices = np.array([10.5, 11.2, 10.8, 12.0, 11.5, 13.0, 12.8])
    print(f"7 天股价：{prices}")

    # 涨跌幅计算
    # prices[1:]: 第 2-7 天价格
    # prices[:-1]: 第 1-6 天价格
    # 计算：(今日 - 昨日) / 昨日 * 100
    changes = (prices[1:] - prices[:-1]) / prices[:-1] * 100
    print(f"涨跌幅 (%): {changes}")

    # 筛选大涨大跌
    big_up = changes[changes > 2]
    big_down = changes[changes < -2]
    print(f"涨幅>2%: {big_up}")
    print(f"跌幅<-2%: {big_down}")

    # 基础统计
    print(f"\n基础统计:")
    print(f"  平均价格：{prices.mean():.2f}")
    print(f"  最高价：{prices.max():.2f}")
    print(f"  最低价：{prices.min():.2f}")
    print(f"  波动率 (标准差): {prices.std():.2f}")
    print(f"  价格区间：{prices.max() - prices.min():.2f}")

    # 模拟成交量
    volumes = np.array([1000, 1200, 800, 1500, 1100, 2000, 1800])
    print(f"\n成交量：{volumes}")
    print(f"  平均成交量：{volumes.mean():.0f}")
    print(f"  最大成交量：{volumes.max()}")
    print(f"  成交量>1500 的天数股价：{prices[volumes > 1500]}")

    # 多维数据：3 只股票 5 天价格
    multi_prices = np.array([
        [10.5, 11.0, 10.8, 12.0, 11.5],  # 股票 A
        [20.0, 21.5, 19.8, 22.0, 21.0],  # 股票 B
        [5.0, 5.2, 4.8, 5.5, 5.3],       # 股票 C
    ])
    print(f"\n3 只股票 5 天价格:\n{multi_prices}")
    print(f"每只股票均价 (axis=1): {multi_prices.mean(axis=1)}")
    print(f"每天市场均价 (axis=0): {multi_prices.mean(axis=0)}")
    print(f"每只股票最大波动：{multi_prices.max(axis=1) - multi_prices.min(axis=1)}")


def main():
    """运行所有练习"""
    section_1_array_creation()
    section_2_dtype_and_shape()
    section_3_indexing_and_slicing()
    section_4_broadcasting()
    section_5_math_operations()
    section_6_stock_application()

    print("\n" + "=" * 50)
    print("✅ Day 8 NumPy 基础练习完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
