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
    """练习 1: ndarray 创建与属性"""
    print("=" * 50)
    print("练习 1: ndarray 创建与属性")
    print("=" * 50)

    # 一维数组
    a = np.array([1, 2, 3, 4, 5])
    print(f"一维数组: {a}")
    print(f"  shape: {a.shape}, dtype: {a.dtype}, ndim: {a.ndim}, size: {a.size}")

    # 二维数组
    b = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"二维数组:\n{b}")
    print(f"  shape: {b.shape}, dtype: {b.dtype}, ndim: {b.ndim}, size: {b.size}")

    # 常用创建方法
    print(f"\nnp.zeros((3, 4)):\n{np.zeros((3, 4))}")
    print(f"\nnp.ones((2, 3)):\n{np.ones((2, 3))}")
    print(f"\nnp.arange(0, 10, 2): {np.arange(0, 10, 2)}")
    print(f"\nnp.linspace(0, 1, 5): {np.linspace(0, 1, 5)}")

    # 随机数组
    print(f"\nnp.random.rand(3, 2) (均匀分布):\n{np.random.rand(3, 2)}")
    print(f"\nnp.random.randn(3) (正态分布): {np.random.randn(3)}")
    print(f"\nnp.random.randint(0, 100, 5): {np.random.randint(0, 100, 5)}")


def section_2_dtype_and_shape():
    """练习 2: 数据类型与形状操作"""
    print("\n" + "=" * 50)
    print("练习 2: 数据类型与形状操作")
    print("=" * 50)

    # 指定数据类型
    a = np.array([1, 2, 3], dtype=np.float32)
    print(f"指定 dtype=float32: {a}, dtype: {a.dtype}")

    b = np.array([1.5, 2.7, 3.9], dtype=np.int32)
    print(f"指定 dtype=int32: {b}, dtype: {b.dtype}")

    # 类型转换
    c = np.array([1, 2, 3])
    d = c.astype(np.float64)
    print(f"astype float64: {d}, dtype: {d.dtype}")

    # 形状操作
    e = np.arange(12)
    print(f"\n原始数组: {e}, shape: {e.shape}")

    f = e.reshape(3, 4)
    print(f"reshape(3, 4):\n{f}")

    g = e.reshape(2, 6)
    print(f"reshape(2, 6):\n{g}")

    # flatten
    h = f.flatten()
    print(f"flatten: {h}")

    # transpose
    print(f"\n原始 3x4:\n{f}")
    print(f"transpose (4x3):\n{f.T}")

    # resize vs reshape
    print(f"\nreshape 只返回视图，resize 改变原数组")
    i = np.arange(6)
    i.resize(2, 3)
    print(f"resize 后: {i}")


def section_3_indexing_and_slicing():
    """练习 3: 索引与切片"""
    print("\n" + "=" * 50)
    print("练习 3: 索引与切片")
    print("=" * 50)

    a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    print(f"数组:\n{a}")

    # 基本索引
    print(f"\na[0, 1] (第0行第1列): {a[0, 1]}")
    print(f"a[2, 3] (第2行第3列): {a[2, 3]}")

    # 切片
    print(f"\na[0, :] (第0行全部): {a[0, :]}")
    print(f"a[:, 0] (第0列全部): {a[:, 0]}")
    print(f"a[1:3, 1:3] (行1-2,列1-2):\n{a[1:3, 1:3]}")

    # 布尔索引（重点！股票场景常用）
    prices = np.array([10, 15, 8, 20, 12, 25, 18])
    print(f"\n价格数组: {prices}")
    print(f"价格 > 15: {prices[prices > 15]}")
    print(f"价格 < 12: {prices[prices < 12]}")
    print(f"价格在 12-20 之间: {prices[(prices >= 12) & (prices <= 20)]}")

    # 花式索引
    print(f"\n花式索引 a[[0, 2], [1, 3]]: {a[[0, 2], [1, 3]]}")
    print(f"a[[0, 1], :] (取第0和第1行):\n{a[[0, 1], :]}")


def section_4_broadcasting():
    """练习 4: 广播机制"""
    print("\n" + "=" * 50)
    print("练习 4: 广播机制")
    print("=" * 50)

    # 案例 1: 二维 + 一维
    a = np.array([[1, 2, 3], [4, 5, 6]])  # shape: (2, 3)
    b = np.array([10, 20, 30])            # shape: (3,)
    print(f"a (2x3):\n{a}")
    print(f"b (1x3): {b}")
    print(f"a + b (广播结果):\n{a + b}")

    # 案例 2: 列向量广播
    c = np.array([[1], [2], [3]])  # shape: (3, 1)
    d = np.array([10, 20])         # shape: (2,)
    print(f"\nc (3x1):\n{c}")
    print(f"d (2): {d}")
    print(f"c + d (广播结果):\n{c + d}")

    # 案例 3: 标量广播
    e = np.array([1, 2, 3, 4, 5])
    print(f"\ne: {e}")
    print(f"e * 10 (标量广播): {e * 10}")
    print(f"e + 100: {e + 100}")

    # 广播规则解释
    print("\n广播规则:")
    print("1. 维度从右对齐")
    print("2. 对应维度相等或其中一个为1")
    print("3. 为1的维度会广播扩展")


