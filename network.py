import numpy as np
import networkx as nx
from IPython.display import display
import matplotlib.pyplot as plt
import json
import community
import copy
%matplotlib inline

plt.figure(figsize=(20, 20))

# Lから要素をchooseNum個選んで返す関数
# Lに同じ要素があっても別物として考えている
# 例えばL = [0, 1, 2, 3]に対して[0, 1, 2]と[1, 0, 2]は同じ選び方と考える


def choose(L: [int], chooseNum: int, now=None) -> [int]:

    # nowが最終的に返すリスト
    # 空リストで初期化

    if now == None:
        now = []

    # "Lから0個選ぶ"という操作に対してはnowをそのまま返す

    if chooseNum == 0:
        yield now

    # chooseNumが1以上の場合

    else:

        # Lの先頭からlen(L) - (chooseNum - 1) - 1番目までの要素の内どれか1つ選ぶ
        # Lから選ぶ範囲を制限することにより[0, 1, 2]と[1, 0, 2]のような重複を除く
        # chooseNumから1ひいて再帰のような操作を行う

        for i in range(0, len(L) - (chooseNum - 1)):
            yield from choose(L[i + 1:], chooseNum - 1, now + [L[i]])


# データをファイルから受け取る

f = open('./data/my_sample_data.json')
data = json.load(f)
f.close()

# strをintに変換

data = {int(key): {int(sub_key): data[key][sub_key]
                   for sub_key in data[key].keys()} for key in data.keys()}

# グラフの定義

G = nx.Graph()
for key in data.keys():
    for sub_key in data[key].keys():
        if(key < sub_key):
            G.add_edge(key, sub_key, weight=(1 / data[key][sub_key]))

# クラスタリング

partition = community.best_partition(G)

# 現在のコミュニティの数
# これが2になるようにしたい

community_num = len(set(list(partition.values())))

# community_numが2になるまで統合を繰り返す

while community_num > 2:

    # new_partitionに統合した結果を保存する
    # mod_numはモジュラリティ指標の比較用

    new_partition = {}
    mod_num = 0

    # mergeが統合する2つのコミュニティの番号
    # これを全探索する

    for merge in choose(list(set(list(partition.values()))), 2):
        next_partition = {}

        # merge[1]のコミュニティに属する頂点をmerge[0]に統合

        for key in partition.keys():
            if partition[key] == merge[1]:
                next_partition.update({key: merge[0]})
            else:
                next_partition.update({key: partition[key]})

        # モジュラリティ指標を比べる

        temp = community.modularity(next_partition, G)
        if temp > mod_num:
            mod_num = temp
            new_partition = next_partition

    # 新しい分割

    partition = new_partition
    community_num -= 1

nx.draw_networkx(G, node_color=[partition[i]
                                for i in G.nodes()], cmap=plt.cm.RdYlBu)
