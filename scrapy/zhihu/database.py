# -*- coding: utf-8 -*-
# ProjectName:  ZhiHuSpider
# FileName:     database
# Description:  
# CreateDate:   2021/12/14
import pymysql

MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASS = '20190930'
MYSQL_DATABASE = 'zhi_hu_db'

CONNECTION = pymysql.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    database=MYSQL_DATABASE,
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)
