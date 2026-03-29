# Day 11: Pandas 进阶

## 学习目标
- [ ] 掌握分组聚合操作
- [ ] 学会数据透视表
- [ ] 掌握数据合并
- [ ] 学会时间序列处理

---

## 目录

- [1. 分组聚合](#1-分组聚合)
- [2. 数据透视表](#2-数据透视表)
- [3. 数据合并](#3-数据合并)
- [4. 时间序列](#4-时间序列)
- [5. 数据清洗](#5-数据清洗)

---

## 1. 分组聚合

### groupby 基础

```python
import pandas as pd

df = pd.DataFrame({
    'department': ['销售', '技术', '销售', '技术', '市场'],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'salary': [5000, 6000, 5500, 7000, 4500]
})

# 按部门分组
grouped = df.groupby('department')

# 聚合操作
print(grouped['salary'].sum())
print(grouped['salary'].mean())
print(grouped['salary'].agg(['sum', 'mean', 'count']))
```

### 多列分组

```python
# 多列分组
df.groupby(['department', 'city'])['salary'].mean()

# 多列聚合
df.groupby('department').agg({
    'salary': ['sum', 'mean'],
    'age': ['min', 'max']
})
```

---

## 2. 数据透视表

### pivot_table

```python
df = pd.DataFrame({
    'date': ['2024-01', '2024-01', '2024-02', '2024-02'],
    'product': ['A', 'B', 'A', 'B'],
    'region': ['北京', '上海', '北京', '上海'],
    'sales': [100, 200, 150, 250]
})

# 透视表
pivot = df.pivot_table(
    values='sales',
    index='region',
    columns='product',
    aggfunc='sum'
)
```

### crosstab 交叉表

```python
pd.crosstab(df['region'], df['product'])
```

---

## 3. 数据合并

### merge 连接

```python
df1 = pd.DataFrame({'id': [1, 2, 3], 'name': ['A', 'B', 'C']})
df2 = pd.DataFrame({'id': [1, 2, 4], 'score': [90, 80, 70]})

# 内连接
pd.merge(df1, df2, on='id', how='inner')

# 左连接
pd.merge(df1, df2, on='id', how='left')

# 外连接
pd.merge(df1, df2, on='id', how='outer')
```

### concat 拼接

```python
# 纵向拼接
pd.concat([df1, df2])

# 横向拼接
pd.concat([df1, df2], axis=1)
```

---

## 4. 时间序列

### 时间处理

```python
# 创建时间序列
dates = pd.date_range('2024-01-01', periods=10, freq='D')

# 转换为时间类型
df['date'] = pd.to_datetime(df['date'])

# 设置时间索引
df = df.set_index('date')

# 时间重采样
df.resample('M').mean()
```

### 时间窗口

```python
# 滚动窗口
df['rolling_mean'] = df['value'].rolling(window=3).mean()

# 移动窗口
df['shift'] = df['value'].shift(1)
```

---

## 5. 数据清洗

### 重复值处理

```python
# 检查重复
df.duplicated()

# 删除重复
df.drop_duplicates()
```

### 异常值处理

```python
# 基于分位数
q1 = df['value'].quantile(0.25)
q3 = df['value'].quantile(0.75)
iqr = q3 - q1
df = df[(df['value'] >= q1 - 1.5*iqr) & (df['value'] <= q3 + 1.5*iqr)]
```

---

## 练习题

1. 对数据按多列分组并计算统计量
2. 创建数据透视表分析销售数据
3. 合并多个 DataFrame
4. 处理时间序列数据

## 学习资源
- Pandas 官方文档：https://pandas.pydata.org/docs/

## 今日产出
- [ ] pandas_advanced.py（待完成）
- [ ] 学习笔记