def section_5_math_operations():
    """练习 5: 数学运算"""
    print("\n" + "=" * 50)
    print("练习 5: 数学运算")
    print("=" * 50)

    a = np.array([1, 2, 3, 4, 5])
    b = np.array([10, 20, 30, 40, 50])

    # 基本运算
    print(f"a: {a}")
    print(f"b: {b}")
    print(f"a + b: {a + b}")
    print(f"a - b: {a - b}")
    print(f"a * b: {a * b}")
    print(f"a / b: {a / b}")
    print(f"a ** 2 (平方): {a ** 2}")

    # 统计函数
    c = np.array([10, 15, 12, 18, 14, 20, 16])
    print(f"\n数据: {c}")
    print(f"sum: {c.sum()}")
    print(f"mean: {c.mean():.2f}")
    print(f"max: {c.max()}")
    print(f"min: {c.min()}")
    print(f"std (标准差): {c.std():.2f}")
    print(f"var (方差): {c.var():.2f}")

    # 轴向统计
    d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(f"\n二维数组:\n{d}")
    print(f"sum(axis=0) 每列求和: {d.sum(axis=0)}")
    print(f"sum(axis=1) 每行求和: {d.sum(axis=1)}")
    print(f"mean(axis=0) 每列均值: {d.mean(axis=0)}")

    # 数学函数
    e = np.array([1, 2, 3, 4])
    print(f"\n数学函数:")
    print(f"np.sqrt({e}): {np.sqrt(e)}")
    print(f"np.exp({e}): {np.exp(e)}")
    print(f"np.log({e}): {np.log(e)}")
    print(f"np.abs([-1, -2, -3]): {np.abs(np.array([-1, -2, -3]))}")

    # 比较运算
    f = np.array([10, 15, 12, 18, 14])
    print(f"\n比较运算:")
    print(f"f > 13: {f > 13}")
    print(f"f == 12: {f == 12}")
    print(f"(f > 12) & (f < 16): {(f > 12) & (f < 16)}")


def section_6_stock_application():
    """练习 6: 股票场景应用"""
    print("\n" + "=" * 50)
    print("练习 6: 股票场景应用")
    print("=" * 50)

    # 模拟 7 天股价
    prices = np.array([10.5, 11.2, 10.8, 12.0, 11.5, 13.0, 12.8])
    print(f"7天股价: {prices}")

    # 涨跌幅计算
    changes = (prices[1:] - prices[:-1]) / prices[:-1] * 100
    print(f"涨跌幅(%): {changes}")

    # 筛选大涨大跌
    big_up = changes[changes > 2]
    big_down = changes[changes < -2]
    print(f"涨幅>2%的天数: {big_up}")
    print(f"跌幅<-2%的天数: {big_down}")

    # 基础统计
    print(f"\n基础统计:")
    print(f"  平均价格: {prices.mean():.2f}")
    print(f"  最高价: {prices.max():.2f}")
    print(f"  最低价: {prices.min():.2f}")
    print(f"  波动率(标准差): {prices.std():.2f}")
    print(f"  价格区间: {prices.max() - prices.min():.2f}")

    # 模拟成交量
    volumes = np.array([1000, 1200, 800, 1500, 1100, 2000, 1800])
    print(f"\n成交量: {volumes}")
    print(f"  平均成交量: {volumes.mean():.0f}")
    print(f"  最大成交量: {volumes.max()}")
    print(f"  成交量>1500的天数股价: {prices[volumes > 1500]}")

    # 多维数据：模拟3只股票5天价格
    multi_prices = np.array([
        [10.5, 11.0, 10.8, 12.0, 11.5],  # 股票A
        [20.0, 21.5, 19.8, 22.0, 21.0],  # 股票B
        [5.0, 5.2, 4.8, 5.5, 5.3],       # 股票C
    ])
    print(f"\n3只股票5天价格:\n{multi_prices}")
    print(f"每只股票均价: {multi_prices.mean(axis=1)}")
    print(f"每天市场均价: {multi_prices.mean(axis=0)}")
    print(f"每只股票最大波动(最高-最低): {multi_prices.max(axis=1) - multi_prices.min(axis=1)}")


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