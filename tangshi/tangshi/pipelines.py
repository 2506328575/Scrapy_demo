# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymongo
class TangshiPipeline(object):
    def __init__(self):
        print('>'*30,'正在连接数据库')
        host='localhost'
        port=27017
        self.client=pymongo.MongoClient(host,port)
    def process_item(self, item, spider):
        data=dict(item)
        mydb=self.client['诗词']
        mydb_sheet_name=mydb['item']
        print('>>>>>>正在插入数据')
        mydb_sheet_name.insert(data)
        return item
    def close_spider(self,spider):
        print('>>>>>>>>>>>关闭数据库<<<<<<<<<<<<<<')

