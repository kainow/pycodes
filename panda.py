import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


url = "http://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
# データのDataFrameへの読み込み
online_retail_xlsx = pd.ExcelFile(url)
online_retail_raw = online_retail_xlsx.parse('Online Retail')

# キャンセル記録および欠損があるデータを削除
online_retail_raw['cancel_flg'] = online_retail_raw.InvoiceNo.map(lambda x:str(x)[0])
online_retail_df = online_retail_raw[(online_retail_raw.cancel_flg == '5') &
                                    online_retail_raw.CustomerID.notnull()]

# Quantity(量)とUnitPrice(単価)から合計金額を計算し、
# カラムが"TotalPrice"の新しい列を作成
online_retail_df["TotalPrice"] = online_retail_df["Quantity"] * online_retail_df["UnitPrice"]

# 顧客ごとに注文をグループ化し、online_retail_groupedに代入
online_retail_grouped = online_retail_df.groupby("CustomerID")

# 顧客ごとの合計金額を計算し、合計金額のみtotal_per_cutomerに代入
# 一列のみ取り出したため、Series型となります
total_per_customer = online_retail_grouped.sum()["TotalPrice"]

# 合計金額が低い順にソートし、customer_sortedに代入
customer_sorted = total_per_customer.sort_values()

# 累積和を計算。customer_cumsumはリストになります。
# この処理はcustomer_cumsum = customer_sorted.cumsum()で一発で計算できます
customer_cumsum = [0]
for i in range(len(customer_sorted)):
    customer_cumsum.append(customer_cumsum[i] + customer_sorted.iloc[i])

# 最初に要素を一個入れた状態だったので1番目以降を残します
customer_cumsum = customer_cumsum[1:]

# xに顧客の人数を代入してください
x = len(sums.index)

# yに顧客ごとの売り上げの累積和をリスト型で代入してください
y = sums['TotalPrice'].values.tolist()


# xに顧客の人数を代入してください
x = len(customer_cumsum)

# yに顧客ごとの売り上げの累積和をリスト型で代入してください
y = customer_cumsum

# 以下、可視化の作業です

# 累積和の最後の項が1になるようにします
x = np.arange(x) / x
y = np.array(y) / y[len(y)-1]

# グラフの要素に名前をつけます
plt.title("Distribution of earings")
plt.xlabel("Cumulative sum of customers")
plt.ylabel("Cumulative sum of earings")
plt.axvline(x=0.8, linestyle='--')
plt.axhline(y=0.2, linestyle='--')
plt.plot(x, y)
plt.show()