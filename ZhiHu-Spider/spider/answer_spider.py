# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     answer_spider
# Description:  
# CreateDate:   2021/12/25

import re
from queue import Queue

from util import WebRequest
from handler import ConfigHandler
from database import RedisClient
from helper import AnswerHelper
from thread import AnswerThread


class AnswerSpider(object):
    """
    采集思路：
    1. 根据question_id获取回答的json数据
    2. 从json数据中获取总共需要爬取的次数total_num
    3. 将question_id和answer_id进行组合，获取回答所在链接
    4. 多线程访问回答所在链接，解析并保存答案数据
    """

    def __init__(self, question_id):
        self.question_id = question_id
        self.total = 0
        self.offset_num = 0
        self.cookie = None
        self.conf = ConfigHandler()
        self.db = RedisClient(host=self.conf.redis_host, port=self.conf.redis_port, db=self.conf.redis_db,
                              password=self.conf.redis_password)

    def run(self):
        base_url = 'https://www.zhihu.com/api/v4/questions/{question_id}/answers?offset={offset_num}&limit=20'.format(
            question_id=self.question_id, offset_num=self.offset_num)
        res = WebRequest().get(base_url, cookie=self.cookie)
        self.cookie = res.set_cookies
        self.total = res.json['paging']['totals']
        self.db.change_table(self.question_id)
        for data in res.json['data']:
            user_id = self.get_user_id(data)
            answer_id = self.get_answer_id(data)
            answer_dict = AnswerHelper(user_id=user_id, answer_id=answer_id, question_id=self.question_id)
            self.db.update(answer_dict)
        if self.offset_num + 20 < self.total:
            self.offset_num += 20
            self.run()
        else:
            total = self.db.get_count()
            print("共获取{total}条回答信息".format(total=total))
            answer_obj = self.db.get_all()
            answer_queue = Queue()
            for obj in answer_obj:
                answer_queue.put(obj)
            cookie = self.cookie
            self.get_detail(target_queue=answer_queue, cookie=cookie)

    def get_detail(self, target_queue, cookie):
        thread_list = list()
        for _index in range(10):
            thread_list.append(
                AnswerThread(target_queue=target_queue, thread_name='thread_{}'.format(str(_index).zfill(2)),
                             cookie=cookie))

        for thread in thread_list:
            thread.setDaemon(True)
            thread.start()

        for thread in thread_list:
            thread.join()

    @staticmethod
    def get_user_id(data):
        return data['author']['id']

    @staticmethod
    def get_answer_id(data):
        answer_url = data['url']
        regex = 'answers\/(\d+)'
        match = re.findall(regex, answer_url)
        return match[0] if match else None


if __name__ == '__main__':
    AnswerSpider(266739695).run()
