import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# データの準備（新しいデータ）
N = [
    1000000,
    2000000,
    3000000,
    4000000,
    5000000,
    6000000,
    7000000,
    8000000,
    9000000,
    10000000,
]

elapsed = [
    120000,
    230000,
    350000,
    480000,
    600000,
    720000,
    850000,
    970000,
    1090000,
    1220000,
]

# 線形近似
coefficients = np.polyfit(N, elapsed, 1)
slope, intercept = coefficients

# グラフの作成
plt.figure(figsize=(10, 6))
plt.scatter(N, elapsed, label='Data Points', color='blue')  # 散布図
plt.plot(N, np.polyval(coefficients, N), color='red', label=f'Fitted Line: y = {slope:.2f}x + {intercept:.2f}')  # 近似直線
plt.title('Fitted Line (add)')
plt.xlabel('N')
plt.ylabel('Elapsed Time (CLOCKS)')
plt.grid(True)
plt.xticks(N)  # X軸の目盛りをNの値に設定

# x軸の目盛りを通常表示に設定
ax = plt.gca()
ax.xaxis.set_major_formatter(ScalarFormatter())
ax.xaxis.get_major_formatter().set_scientific(False)  # x軸の指数表示を無効にする

# y軸の目盛りを通常表示に設定
ax.yaxis.set_major_formatter(ScalarFormatter())
ax.yaxis.get_major_formatter().set_scientific(False)  # y軸の指数表示を無効にする

# 傾きをグラフに表示
plt.text(0.5, 0.9, f'Slope: {slope:.2f}', transform=plt.gca().transAxes, fontsize=12, color='black', ha='center')

plt.legend()
plt.tight_layout()

# グラフを保存
plt.savefig('graph_add.png')

# グラフを表示
plt.show()

# 傾きを表示
print(f'傾き (Slope): {slope:.2f}')
print(f'切片 (Intercept): {intercept:.2f}')
