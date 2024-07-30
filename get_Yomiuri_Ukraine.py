#requestsとBeautifulSoup4をインポート
import requests
from bs4 import BeautifulSoup

#読売新聞オンラインのウクライナ情勢のページのデータを取得
url = 'https://www.yomiuri.co.jp/feature/titlelist/ukraine_news/'
res = requests.get(url)

#ステータスコードを取得
res.status_code

#html.parserで解析
soup = BeautifulSoup(res.text, "html.parser")

#CSSセレクターで絞り込む
elems = soup.select("body > div.layout-contents > div.layout-contents__main")

#リストelemsからh3タグで絞り込む
#h3_elemsからテキストを取得
h3_elems = elems[0].find_all("h3", class_="c-list-title")
h3_texts = [h3.get_text(strip=True) for h3 in h3_elems]

#初期化
a_texts = []
a_urls = []

#ループ処理
for h3 in h3_elems:
    #h3の中のデータをaタグで絞り込む
    a_tag = h3.find("a")
    #もしaタグかテキストの入ったaタグが存在したら
    if a_tag and a_tag.get_text(strip=True):
        #リストa_textsにaタグの中のテキストを追加
        #リストa_urlsにaタグの中のURLを追加
        a_texts.append(a_tag.get_text(strip=True))
        a_urls.append(a_tag.get("href"))

#ループ処理
#titleとurlに、a_textとa_urlsの要素を一つずつ格納
for title, url in zip(a_texts, a_urls):
    #タイトルを表示
    #URLを表示して改行
    print(title)
    print("https://www.yomiuri.co.jp/" + url, end="\n\n")