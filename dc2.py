import os

import numpy as np
import matplotlib.pyplot as plt
import cv2


def scratch_image(img, flip=True, thr=True, filt=True, resize=True, erode=True):
    # ----------------------------ここから書いて下さい----------------------------
    # 水増しの手法を配列にまとめる
    methods = [flip, thr, filt, resize, erode]
    # 画像のサイズを習得、ぼかしに使うフィルターの作成
    img_size = img.shape
    filter1 = np.ones((3, 3))
    # オリジナルの画像データを配列に格納
    images = [img]
    # 手法に用いる関数
    scratch = np.array([
        lambda x: cv2.flip(x, 1),
        lambda x: cv2.threshold(x, 100, 255, cv2.THRESH_TOZERO)[1],
        lambda x: cv2.GaussianBlur(x, (5, 5), 0),
        lambda x: cv2.resize(cv2.resize(
                        x, (img_size[1] // 5, img_size[0] // 5)
                    ),(img_size[1], img_size[0])),
        lambda x: cv2.erode(x, filter1)
    ])
    # 関数と画像を引数に、加工した画像を元と合わせて水増しする関数
    doubling_images = lambda f, imag: np.r_[imag, [f(i) for i in imag]]
    # methodsがTrueの関数で水増し
    for func in scratch[methods]:
        images = doubling_images(func, images)
    print(images.shape)
    return images
    # ----------------------------ここまで書いて下さい----------------------------

    
# 画像の読み込み
cat_img = cv2.imread("5.クレンジング用データ/cat_sample.jpg")

# 画像の水増し
scratch_cat_images = scratch_image(cat_img)

# 画像を保存するフォルダーを作成
if not os.path.exists("scratch_images"):
    os.mkdir("scratch_images")
for num, im in enumerate(scratch_cat_images):
    # まず保存先のディレクトリ"scratch_images/"を指定、番号を付けて保存
    cv2.imwrite("scratch_images/" + str(num) + ".jpg" ,im) 