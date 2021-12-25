# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     mongo_client
# Description:  
# CreateDate:   2021/12/25

from pymongo import MongoClient

from handler import ConfigHandler


class MongoDBClient(object):

    def __init__(self):
        self.cnf = ConfigHandler()
        self.__conn = MongoClient(
            host=self.cnf.mongo_host,
            port=self.cnf.mongo_port,
            username=self.cnf.mongo_username,
            password=self.cnf.mongo_password
        )
        self.db = self.__conn[self.cnf.mongo_database]
