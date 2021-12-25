# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     redis_client
# Description:  
# CreateDate:   2021/12/25

import random

from redis.client import Redis
from redis.connection import BlockingConnectionPool


class RedisClient(object):

    def __init__(self, **kwargs):
        self.name = ''
        self.__conn = Redis(connection_pool=BlockingConnectionPool(
            decode_responses=True,
            timeout=5,
            socket_timeout=5,
            **kwargs
        ))

    def change_table(self, name):
        self.name = name

    def get_all(self):
        return self.__conn.hvals(self.name)

    def get(self):
        items = self.get_all()
        return random.choice(items)

    def delete(self, answer_id):
        return self.__conn.hdel(self.name, answer_id)

    def update(self, answer_obj):
        return self.__conn.hset(self.name, answer_obj.answer_id, answer_obj.to_json)

    def put(self, answer_obj):
        return self.__conn.hset(self.name, answer_obj.answer_id, answer_obj.to_json)

    def exists(self, answer_id):
        return self.__conn.hexists(self.name, answer_id)

    def get_all(self):
        return self.__conn.hvals(self.name)

    def get_count(self):
        return len(self.get_all())
