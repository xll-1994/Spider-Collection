# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     mysql_client
# Description:  
# CreateDate:   2021/12/25

import pymysql

from handler import ConfigHandler


class MysqlClient(object):

    def __init__(self):
        conf = ConfigHandler()
        self.__conn = pymysql.connect(
            host=conf.mysql_host,
            port=conf.mysql_port,
            user=conf.mysql_username,
            password=conf.mysql_password,
            database=conf.mysql_database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.__cursor = self.__conn.cursor()

    def save(self, answer_detail, table_name):
        keys = answer_detail.keys()
        values = tuple(answer_detail.values())
        fields = ','.join(keys)
        temp = ','.join(['%s'] * len(keys))
        sql = 'INSERT INTO {table_name} ({fields}) VALUES ({temp})'.format(table_name=table_name, fields=fields,
                                                                           temp=temp)
        self.__cursor.execute(sql, values)
        return self.__conn.commit()
