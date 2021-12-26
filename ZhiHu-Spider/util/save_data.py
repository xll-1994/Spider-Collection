# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     save_data
# Description:  
# CreateDate:   2021/12/25
import os

import xlwt
import xlrd
from xlutils.copy import copy

from database import MysqlClient
from database import MongoDBClient
from handler import ConfigHandler


class SaveData(object):

    def __init__(self, data, table_name, unique_id):
        self.data = data
        self.table_name = table_name
        self.unique_id = unique_id
        self.conf = ConfigHandler()

    def to_mysql(self):
        mysql_client = MysqlClient()
        mysql_client.save(self.data, table_name=self.table_name)

    def to_mongo(self):
        mongo_client = MongoDBClient()
        db = mongo_client.db
        db[self.table_name].update_one({self.unique_id: self.data[self.unique_id]}, {'$set': self.data}, upsert=True)

    def to_xls(self):
        file_name = 'data/{}/{}.xls'.format(self.table_name, self.table_name)
        try:
            rd_book = xlrd.open_workbook(file_name)
            rd_sheet = rd_book.sheet_by_name('sheet')
            sheet_rows = rd_sheet.nrows
            wt_book = copy(rd_book)
            wt_sheet = wt_book.get_sheet('sheet')
        except:
            os.makedirs('data/{}'.format(self.table_name))
            wt_book = xlwt.Workbook(encoding='utf-8')
            wt_sheet = wt_book.add_sheet('sheet')
            my_keys = list(self.data.keys())
            for col in range(len(my_keys)):
                wt_sheet.write(0, col, my_keys[col])
            sheet_rows = 1
        my_values = list(self.data.values())
        for col in range(len(my_values)):
            wt_sheet.write(sheet_rows, col, my_values[col])
        wt_book.save(file_name)

    def run(self):
        if self.conf.use_mysql == 1:
            self.to_mysql()
        if self.conf.use_mongo == 1:
            self.to_mongo()
        if self.conf.use_xls == 1:
            self.to_xls()
