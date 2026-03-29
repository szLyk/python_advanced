"""
Day 13: 综合项目 - 股票数据分析

项目目标：
1. 综合运用 NumPy 和 Pandas
2. 实现数据读取和清洗
3. 进行数据分析和可视化
4. 生成分析报告

作者：AI Agent 工程师学习者
日期：2026-03-30
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


# ============================================================
# 1. 模拟股票数据生成
# ============================================================

def generate_stock_data(days=100, seed=42):
    """生成模拟股票数据"""
    np.random.seed(seed)

    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')

    # 模拟股价走势（随机游走）
    base_price = 100
    returns = np.random.randn(days) * 0.02  # 日收益率
    prices = base_price * np.exp(np.cumsum(returns))

    # 模拟 OHLCV 数据
    data = {
        'date': dates,
        'open': prices * (1 + np.random.randn(days) * 0.01),
        'high': prices * (1 + np.abs(np.random.randn(days) * 0.02)),
        'low': prices * (1 - np.abs(np.random.randn(days) * 0.02)),
        'close': prices,
        'volume': np.random.randint(1000000, 10000000, days)
    }

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    return df


# ============================================================
# 2. 数据预处理
# ============================================================

def preprocess_data(df):
    """数据预处理"""
    print("=" * 50)
    print("2. 数据预处理")
    print("=" * 50)

    # 设置日期索引
    df = df.set_index('date')

    # 按日期排序
    df = df.sort_index()

    # 检查缺失值
    print(f"\n缺失值检查:\n{df.isnull().sum()}")

    # 添加衍生列
    df['price_change'] = df['close'] - df['open']
    df['pct_change'] = df['close'].pct_change()

    print(f"\n处理后数据预览:\n{df.head()}")
    return df


# ============================================================
# 3. 基本统计分析
# ============================================================

def analyze_basic_stats(df):
    """基本统计分析"""
    print("\n" + "=" * 50)
    print("3. 基本统计分析")
    print("=" * 50)

    # 统计摘要
    print("\n--- 价格统计 ---")
    print(df[['open', 'high', 'low', 'close']].describe())

    # 收益率统计
    print("\n--- 收益率统计 ---")
    returns = df['pct_change'].dropna()
    print(f"平均日收益率: {returns.mean():.4%}")
    print(f"收益率标准差: {returns.std():.4%}")
    print(f"最大单日涨幅: {returns.max():.4%}")
    print(f"最大单日跌幅: {returns.min():.4%}")

    # 波动率（年化）
    volatility = returns.std() * np.sqrt(252)
    print(f"年化波动率: {volatility:.4%}")

    # 成交量统计
    print("\n--- 成交量统计 ---")
    print(f"平均成交量: {df['volume'].mean():,.0f}")
    print(f"最大成交量: {df['volume'].max():,.0f}")
    print(f"最小成交量: {df['volume'].min():,.0f}")

    return returns


# ============================================================
# 4. 技术指标计算
# ============================================================

def calculate_indicators(df):
    """计算技术指标"""
    print("\n" + "=" * 50)
    print("4. 技术指标计算")
    print("=" * 50)

    # 移动平均线
    df['ma5'] = df['close'].rolling(window=5).mean()
    df['ma10'] = df['close'].rolling(window=10).mean()
    df['ma20'] = df['close'].rolling(window=20).mean()

    print("\n--- 移动平均线 ---")
    print(df[['close', 'ma5', 'ma10', 'ma20']].tail())

    # RSI (相对强弱指标)
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))

    print("\n--- RSI ---")
    print(f"最新 RSI: {df['rsi'].iloc[-1]:.2f}")

    # MACD
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema12 - ema26
    df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['histogram'] = df['macd'] - df['signal']

    print("\n--- MACD ---")
    print(df[['macd', 'signal', 'histogram']].tail())

    # 布林带
    df['boll_middle'] = df['close'].rolling(window=20).mean()
    df['boll_std'] = df['close'].rolling(window=20).std()
    df['boll_upper'] = df['boll_middle'] + 2 * df['boll_std']
    df['boll_lower'] = df['boll_middle'] - 2 * df['boll_std']

    print("\n--- 布林带 ---")
    print(df[['close', 'boll_upper', 'boll_middle', 'boll_lower']].tail())

    return df


# ============================================================
# 5. 交易信号分析
# ============================================================

def analyze_signals(df):
    """分析交易信号"""
    print("\n" + "=" * 50)
    print("5. 交易信号分析")
    print("=" * 50)

    # 均线交叉信号
    df['ma_signal'] = 0
    df.loc[df['ma5'] > df['ma20'], 'ma_signal'] = 1  # 买入信号
    df.loc[df['ma5'] < df['ma20'], 'ma_signal'] = -1  # 卖出信号

    # 计算信号变化点
    df['ma_position'] = df['ma_signal'].diff()
    buy_signals = df[df['ma_position'] == 2]  # 从-1变为1
    sell_signals = df[df['ma_position'] == -2]  # 从1变为-1

    print(f"\n均线策略:")
    print(f"买入信号次数: {len(buy_signals)}")
    print(f"卖出信号次数: {len(sell_signals)}")

    # RSI 信号
    df['rsi_signal'] = 0
    df.loc[df['rsi'] < 30, 'rsi_signal'] = 1   # 超卖
    df.loc[df['rsi'] > 70, 'rsi_signal'] = -1  # 超买

    print(f"\nRSI 信号:")
    print(f"超卖信号: {(df['rsi'] < 30).sum()}")
    print(f"超买信号: {(df['rsi'] > 70).sum()}")

    return df


# ============================================================
# 6. 数据可视化
# ============================================================

def plot_analysis(df):
    """绘制分析图表"""
    print("\n" + "=" * 50)
    print("6. 数据可视化")
    print("=" * 50)

    # 设置中文字体（如果支持）
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
    except:
        pass

    fig, axes = plt.subplots(4, 1, figsize=(14, 16))

    # 1. 价格和移动平均
    ax1 = axes[0]
    ax1.plot(df.index, df['close'], label='Close Price', linewidth=1.5)
    ax1.plot(df.index, df['ma5'], label='MA5', linestyle='--', alpha=0.8)
    ax1.plot(df.index, df['ma20'], label='MA20', linestyle='--', alpha=0.8)
    ax1.fill_between(df.index, df['boll_lower'], df['boll_upper'], alpha=0.1, label='Bollinger Band')
    ax1.set_title('Stock Price with Moving Averages')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 成交量
    ax2 = axes[1]
    colors = ['green' if df['close'].iloc[i] >= df['open'].iloc[i] else 'red' for i in range(len(df))]
    ax2.bar(df.index, df['volume'], color=colors, alpha=0.6)
    ax2.set_title('Trading Volume')
    ax2.grid(True, alpha=0.3)

    # 3. RSI
    ax3 = axes[2]
    ax3.plot(df.index, df['rsi'], label='RSI', color='purple')
    ax3.axhline(y=70, color='red', linestyle='--', alpha=0.5)
    ax3.axhline(y=30, color='green', linestyle='--', alpha=0.5)
    ax3.fill_between(df.index, 30, 70, alpha=0.1)
    ax3.set_title('RSI (Relative Strength Index)')
    ax3.set_ylim(0, 100)
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. MACD
    ax4 = axes[3]
    ax4.plot(df.index, df['macd'], label='MACD', color='blue')
    ax4.plot(df.index, df['signal'], label='Signal', color='orange')
    colors = ['green' if x >= 0 else 'red' for x in df['histogram']]
    ax4.bar(df.index, df['histogram'], color=colors, alpha=0.5, label='Histogram')
    ax4.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax4.set_title('MACD')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()

    # 保存图片
    output_file = 'stock_analysis.png'
    plt.savefig(output_file, dpi=100, bbox_inches='tight')
    print(f"\n图表已保存: {output_file}")

    plt.close()


# ============================================================
# 7. 生成分析报告
# ============================================================

def generate_report(df):
    """生成分析报告"""
    print("\n" + "=" * 50)
    print("7. 分析报告")
    print("=" * 50)

    latest = df.iloc[-1]
    first = df.iloc[0]

    report = f"""
