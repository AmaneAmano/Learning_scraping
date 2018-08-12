import feedparser
import MySQLdb

# connect database
connection = MySQLdb.connect(
    user='scrapingman',
    passwd='@h]Pm/&.#5?NW,<L',
    host='localhost',
    db='scrapingdata',
    charset='utf8'
)

# generate cursor
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS books")

# create books table
cursor.execute("CREATE TABLE books (title text, url text)")

url = "https://www.shoeisha.co.jp/rss/index.xml"
rss = feedparser.parse(url)

print(rss.version)

print(rss['feed']['title'])
print(rss['feed']['published'])

for content in rss['entries']:
    title = content['title']
    link = content['link']
    cursor.execute('INSERT INTO books VALUES (%s, %s)', (title, link))
    print(f"[SAVE] title: {title} - link: {link}")

connection.commit()
connection.close()
