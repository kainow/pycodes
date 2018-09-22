import pandas as pd
from time import sleep
import urllib.request
from bs4 import BeautifulSoup

# 取得するURL
url = "https://news.yahoo.co.jp/list/?c=domestic&d=20180721"
print(url[:52])
# データフレームの定義・初期化
df = pd.DataFrame(columns=["news"])


# スクレイピングするURLを引数に取る関数を定義
# ニュースのタイトル部分をまとめたデータフレームと遷移先URLを返す
def scraping(url):
    
    # データの読み込み、そしてBeautifulSoupによるパース
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "lxml")

    # dt要素のものを全て取得
    news_list = soup.find_all("dt")
    
    df_add = pd.DataFrame(columns=["news"])
    for news in news_list:
        news = news.text
        df_add = df_add.append(pd.DataFrame([[news]], columns=["news"]))[df_add.columns.tolist()]
    

    next_url = url[:52] + "&p=" + str(i+2) 
    
    
    return df_add,next_url

# scraping(url) を呼び出してスクレイピングを実行
# また、念の為アクセスする間隔を1秒あけるために sleep(1) を呼び出し
for i in range(5):
    df_add, url= scraping(url)
    print(url)
    df = df.append(df_add,ignore_index=True)
    sleep(1)
    
# スクレイピングしたデータに重複データがあることを確認
print("データの個数："+str(len(df)))
df[0:30]

#データに重複があるものは全て削除
df_cleansing = df.drop_duplicates(keep=False)
print("データの個数："+str(len(df_cleansing)))
df_cleansing[1:30]

#CSVでデータを保存
df_cleansing.to_csv("news.csv", index=False, encoding="UTF-8")
