# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     save_data
# Description:  
# CreateDate:   2021/12/25

from database import MysqlClient


class SaveData(object):

    def __init__(self, data):
        self.data = data

    def to_mysql(self, table_name):
        mysql_client = MysqlClient()
        mysql_client.save(self.data, table_name=table_name)

