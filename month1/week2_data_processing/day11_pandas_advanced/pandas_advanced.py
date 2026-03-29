"""
Day 11: Pandas 进阶

学习目标：
1. 掌握分组聚合操作
2. 学会数据透视表
3. 掌握数据合并
4. 学会时间序列处理

作者：AI Agent 工程师学习者
日期：2026-03-30
"""

import pandas as pd
import numpy as np


# ============================================================
# 1. 分组聚合
# ============================================================

def demo_groupby():
    """演示分组聚合"""
    print("=" * 50)
    print("1. 分组聚合")
    print("=" * 50)

    # 创建示例数据
    df = pd.DataFrame({
        'department': ['销售', '技术', '销售', '技术', '市场', '市场'],
        'city': ['北京', '上海', '上海', '北京', '北京', '上海'],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],
        'salary': [5000, 6000, 5500, 7000, 4500, 4800],
        'age': [25, 30, 28, 35, 22, 26]
    })
    print(f"原数据:\n{df}")

    # 单列分组
    print("\n--- 单列分组 ---")
    print(f"按部门分组，薪资总和:\n{df.groupby('department')['salary'].sum()}")

    # 多列聚合
    print("\n--- 多列聚合 ---")
    print(df.groupby('department')['salary'].agg(['sum', 'mean', 'count']))

    # 多列分组
    print("\n--- 多列分组 ---")
    print(df.groupby(['department', 'city'])['salary'].mean())

    # 多列多聚合
    print("\n--- 多列多聚合 ---")
    print(df.groupby('department').agg({
        'salary': ['sum', 'mean'],
        'age': ['min', 'max']
    }))


# ============================================================
# 2. 数据透视表
# ============================================================

def demo_pivot_table():
    """演示数据透视表"""
    print("\n" + "=" * 50)
    print("2. 数据透视表")
    print("=" * 50)

    # 创建示例数据
    df = pd.DataFrame({
        'date': ['2024-01', '2024-01', '2024-01', '2024-02', '2024-02', '2024-02'],
        'product': ['A', 'B', 'A', 'A', 'B', 'B'],
        'region': ['北京', '上海', '上海', '北京', '北京', '上海'],
        'sales': [100, 200, 150, 120, 180, 250],
        'quantity': [10, 20, 15, 12, 18, 25]
    })
    print(f"原数据:\n{df}")

    # 简单透视表
    print("\n--- 简单透视表 ---")
    pivot = df.pivot_table(
        values='sales',
        index='region',
        columns='product',
        aggfunc='sum'
    )
    print(pivot)

    # 多值透视表
    print("\n--- 多值透视表 ---")
    pivot = df.pivot_table(
        values=['sales', 'quantity'],
        index='region',
        columns='product',
        aggfunc='sum'
    )
    print(pivot)

    # 交叉表
    print("\n--- 交叉表 crosstab ---")
    print(pd.crosstab(df['region'], df['product']))


# ============================================================
# 3. 数据合并
# ============================================================

def demo_merge():
    """演示数据合并"""
    print("\n" + "=" * 50)
    print("3. 数据合并")
    print("=" * 50)

    # 创建示例数据
    df1 = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie']
    })
    df2 = pd.DataFrame({
        'id': [1, 2, 4],
        'score': [90, 85, 70],
        'grade': ['A', 'B', 'C']
    })

    print(f"df1:\n{df1}")
    print(f"\ndf2:\n{df2}")

    # 内连接
    print("\n--- 内连接 inner ---")
    print(pd.merge(df1, df2, on='id', how='inner'))

    # 左连接
    print("\n--- 左连接 left ---")
    print(pd.merge(df1, df2, on='id', how='left'))

    # 右连接
    print("\n--- 右连接 right ---")
    print(pd.merge(df1, df2, on='id', how='right'))

    # 外连接
    print("\n--- 外连接 outer ---")
    print(pd.merge(df1, df2, on='id', how='outer'))


def demo_concat():
    """演示数据拼接"""
    print("\n" + "=" * 50)
    print("4. 数据拼接 concat")
    print("=" * 50)

    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})

    print(f"df1:\n{df1}")
    print(f"\ndf2:\n{df2}")

    # 纵向拼接
    print("\n--- 纵向拼接 ---")
    print(pd.concat([df1, df2], ignore_index=True))

    # 横向拼接
    print("\n--- 横向拼接 ---")
    df3 = pd.DataFrame({'C': [9, 10], 'D': [11, 12]})
    print(pd.concat([df1, df3], axis=1))


# ============================================================
# 4. 时间序列
# ============================================================

def demo_time_series():
    """演示时间序列"""
    print("\n" + "=" * 50)
    print("5. 时间序列")
    print("=" * 50)

    # 创建时间序列
    print("\n--- 创建时间序列 ---")
    dates = pd.date_range('2024-01-01', periods=10, freq='D')
    print(f"日期范围: {dates[:5]}...")

    # 创建时间序列数据
    df = pd.DataFrame({
        'date': dates,
        'value': np.random.randn(10).cumsum()
    })
    df = df.set_index('date')
    print(f"\n时间序列数据:\n{df}")

    # 时间索引
    print("\n--- 时间索引 ---")
    print(f"df.loc['2024-01-05']:\n{df.loc['2024-01-05']}")

    # 滚动窗口
    print("\n--- 滚动窗口 ---")
    df['rolling_mean'] = df['value'].rolling(window=3).mean()
    print(df)

    # 时间位移
    print("\n--- 时间位移 ---")
    df['shift_1'] = df['value'].shift(1)
    df['diff'] = df['value'].diff()
    print(df[['value', 'shift_1', 'diff']])


# ============================================================
# 5. 数据清洗
# ============================================================

def demo_data_cleaning():
    """演示数据清洗"""
    print("\n" + "=" * 50)
    print("6. 数据清洗")
    print("=" * 50)

    # 创建含问题的数据
    df = pd.DataFrame({
        'id': [1, 2, 3, 3, 4],
        'name': ['Alice', 'Bob', None, 'Charlie', 'David'],
        'value': [100, 200, 150, 150, 999]  # 999 是异常值
    })
    print(f"原数据:\n{df}")

    # 检查重复
    print("\n--- 检查重复 ---")
    print(f"重复行: {df.duplicated().sum()}")
    print(df[df.duplicated()])

    # 删除重复
    print("\n--- 删除重复 ---")
    df_clean = df.drop_duplicates()
    print(df_clean)

    # 填充缺失值
    print("\n--- 填充缺失值 ---")
    df['name'] = df['name'].fillna('Unknown')
    print(df)

    # 异常值处理
    print("\n--- 异常值处理 ---")
    print(f"原始 value: {df['value'].tolist()}")
    q1 = df['value'].quantile(0.25)
    q3 = df['value'].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    print(f"IQR 方法: 下界={lower:.2f}, 上界={upper:.2f}")
    df_clean = df[(df['value'] >= lower) & (df['value'] <= upper)]
    print(f"处理后:\n{df_clean}")


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Day 11: Pandas 进阶完整示例")
    print("=" * 60)

    demo_groupby()
    demo_pivot_table()
    demo_merge()
    demo_concat()
    demo_time_series()
    demo_data_cleaning()

    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)