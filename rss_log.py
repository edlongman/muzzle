import MySQLdb, feedparser
sql = MySQLdb.connect(host="localhost", # your host, usually localhost
                            user="root", # your username
                            passwd="", # your password
                            db="agnes") # name of the data base
rss_url = ""
feed = feedparser.parse(url)
items = feed [ 'items' ]
i = 0
while i < len(items):
    if sql.query('SELECT * FROM bbcfeeds WHERE url=' + items[i]['link'] + ' AND  date=' + items[i]['published'] ) == '':
      sql.query('INSERT INTO news_log ' + items[i]['link'] + ',' + items[i] + ',' + items[i]['summary'] + ',' + (len(items) - i * 1.002))
    else:
        curpoints = sql.query('SELECT FROM points WHERE url = ' + items[i]['link'])
        sql.query('UPDATE url = ' + items[i]['link'] + ' INSERT points ' + str(int(curpoints + curpoints * 1.002)))
    i = i + 1



