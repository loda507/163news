# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class WangyinewsPipeline(object):
    def __init__(self):

        dbargs = dict(
            host='localhost',
            db='test',
            user='root',
            passwd='123456',
            charset='utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode= True,
        )
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)

    #pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item)
        d.addErrback(self.handle_error)

        return item
    #将每行更新或写入数据库中
    def _do_upinsert(self, conn, item):
        if item.get('title'):
            conn.execute(\
                "insert into news (title, url, time, body)\
                values (%s, %s, %s, %s)",
                (item['title'],
                 item['url'],
                 item['time'],
                 item['body'])
                )
    def handle_error(self, e):
        log.err(e)

