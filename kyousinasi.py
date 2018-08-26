添削問題、お疲れ様です。
ｋ平均法で画像の氏帰趨を減らして、N色の画像にするというのは
１ランダムにN個の代表職を選択
↓
２画像ピクセルそれぞれにつき一番近い代表職を選び、全ピクセルをＮ色個にわける
↓
３それぞれの色のRGBの平均色を新たな代表職とする
↓
４新たな代表職を用いて再度２の処理を行う
↓
5この処理を繰り返し代表職が変化しなくなったものを最終的な代表職とする
と言った処理をすることで、また距離を活用するというのは２つの色がどれだけ離れているかということを、
(R1,G1,B1)と(R2,G2,B2)の距離と捉え、それを３次元ベクトル空間上の距離と同様に
(R1-R2)^2 +(G1-G2)^2 + (B1-B2)^2
で計算するということです。


解答例では、以下の手順でk-means法を実装しました。
①初期値のRGBをnp.randintで代入
②初期値と代表色のユーグリッド距離を求める
d = sum([x*x for x in point-center[i]])としています。
d=np.linalg.norm(center[i]-point)とも表せます。

これはk-means法でpointがどのセントロイドに属するか決めるために
各セントロイドとの距離を測っています。
③最も距離が近いセントロイドにクラス分けされる
④新しく分類されたセントロイドで新しい代表色を決める

②-④を繰り替えし、変化率が一定以下になった場合終了する。

解答例ではnumpyのみを用いてk-meansを実装しました。参考にして、復習しておきましょう。


import numpy as np
from sklearn.cluster import KMeans
import cv2
import matplotlib.pyplot as plt
def reduce_colors():
    N = np.random.randint(1,32)
    print(N)

    img = cv2.imread("./img_cluster/img_1_0.png")
    b,g,r = cv2.split(img)
    img = cv2.merge([r,g,b])

    plt.imshow(img)
    plt.show()

    X = np.reshape(img, (90000, 3))

    km = KMeans(n_clusters=N, random_state=0)
    Y_km = km.fit_predict(X)

    X2 = X.copy()
    for i in set(Y_km):
        color_group = X[Y_km==i]
        R_avg = np.average([i[0] for i in color_group])
        G_avg = np.average([i[1] for i in color_group])
        B_avg = np.average([i[2] for i in color_group])

        X2[Y_km==i] = [R_avg, G_avg, B_avg]

    X2 = X2.reshape(300,300,3)

    plt.imshow(X2)
    plt.show()

reduce_colors()