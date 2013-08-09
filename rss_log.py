import MySQLdb, feedparser, config, urllib, cgi, datetime
sql = MySQLdb.connect(host="localhost", 
                            user=config.username, 
                            passwd=config.passwd,
                            db=config.db)
rss_urls = (('news' , 'http://feeds.bbci.co.uk/news/rss.xml?edition=uk') , ('technology' , 'http://feeds.bbci.co.uk/news/technology/rss.xml'))
table_name = "bbcstories"
feed = feedparser.parse(rss_urls)
items = feed [ 'items' ]
i = 0
def algo(pts,pos):
	return pts * (1+0.02/(pos+1))
for rss_url_data in rss_urls:
	while i < len(items):
		section_name = rss_url_data[0]
		rss_url = rss_url_data[1]
		item=items[i];
		conditions=' WHERE url="' + item['id'] + '" AND  date_added=CURDATE()'
		sql.query('SELECT points FROM '+ table_name + conditions)
		points_result=sql.store_result();
		item['title']=urllib.quote(item['title'].encode('utf-8'))
		item['summary']=urllib.quote(item['summary'].encode('utf-8'))
		if len(item['media_thumbnail'])==1:
			item['media_thumbnail'].append(item['media_thumbnail'][0])
		if points_result.num_rows()==0:#if the url has not been logged today
			query='INSERT INTO '+ table_name +' (`url`,`title`,`description`,`points`,`date_added`,`small_thumb`,`large_thumb`,`section`) VALUES("' + item['id'] + '","' + item['title'] + '","' + item['summary'] + '",' + str(algo(1,i)) + ',CURDATE(),"'
			query+=item['media_thumbnail'][0]['url']+'","'+item['media_thumbnail'][1]['url']+'","'+ section_name +'")'
			sql.query(query)#then add it to the db, setting points to 1 * (1.02/list_postition)
			insert_result=sql.store_result()
		else:
			row = points_result.fetch_row()
			currpoints=float(row[0][0])
			sql.query('UPDATE '+ table_name +' SET points=' + str(algo(currpoints,i)) + ',title="' + item['title'] + '",description="' + item['summary']  + '",small_thumb="' + item['media_thumbnail'][0]['url'] + '",large_thumb="' + item['media_thumbnail'][1]['url']+ '"' + conditions)#and update the points
		i = i + 1
timenow=datetime.datetime.now()
print "success at: " + timenow.strftime('%d-%m-%y %H:%M\n')
#Fields I want: id INT, url VARSTRING(255), date (#a mysql date format), title VARSTRING(140), desc VARSTRING(255), points INT
