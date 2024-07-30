#モジュールのインポート
import requests
from bs4 import BeautifulSoup
import time
import re

#Yahoo!JAPANからデータを取得
url = "https://www.yahoo.co.jp/"
res = requests.get(url)

#fetchに成功したかどうかの確認
if res.status_code == 200:
    print("URLをfetchすることに成功しました。")
else:
    print(f"URLをfetchすることに失敗しました。Status code: {res.status_code}")

#html.parserでサイトを解析
soup = BeautifulSoup(res.text, "html.parser")

#全ての要素を指定
elems = soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))

#タイトルのリストを初期化
#URLのリストを初期化
elems_titles = []
elems_urls = []

#elemsからタイトルとURLを取得
for title in elems:
    elems_titles.append(title.get_text(strip=True))
    elems_urls.append(title.attrs["href"])

#記事タイトルとURLの数を表示
print(f"主要ニュースの記事のタイトルの数: {len(elems_titles)}")
print(f"主要ニュースの記事のURLの数: {len(elems_urls)}")

#タイトルとURLを表示
for title, url in zip(elems_titles, elems_urls):
    print(title)
    print(url, end="\n\n")