# モジュールのインポート
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.metrics import f1_score

data = load_digits()
train_X, test_X, train_y, test_y = train_test_split(
    data.data, data.target, random_state=42)


# パラメーターの値の候補を設定
model_param_set_grid = {
    #ロジスティック回帰
    LogisticRegression(): {
        "C": [10 ** i for i in range(-5, 5)],
        "random_state": [42]
    },
    #線形SVM
    LinearSVC(): {
        "C": [10 ** i for i in range(-5, 5)],
        "multi_class": ["ovr", "crammer_singer"],
        "random_state": [42]
    },
    #非線形SVM
    SVC(): {
        "kernel": ["linear", "poly", "rbf", "sigmoid"],
        "C": [10 ** i for i in range(-5, 5)],
        "decision_function_shape": ["ovr", "ovo"],
        "random_state": [42]
    },
    #決定木
    DecisionTreeClassifier(): {
        "max_depth": [i for i in range(1, 20)],
    },
    #ランダムフォレスト
    RandomForestClassifier(): {
        "n_estimators": [i for i in range(10, 20)],
        "max_depth": [i for i in range(1, 10)],
    },
    #k-NN
    KNeighborsClassifier(): {
        "n_neighbors": [i for i in range(1, 10)]
    }
}

# 学習器を構築
model1 = LogisticRegression()
model2 = LinearSVC()
model3 = SVC()
model4 = DecisionTreeClassifier()
model5 = RandomForestClassifier()
model6 = KNeighborsClassifier()

#各モジュールの実行
model1.fit(train_X, train_y)
model2.fit(train_X, train_y)
model3.fit(train_X, train_y)
model4.fit(train_X, train_y)
model5.fit(train_X, train_y)
model6.fit(train_X, train_y)

score1 = model1.score(test_X, test_y)
score2 = model2.score(test_X, test_y)
score3 = model3.score(test_X, test_y)
score4 = model4.score(test_X, test_y)
score5 = model5.score(test_X, test_y)
score6 = model6.score(test_X, test_y)

#学習前の結果を出力
print(score1, score2, score3, score4, score5, score6)

max_score = 0
best_model = None
best_param = None

for model, param in model_param_set_grid.items():
    clf = GridSearchCV(model, param)
    clf.fit(train_X, train_y)
    pred_y = clf.predict(test_X)
    score = f1_score(test_y, pred_y, average="micro")
    
    # 最高評価更新時にモデルやパラメーターも更新
    if max_score < score:
        max_score = score
        best_param = clf.best_params_
        best_model = model.__class__.__name__

    print(score)

# 最も成績のいいスコアを出力
print("学習モデル:{},\nパラメーター:{}".format(best_model, best_param))
