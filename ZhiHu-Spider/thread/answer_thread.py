# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     answer_thread
# Description:  
# CreateDate:   2021/12/25

import json
import time
from datetime import datetime

from threading import Thread
from queue import Empty

from util import WebRequest
from util import SaveData
from parser import AnswerParser


class AnswerThread(Thread):

    def __init__(self, target_queue, thread_name, cookie):
        Thread.__init__(self, name=thread_name)
        self.target_queue = target_queue
        self.cookie = cookie

    def run(self):
        while True:
            try:
                answer = self.target_queue.get(block=False)
            except Empty:
                break
            data = json.loads(answer)
            question_id = data['question_id']
            answer_id = data['answer_id']
            user_id = data['user_id']
            answer_url = 'https://www.zhihu.com/question/{question_id}/answer/{answer_id}'.format(
                question_id=question_id, answer_id=answer_id)
            res = WebRequest().get(answer_url, cookie=self.cookie)
            time.sleep(0.5)
            self.cookie = res.set_cookies
            html_tree = res.tree
            content = html_tree.xpath(
                '//div[@class="QuestionAnswer-content"]/div/div/div[contains(@class,"RichContent--unescapable")]')[0]
            answer_detail = AnswerParser().get_detail(content)
            answer_detail['answer_url'] = answer_url
            answer_detail['question_id'] = question_id
            answer_detail['answer_id'] = answer_id
            answer_detail['user_id'] = user_id
            answer_detail['insert_time'] = datetime.now()
            SaveData(answer_detail).to_mysql('answer')


def answer_thread_pool(target_queue, cookie):
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
