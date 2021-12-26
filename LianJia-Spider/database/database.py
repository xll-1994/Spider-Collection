# -*- coding: utf-8 -*-
# ProjectName:  LianJiaZuFangSpider
# FileName:     database
# Description:  
# CreateDate:   2021/12/11

from setting import MONGODB_HOST, MONGODB_PORT, MONGODB_USER, MONGODB_PASSWORD
from pymongo import MongoClient

Client = MongoClient(
    host=MONGODB_HOST,
    port=MONGODB_PORT,
    username=MONGODB_USER,
    password=MONGODB_PASSWORD
)
