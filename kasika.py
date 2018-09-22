import matplotlib.pyplot as plt
import numpy as np
import math
import time 

np.random.seed(100)
X = 0 # 的に当たった回数

# 試行回数Nを指定
N = 1000
# 四分円の境界の方程式[y=√1-x^2 (0<=x<=1)]を描画
circle_x = np.arange(0, 1, 0.001)
circle_y = np.sqrt(1- circle_x * circle_x)
plt.figure(figsize=(5,5))
plt.plot(circle_x, circle_y) 

# N回の試行にかかる時間を計測
start_time = time.clock() 

# N回の試行
for i in range(0, N):
    # 0から1の間で一様乱数を発生させ、変数score_xに格納
    score_x = np.random.rand()
    # 0から1の間で一様乱数を発生させ、変数score_yに格納
    score_y = np.random.rand()
    # 点が円の中に入った場合と入らなかった場合について条件分岐
    # 円内に入ったものは赤で表示させ、外れたものは青で表示
    # 円内に入ったならば、上で定義した変数Xに1ポイント加算
    if(np.sqrt(score_x ** 2 + score_y ** 2) <= 1):
        plt.scatter(score_x, score_y, color = "r")
        X += 1
    else:
        plt.scatter(score_x, score_y, color = "b")




# piの近似値をここで計算
pi = 4 * X / N
# モンテカルロ法の実行時間を計算
end_time = time.clock() 
time = end_time - start_time

# 円周率の結果を表示
print("近似した円周率は{0}です".format(pi))
print("実行時間:%f" % (time))

# 結果を表示 
plt.grid(True)
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
