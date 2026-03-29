# Day 13: 综合项目 - 股票数据分析

## 项目目标
- [ ] 综合运用 NumPy 和 Pandas
- [ ] 实现数据读取和清洗
- [ ] 进行数据分析和可视化
- [ ] 生成分析报告

---

## 项目概述

本项目将分析股票数据，包括：
1. 数据读取和预处理
2. 基本统计分析
3. 技术指标计算
4. 数据可视化

---

## 技术要点

### 1. 数据读取

```python
import pandas as pd

# 读取 CSV 文件
df = pd.read_csv('stock_data.csv')

# 解析日期
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')
```

### 2. 数据分析

```python
# 基本统计
df.describe()

# 计算收益率
df['return'] = df['close'].pct_change()

# 计算移动平均
df['ma5'] = df['close'].rolling(window=5).mean()
df['ma20'] = df['close'].rolling(window=20).mean()
```

### 3. 数据可视化

```python
import matplotlib.pyplot as plt

# 绘制收盘价
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['close'])
plt.title('Stock Price')
plt.show()
```

---

## 分析内容

1. **价格分析**：开盘价、收盘价、最高价、最低价
2. **成交量分析**：成交量趋势
3. **技术指标**：移动平均、RSI、MACD
4. **收益分析**：日收益率、累计收益

---

## 今日产出
- [ ] stock_analysis.py（待完成）
- [ ] 分析报告