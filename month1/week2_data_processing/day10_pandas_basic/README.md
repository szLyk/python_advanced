# Day 10: Pandas 基础

## 学习目标
- [ ] 理解 Series 和 DataFrame
- [ ] 掌握数据创建和读取
- [ ] 学会数据查看和筛选
- [ ] 掌握基本数据操作

---

## 目录

- [1. Pandas 简介](#1-pandas-简介)
- [2. Series](#2-series)
- [3. DataFrame](#3-dataframe)
- [4. 数据读取和写入](#4-数据读取和写入)
- [5. 数据查看](#5-数据查看)
- [6. 数据筛选](#6-数据筛选)
- [7. 数据操作](#7-数据操作)

---

## 1. Pandas 简介

Pandas 是 Python 数据分析的核心库，提供：
- **Series**：一维数据结构
- **DataFrame**：二维表格数据结构
- **数据读写**：支持 CSV、Excel、SQL 等
- **数据处理**：清洗、转换、分析

---

## 2. Series

### 创建 Series

```python
import pandas as pd

# 从列表创建
s = pd.Series([1, 2, 3, 4, 5])

# 指定索引
s = pd.Series([1, 2, 3], index=['a', 'b', 'c'])

# 从字典创建
s = pd.Series({'a': 1, 'b': 2, 'c': 3})
```

### Series 属性

```python
s = pd.Series([1, 2, 3, 4, 5])

print(s.values)   # 值数组
print(s.index)    # 索引
print(s.dtype)    # 数据类型
print(s.shape)    # 形状
```

---

## 3. DataFrame

### 创建 DataFrame

```python
import pandas as pd

# 从字典创建
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['北京', '上海', '广州']
})

# 从列表创建
df = pd.DataFrame([
    ['Alice', 25, '北京'],
    ['Bob', 30, '上海'],
], columns=['name', 'age', 'city'])
```

### DataFrame 属性

```python
print(df.shape)      # (行数, 列数)
print(df.columns)    # 列名
print(df.index)      # 行索引
print(df.dtypes)     # 各列数据类型
print(df.values)     # 值数组
```

---

## 4. 数据读取和写入

### 读取数据

```python
# CSV 文件
df = pd.read_csv('data.csv')

# Excel 文件
df = pd.read_excel('data.xlsx')

# 指定分隔符
df = pd.read_csv('data.txt', sep='\t')

# 指定编码
df = pd.read_csv('data.csv', encoding='utf-8')
```

### 写入数据

```python
# 写入 CSV
df.to_csv('output.csv', index=False)

# 写入 Excel
df.to_excel('output.xlsx', index=False)
```

---

## 5. 数据查看

### 查看基本信息

```python
# 前 5 行
print(df.head())
print(df.head(10))

# 后 5 行
print(df.tail())

# 基本信息
print(df.info())

# 统计摘要
print(df.describe())

# 列名
print(df.columns)
```

### 查看数据

```python
# 查看某一列
print(df['name'])

# 查看多列
print(df[['name', 'age']])

# 查看某行
print(df.loc[0])      # 按索引
print(df.iloc[0])     # 按位置
```

---

## 6. 数据筛选

### 条件筛选

```python
# 单条件
df[df['age'] > 25]

# 多条件
df[(df['age'] > 25) & (df['city'] == '北京')]

# isin 筛选
df[df['city'].isin(['北京', '上海'])]
```

### 字符串筛选

```python
# 包含字符串
df[df['name'].str.contains('li')]

# 开头/结尾
df[df['name'].str.startswith('A')]
```

---

## 7. 数据操作

### 添加列

```python
# 直接赋值
df['salary'] = [5000, 6000, 7000]

# 计算列
df['age_plus_10'] = df['age'] + 10
```

### 删除列/行

```python
# 删除列
df.drop('salary', axis=1)
df.drop(columns=['salary'])

# 删除行
df.drop(0, axis=0)
df.drop(index=[0, 1])
```

### 修改值

```python
# 修改列值
df['age'] = df['age'] + 1

# 条件修改
df.loc[df['age'] > 30, 'city'] = '深圳'
```

---

## 练习题

1. 创建一个包含学生信息的 DataFrame
2. 读取 CSV 文件并查看前 10 行
3. 筛选年龄大于 20 的记录
4. 添加一个新列并计算值

## 学习资源
- Pandas 官方文档：https://pandas.pydata.org/docs/
- B 站：pandas 从入门到实战

## 今日产出
- [ ] pandas_basic.py（待完成）
- [ ] 学习笔记