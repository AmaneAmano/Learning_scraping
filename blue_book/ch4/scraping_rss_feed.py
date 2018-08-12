import feedparser

url = "https://www.shoeisha.co.jp/rss/index.xml"
rss = feedparser.parse(url)

print(rss)

"""
print(type(rss))
print(issubclass(type(rss), dict))
<class 'feedparser.FeedParserDict'>は辞書クラスのサブクラス
よって、辞書のように値にアクセスできる
"""
for content in rss['entries']:
    print(f"{content['title']}: {content['link']}")

print(f"RSS version is {rss.version}")
print(f"Feed title is {rss['feed']['title']}")
print(f"Feed published date is {rss['feed']['published']}")