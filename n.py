import numpy as np

# 乱数の初期化
np.random.seed(0)

# 縦の大きさ、横の大きさを渡されたときに乱数で指定の大きさの画像を生成する関数
def make_image(m, n):
    
    # n×m行列の各成分を0~5の値でランダムに満たしてください
    image = np.random.randint(0, 6, (m, n))
    return image


# 渡された行列の一部を変更する関数
def change_matrix(matrix):
    # 与えられた行列の形を取得し、shapeに代入してください
    shape = matrix.shape
    
    # 行列の各成分について、変更するかしないかをランダムに決めた上で
    # 変更する場合は0~5のいずれかの整数にランダムに入れ替えてください
    
    # 変更後の値の元となる行列
    source_matrix = np.random.randint(0, 6, shape)
    
    # Trueの場合変更を加える行列
    random =  np.random.randint(0, 2, shape) == 1

    matrix[random] = source_matrix[random]
    
    return matrix

# ランダムに画像を作成
image1 = make_image(3, 3)
print('image1')
print(image1)

# ランダムに変更を適用する
image2 = change_matrix(np.copy(image1))
print()
print('image2')
print(image2)

# image1とimage2の差分を計算し、image3に代入してください
image3 = image1 - image2
print()
print('image3')
print(image3)

# image3の各成分が絶対値である行列をもとめimage3に再代入してください
image3 = np.abs(image3)

# image3を出力
print()
print('modified image3')
print(image3)