# -*- coding: utf-8 -*-
# ProjectName:  ZhiHuSpider
# FileName:     database
# Description:  
# CreateDate:   2021/12/14
import pymysql
import os

MYSQL_HOST = os.environ.get('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
MYSQL_USER = os.environ.get('MYSQL_USER', 'username')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'password')
MYSQL_DATABASE = 'zhi_hu_db'

connection = pymysql.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE,
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)
