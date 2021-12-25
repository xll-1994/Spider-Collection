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
from parser import AnswerParser
from database import MysqlClient


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
            base_url = 'https://www.zhihu.com/question/{question_id}/answer/{answer_id}'.format(
                question_id=question_id, answer_id=answer_id)
            time.sleep(0.5)
            res = WebRequest().get(base_url, cookie=self.cookie)
            self.cookie = res.set_cookies
            html_tree = res.tree
            content = html_tree.xpath(
                '//div[@class="QuestionAnswer-content"]/div/div/div[contains(@class,"RichContent--unescapable")]')[0]
            answer_detail = AnswerParser().get_detail(content)
            answer_detail['answer_url'] = base_url
            answer_detail['question_id'] = question_id
            answer_detail['answer_id'] = answer_id
            answer_detail['user_id'] = user_id
            answer_detail['insert_time'] = datetime.now()
            mysql_client = MysqlClient()
            mysql_client.save_answer(answer_detail)
