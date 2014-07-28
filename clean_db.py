import MySQLdb, config, urllib, cgi, datetime, time
sql = MySQLdb.connect(host="localhost", 
                            user=config.username, 
                            passwd=config.passwd,
                            db=config.db)
sql.query("SELECT `id` FROM `feedurls`")
db_feed_query=sql.store_result()
rss_urls=db_feed_query.fetch_row(0)
table_name = "stories"
date_from = datetime.datetime.strptime(raw_input("start date inc. in form 'dd-mm-yyyy'"),"%d-%m-%Y")
date_to = datetime.datetime.strptime(raw_input("end date inc. in form 'dd-mm-yyyy'"),"%d-%m-%Y")
for rss_url_data in rss_urls:
    feed_id=rss_url_data[0]
    i = date_from 
    while i <= date_to:
        t0=time.clock()
        print i.strftime("%d/%m/%Y")
        whereclause="`date_added` = '" + i.strftime("%Y-%m-%d") + "'"
        whereclause+=" AND `feedid`= "+ str(feed_id) +""
        query="DELETE FROM stories WHERE " + whereclause 
        query+=" AND `url` NOT IN (SELECT * FROM (SELECT `url` FROM stories WHERE "+whereclause
        query+=" ORDER BY `points` DESC LIMIT 0,20) AS TAB);"
        print(time.clock()-t0)
        sql.query(query)
        sql.commit()
        i += datetime.timedelta(days=1)
 
