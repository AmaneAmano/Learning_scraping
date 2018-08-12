import MySQLdb

connection = MySQLdb.connect(
    user='scrapingman',
    passwd='@h]Pm/&.#5?NW,<L',
    host='localhost',
    db='scrapingdata',
    charset='utf8'
)

cursor = connection.cursor()
r = cursor.execute("INSERT INTO books VALUES (%s, %s)",
                   ('Pythonによるクローラー＆スクレイピング入門 設計・開発から収集データの解析まで ', 'http://amzn.asia/cbfU3py'))
print(r)
connection.commit()
connection.close()

