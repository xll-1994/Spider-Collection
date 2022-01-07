# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     answer_thread
# Description:  
# CreateDate:   2021/12/25

import json
from datetime import datetime

from threading import Thread
from queue import Empty

from util import WebRequest
from util import SaveData
from itemparser import AnswerParser
from handler import LogHandler


class AnswerThread(Thread):

    def __init__(self, target_queue, thread_name):
        Thread.__init__(self, name=thread_name)
        self.target_queue = target_queue
        self.log = LogHandler('answer_thread')

    def run(self):
        self.log.info("{} 开始工作".format(self.name))
        while True:
            try:
                answer = self.target_queue.get(block=False)
            except Empty:
                self.log.info("{} 结束工作".format(self.name))
                break
            data = json.loads(answer)
            question_id = data['question_id']
            answer_id = data['answer_id']
            user_id = data['user_id']
            answer_url = 'https://www.zhihu.com/question/{question_id}/answer/{answer_id}'.format(
                question_id=question_id, answer_id=answer_id)
            res = WebRequest().get(answer_url)
            html_tree = res.tree
            content = html_tree.xpath(
                '//div[@class="QuestionAnswer-content"]/div/div/div[contains(@class,"RichContent--unescapable")]')[0]
            answer_detail = AnswerParser().get_detail(content)
            answer_detail['answer_url'] = answer_url
            answer_detail['question_id'] = question_id
            answer_detail['answer_id'] = answer_id
            answer_detail['user_id'] = user_id
            answer_detail['insert_time'] = datetime.now()
            SaveData(data=answer_detail, table_name='answer', unique_id='answer_id').run()
            self.log.info("{} 完成了对回答ID {} 的访问".format(self.name, answer_id.ljust(10)))
            self.target_queue.task_done()


def answer_thread_pool(target_queue, thread_num):
    thread_list = list()
    for _index in range(thread_num):
        thread_list.append(
            AnswerThread(target_queue=target_queue, thread_name='thread_{}'.format(str(_index + 1).zfill(2))))

    for thread in thread_list:
        thread.setDaemon(True)
        thread.start()

    for thread in thread_list:
        thread.join()
