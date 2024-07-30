import requests
from bs4 import BeautifulSoup
import re
import time

url = "https://www.yahoo.co.jp/"

res = requests.get(url)

if res.status_code == 200:
    print("URLをfetchすることに成功しました。")
else:
    print(f"URLをfetchすることに失敗しました。Status code: {res.status_code}")

# html.parserでページを解析
soup = BeautifulSoup(res.text, "html.parser")

# href属性に"news.yahoo.co.jp/pickup"が含まれる要素をすべて選択する
elems = soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))

# タイトル・URLが入る空のリストを作成
elem_titles = []
elem_urls = []

# リスト内包表記
# タイトル・URLを取得してリストに入れる
elem_titles = [elem.span.string for elem in elems]
elem_urls = [elem.attrs["href"] for elem in elems]

# デバッグ用
#print(elem_titles)
#print(elem_urls)

#ループ処理でニュースのタイトルとURLをリストから取り出す
#取り出したURLからページを取得する
#取得したページをhtml.parserで解析する
for news_title, pickup_url in zip(elem_titles, elem_urls):
    pickup_res = requests.get(pickup_url)
    pickup_soup = BeautifulSoup(pickup_res.text, "html.parser")
    
    #pickup_soupに格納したページのデータから記事が格納されたものを取りだす
    #news_urlに記事本文へのURLを格納する
    pickup_elem = pickup_soup.find("div", class_="sc-gdv5m1-8 eMtbmz")
    news_url = pickup_elem.a.attrs["href"]
    
    #記事のタイトルとURLを出力
    print(news_title)
    print(news_url, end="\n\n")
    
    #1秒ごとにループ処理を実行
    time.sleep(1)