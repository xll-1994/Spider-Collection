# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     save_data
# Description:  
# CreateDate:   2021/12/25

from database import MysqlClient
from database import MongoDBClient


class SaveData(object):

    def __init__(self, data):
        self.data = data

    def to_mysql(self, table_name):
        mysql_client = MysqlClient()
        mysql_client.save(self.data, table_name=table_name)

    def to_mongo(self, table_name, unique_id):
        mongo_client = MongoDBClient()
        db = mongo_client.db
        db[table_name].update_one({unique_id: self.data[unique_id]}, {'$set': self.data}, upsert=True)
