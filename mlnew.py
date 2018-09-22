import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# (1.)
# Irisデータセットをロード
iris = datasets.load_iris()
# 3,4列目の特徴量を抽出
X = iris.data[:, [2,3]]
# クラスラベルを取得
y = iris.target

'''
(1.) の説明
Iris オブジェクトの data要素を取得し、
（dataは　[[float1, float2, float3, float4]]  という2次元リストなっている）
そのうち、float3, float4 を切り出してXに代入している
また、各リストの正解ラベルも取得しyに代入している
'''


# (2.)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=0)
print('X_train, X_test, y_train, y_test')
print(X_train, X_test, y_train, y_test)
'''
(2.) の説明
ホールドアウト法を用いて、
データのうち30%をテストデータ、70%をトレーニングデータとして分けた。
random_state=0 として、再現性も保証した。
'''


# (3.)
svc = svm.SVC(C=1, kernel='rbf', gamma=0.001)
svc.fit(X_train, y_train)
'''
(3.) の説明
機械学習アルゴリズムSVMを用いて、
学習をおこなっている
'''


# (4.)
y_pred = svc.predict(X_test)
print ("Accuracy: %.2f"% accuracy_score(y_test, y_pred))

'''
(4.) の説明
学習済みモデルを用いて、ラベルの予測を取得し、
正解率を表示している。
'''
