#モジュールのインポート
import requests
from bs4 import BeautifulSoup
import time
import re
import textwrap

#Yahoo!JAPANのページのデータを取得
url = "https://www.yahoo.co.jp/"
res = requests.get(url)

#parserでデータを解析
soup = BeautifulSoup(res.text, "html.parser")

#news.yahoo.co.jp/pickupで絞り込む
#news.yahoo.co.jp/expertで絞り込む
elems_pickup = soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))
elems_expert = soup.find_all(href=re.compile("news.yahoo.co.jp/expert"))

#print(elems_pickup)
#print(elems_expert, end="\n\n")

elems = elems_pickup or elems_expert

#要約記事のタイトルとURLのリストの初期化
elem_titles = []
elem_urls = []

#リスト化
elem_titles = [elem.span.string for elem in elems]
elem_urls = [elem.attrs["href"] for elem in elems]

print(elem_titles)
#print(elem_urls, end="\n\n")

#ループ処理でニュースのタイトルとURLをリストから取り出す
#取り出したURLからページを取得する
#取得したページをhtml.parserで解析する
for news_title, pickup_url in zip(elem_titles, elem_urls):
    pickup_res = requests.get(pickup_url)
    pickup_soup = BeautifulSoup(pickup_res.text, "html.parser")
    
    #pickup_soupに格納したページのデータから記事が格納されたものを取りだす
    #news_urlに記事本文へのURLを格納する
    pickup_elems = pickup_soup.find("div", class_="sc-gdv5m1-8 eMtbmz")
    news_url = pickup_elems.a.attrs["href"]
    
    #記事本文へのURLからページを取得
    #取得したページをhtml.parserで解析
    article_res = requests.get(news_url)
    article_soup = BeautifulSoup(article_res.text, "html.parser")
    
    #クラス名で絞り込む
    class_name_1 = "sc-54nboa-0"
    class_name_2 = "deLyrJ"
    class_name_3 = "yjSlinkDirectlink"
    class_name_4 = "highLightSearchTarget"
    
    class_name_pattern = class_name_1 or class_name_2 or class_name_3 or class_name_4
    
    article_element = article_soup.find(class_=class_name_pattern)
    
    #要素が存在するか確認し、存在する場合のみテキストを取得
    if article_element is not None:
        article_text = article_element.text
        #textwrapモジュールを使う
        #そのまま出力すると文章が横に長くなって読みにくいから改行する
        def wrap_text(article_text, width=95):
            return "\n".join(textwrap.wrap(article_text, width))
        #結果の出力
        print(article_soup.title.text)
        print(news_url)
        print(wrap_text(article_text), end="\n\n")
    else:
        print("指定された要素が見つかりませんでした。", end="\n\n")
    
    time.sleep(1)