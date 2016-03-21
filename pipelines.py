# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

con = MySQLdb.connect(host="localhost",  # your host, usually localhost
                      user="lenta",  # your username
                      passwd="password",  # your password
                      db="lenta")
query_url = 'INSERT INTO Pages (Url) VALUES ("{}")'
query_url_id = 'SELECT LAST_INSERT_ID()'
query_rank = 'INSERT INTO PersonPageRank (PersonID, PageID, Rank) VALUES ({},{},{})'

# select ke.Name, per.Rank, pa.Url FROM PersonPageRank per INNER JOIN Keywords ke ON per.PersonID  = ke.PersonID INNER JOIN Pages pa ON per.PageID = pa.ID WHERE Rank> 10;

keywords = {u'кадыров': 2, u'немцов': 1, u'навальн': 3, u'гундяев': 5, u'лужков': 6}


class LentaPipeline(object):
    def process_item(self, item, spider):
        with con:
            cur = con.cursor()
            cur.execute(query_url.format(item['url']))
            cur.execute(query_url_id)
            page_id = cur.fetchone()[0]
            for person_name, person_id in keywords.items():
                pr = item['post_body'].lower().count(person_name)
                if pr > 0:
                    cur.execute(query_rank.format(person_id, page_id, pr))
        return item
