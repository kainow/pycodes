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

online_retail_df["TotalPrice"] = online_retail_df["Quantity"] * online_retail_df["UnitPrice"]
grouped_CID = online_retail_df.groupby("CustomerID")



# xに顧客の人数を代入
x = len(grouped_CID)

# yに顧客ごとの売り上げの累積和をリスト型で代入
y = grouped_CID.sum().loc[:, "TotalPrice"].sort_values().tolist()



# 累積和の最後の項が1になるように
x = np.arange(x) / x
y = np.array(y) / y[len(y)-1]

# グラフの要素に名前を
plt.title("Distribution of earings")
plt.xlabel("Cumulative sum of customers")
plt.ylabel("Cumulative sum of earings")
plt.axvline(x=0.8, linestyle='--')
plt.axhline(y=0.2, linestyle='--')
plt.plot(x, y)
plt.ylim([0, 0.2])
plt.show()
