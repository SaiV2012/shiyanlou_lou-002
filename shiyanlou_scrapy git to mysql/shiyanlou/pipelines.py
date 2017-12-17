# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from shiyanlou.models import Repository, engine
import re
import time

class ShiyanlouPipeline(object):
    def process_item(self, item, spider):
        ls_temp = re.findall('\d+', item['update_time'])
        str_temp = "{t[0]}-{t[1]}-{t[2]} {t[3]}:{t[4]}:{t[5]}".format(t=ls_temp[0:6])
        item['update_time'] = str_temp
        #item['update_time'] = time.strptime(str_temp, "%Y-%m-%d %H:%M:%S")
        self.session.add(Repository(**item))
        return item

    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()
