"""
Day 10: Pandas 基础

学习目标：
1. 理解 Series 和 DataFrame
2. 掌握数据创建和读取
3. 学会数据查看和筛选
4. 掌握基本数据操作

作者：AI Agent 工程师学习者
日期：2026-03-30
"""

import pandas as pd
import numpy as np


# ============================================================
# 1. Series
# ============================================================

def demo_series():
    """演示 Series"""
    print("=" * 50)
    print("1. Series")
    print("=" * 50)

    # 创建 Series
    print("\n--- 创建 Series ---")
    s1 = pd.Series([1, 2, 3, 4, 5])
    s2 = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
    s3 = pd.Series({'a': 10, 'b': 20, 'c': 30})
    print(f"从列表创建:\n{s1}")
    print(f"\n指定索引:\n{s2}")
    print(f"\n从字典创建:\n{s3}")

    # Series 属性
    print("\n--- Series 属性 ---")
    s = pd.Series([1, 2, 3, 4, 5], index=['a', 'b', 'c', 'd', 'e'])
    print(f"values: {s.values}")
    print(f"index: {s.index}")
    print(f"dtype: {s.dtype}")
    print(f"shape: {s.shape}")

    # Series 索引
    print("\n--- Series 索引 ---")
    print(f"s['a']: {s['a']}")
    print(f"s.iloc[0]: {s.iloc[0]}  # 使用 iloc 按位置索引")
    print(f"s[['a', 'c']]:\n{s[['a', 'c']]}")


# ============================================================
# 2. DataFrame
# ============================================================

def demo_dataframe():
    """演示 DataFrame"""
    print("\n" + "=" * 50)
    print("2. DataFrame")
    print("=" * 50)

    # 创建 DataFrame
    print("\n--- 创建 DataFrame ---")
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'David'],
        'age': [25, 30, 35, 40],
        'city': ['北京', '上海', '广州', '深圳'],
        'salary': [5000, 6000, 7000, 8000]
    })
    print(df)

    # DataFrame 属性
    print("\n--- DataFrame 属性 ---")
    print(f"shape: {df.shape}")
    print(f"columns: {df.columns.tolist()}")
    print(f"index: {df.index.tolist()}")
    print(f"dtypes:\n{df.dtypes}")


# ============================================================
# 3. 数据查看
# ============================================================

def demo_data_view():
    """演示数据查看"""
    print("\n" + "=" * 50)
    print("3. 数据查看")
    print("=" * 50)

    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, 40, 45],
        'city': ['北京', '上海', '广州', '深圳', '杭州'],
        'salary': [5000, 6000, 7000, 8000, 9000]
    })

    print("\n--- head/tail ---")
    print(f"head(3):\n{df.head(3)}")
    print(f"\ntail(2):\n{df.tail(2)}")

    print("\n--- info ---")
    print(df.info())

    print("\n--- describe ---")
    print(df.describe())

    print("\n--- 查看列 ---")
    print(f"df['name']:\n{df['name']}")
    print(f"\ndf[['name', 'age']]:\n{df[['name', 'age']]}")

    print("\n--- 查看行 ---")
    print(f"df.loc[0]:\n{df.loc[0]}")
    print(f"\ndf.iloc[1]:\n{df.iloc[1]}")
    print(f"\ndf.loc[0:2]:\n{df.loc[0:2]}")


# ============================================================
# 4. 数据筛选
# ============================================================

def demo_data_filter():
    """演示数据筛选"""
    print("\n" + "=" * 50)
    print("4. 数据筛选")
    print("=" * 50)

    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, 40, 45],
        'city': ['北京', '上海', '广州', '深圳', '杭州'],
        'salary': [5000, 6000, 7000, 8000, 9000]
    })

    print(f"原数据:\n{df}")

    print("\n--- 单条件筛选 ---")
    print(f"age > 30:\n{df[df['age'] > 30]}")

    print("\n--- 多条件筛选 ---")
    print(f"age > 30 且 city == '广州':\n{df[(df['age'] > 30) & (df['city'] == '广州')]}")

    print("\n--- isin 筛选 ---")
    print(f"city in ['北京', '上海']:\n{df[df['city'].isin(['北京', '上海'])]}")

    print("\n--- 字符串筛选 ---")
    print(f"name 包含 'li':\n{df[df['name'].str.contains('li')]}")
    print(f"name 以 'A' 开头:\n{df[df['name'].str.startswith('A')]}")


# ============================================================
# 5. 数据操作
# ============================================================

def demo_data_operations():
    """演示数据操作"""
    print("\n" + "=" * 50)
    print("5. 数据操作")
    print("=" * 50)

    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'David'],
        'age': [25, 30, 35, 40],
        'city': ['北京', '上海', '广州', '深圳']
    })

    print(f"原数据:\n{df}")

    # 添加列
    print("\n--- 添加列 ---")
    df['salary'] = [5000, 6000, 7000, 8000]
    df['age_plus_10'] = df['age'] + 10
    print(df)

    # 删除列
    print("\n--- 删除列 ---")
    df_drop = df.drop('age_plus_10', axis=1)
    print(df_drop)

    # 删除行
    print("\n--- 删除行 ---")
    df_drop_row = df.drop(index=[0, 1])
    print(df_drop_row)

    # 修改值
    print("\n--- 修改值 ---")
    df.loc[0, 'salary'] = 5500
    df.loc[df['age'] > 30, 'city'] = '未知'
    print(df)


# ============================================================
# 6. 数据读取和写入（模拟）
# ============================================================

def demo_io_operations():
    """演示数据读取和写入"""
    print("\n" + "=" * 50)
    print("6. 数据读取和写入（模拟）")
    print("=" * 50)

    # 创建示例数据
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'city': ['北京', '上海', '广州']
    })

    # 模拟写入 CSV
    print("\n--- 写入 CSV ---")
    print("df.to_csv('data.csv', index=False)")
    print(f"数据:\n{df}")

    # 模拟读取
    print("\n--- 读取 CSV ---")
    print("df = pd.read_csv('data.csv')")

    # 实际创建临时文件演示
    import tempfile
    import os
    temp_file = tempfile.mktemp(suffix='.csv')
    df.to_csv(temp_file, index=False)
    df_read = pd.read_csv(temp_file)
    print(f"读取结果:\n{df_read}")
    os.remove(temp_file)


# ============================================================
# 7. 缺失值处理
# ============================================================

def demo_missing_values():
    """演示缺失值处理"""
    print("\n" + "=" * 50)
    print("7. 缺失值处理")
    print("=" * 50)

    df = pd.DataFrame({
        'name': ['Alice', 'Bob', None, 'David'],
        'age': [25, None, 35, 40],
        'city': ['北京', '上海', '广州', None]
    })

    print(f"含缺失值的数据:\n{df}")

    print("\n--- 检查缺失值 ---")
    print(f"isnull():\n{df.isnull()}")
    print(f"\n缺失值数量:\n{df.isnull().sum()}")

    print("\n--- 填充缺失值 ---")
    df_filled = df.fillna({'name': 'Unknown', 'age': df['age'].mean(), 'city': '未知'})
    print(df_filled)

    print("\n--- 删除缺失值 ---")
    df_dropna = df.dropna()
    print(df_dropna)


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Day 10: Pandas 基础完整示例")
    print("=" * 60)

    demo_series()
    demo_dataframe()
    demo_data_view()
    demo_data_filter()
    demo_data_operations()
    demo_io_operations()
    demo_missing_values()

    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)