=====================================
股票数据分析报告
=====================================

数据周期: {df.index[0].strftime('%Y-%m-%d')} 至 {df.index[-1].strftime('%Y-%m-%d')}
交易天数: {len(df)}

一、价格概况
-------------------------------------
起始价格: {first['close']:.2f}
最新价格: {latest['close']:.2f}
期间涨幅: {(latest['close'] / first['close'] - 1) * 100:.2f}%
期间最高: {df['high'].max():.2f}
期间最低: {df['low'].min():.2f}

二、收益分析
-------------------------------------
平均日收益率: {df['pct_change'].mean() * 100:.4f}%
年化波动率: {df['pct_change'].std() * np.sqrt(252) * 100:.2f}%

三、技术指标
-------------------------------------
MA5: {latest['ma5']:.2f}
MA20: {latest['ma20']:.2f}
RSI: {latest['rsi']:.2f}
MACD: {latest['macd']:.4f}
Signal: {latest['signal']:.4f}

四、信号提示
-------------------------------------
均线信号: {'买入' if latest['ma_signal'] == 1 else '卖出'}
RSI状态: {'超买' if latest['rsi'] > 70 else '超卖' if latest['rsi'] < 30 else '正常'}
MACD状态: {'金叉' if latest['histogram'] > 0 else '死叉'}

=====================================
"""
    print(report)

    # 保存报告
    with open('stock_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    print("报告已保存: stock_report.txt")


# ============================================================
# 主程序
# ============================================================

def main():
    """主函数"""
    print("=" * 60)
    print("Day 13: 股票数据分析项目")
    print("=" * 60)

    # 1. 生成模拟数据
    print("\n1. 生成模拟股票数据...")
    df = generate_stock_data(days=100)
    print(f"生成 {len(df)} 天的数据")

    # 2. 数据预处理
    df = preprocess_data(df)

    # 3. 基本统计分析
    analyze_basic_stats(df)

    # 4. 计算技术指标
    df = calculate_indicators(df)

    # 5. 交易信号分析
    df = analyze_signals(df)

    # 6. 数据可视化
    plot_analysis(df)

    # 7. 生成报告
    generate_report(df)

    print("\n" + "=" * 60)
    print("分析完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()