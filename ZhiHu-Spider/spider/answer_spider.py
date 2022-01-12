# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     answer_spider
# Description:  
# CreateDate:   2021/12/25

import re
from queue import Queue

from util import WebRequest
from util import SaveData
from handler import ConfigHandler
from handler import LogHandler
from database import RedisClient
from helper import AnswerHelper
from thread import answer_thread_pool


class AnswerSpider(object):
    """
    采集思路：
    1. 根据question_id获取回答的json数据
    2. 从json数据中获取总共需要爬取的次数total_num
    3. 将question_id和answer_id进行组合，获取回答所在链接
    4. 多线程访问回答所在链接，解析并保存答案数据
    """

    def __init__(self, question_id):
        self.answer_info_table = list()
        self.question_id = question_id
        self.total = 0
        self.offset_num = 0
        self.cookie = None
        self.conf = ConfigHandler()
        self.log = LogHandler('question_spider')
        if self.conf.use_redis == 1:
            self.db = RedisClient(host=self.conf.redis_host, port=self.conf.redis_port, db=self.conf.redis_db,
                                  password=self.conf.redis_password)

    def run(self):
        base_url = 'https://www.zhihu.com/api/v4/questions/{question_id}/answers?offset={offset_num}&limit=20'.format(
            question_id=self.question_id, offset_num=self.offset_num)
        self.log.info('正在采集ID为 {} 的问题的第 {} 到 {} 个回答ID'.format(self.question_id, str(self.offset_num),
                                                              str(self.offset_num + 20)))
        res = WebRequest().get(base_url)
        self.total = res.json['paging']['totals']

        if self.conf.use_redis == 1:
            self.db.change_table(self.question_id)
        for data in res.json['data']:
            user_id = self.get_user_id(data)
            answer_id = self.get_answer_id(data)
            answer_dict = AnswerHelper(user_id=user_id, answer_id=answer_id, question_id=self.question_id)
            if self.conf.use_redis == 1:
                self.db.update(answer_dict)
            else:
                self.answer_info_table.append(answer_dict.to_json)
        if self.offset_num + 20 < self.total:
            self.offset_num += 20
            self.run()
        else:
            if self.conf.use_redis == 1:
                total = self.db.get_count()
            else:
                total = len(self.answer_info_table)
            self.log.info("共获取 {total} 条回答ID".format(total=total))
            if self.conf.use_redis == 1:
                answer_obj = self.db.get_all()
            else:
                answer_obj = self.answer_info_table
            answer_queue = Queue()
            for obj in answer_obj:
                answer_queue.put(obj)
            cnt = int(len(answer_obj) / 20) + 1
            for i in range(cnt):
                item_queue = Queue()
                for j in range(20):
                    try:
                        val = answer_queue.get(block=False)
                        item_queue.put(val)
                    except:
                        break
                output = answer_thread_pool(target_queue=item_queue, thread_num=self.conf.thread_num)
                SaveData(data=output, table_name='answer', unique_id='answer_id').run()
                self.log.info("第{}份数据已保存".format(i + 1))
            self.log.info("已完成对 {total} 条回答的采集工作！".format(total=total))

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
    pass
