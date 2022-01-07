# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     answer_parser
# Description:  
# CreateDate:   2021/12/25

import re
from datetime import datetime

from lxml import etree


class AnswerParser(object):

    def get_detail(self, content):
        answer_detail = dict()
        answer_detail['answer_content_tree'] = self.parse_answer_content_tree(content)
        answer_detail['answer_content'] = self.parse_answer_content(content)
        answer_detail['edit_time'] = self.parse_publish_time(content)
        answer_detail['vote_up_num'] = self.parse_vote_up_num(content)
        answer_detail['comment_num'] = self.parse_comment_num(content)
        return answer_detail

    @staticmethod
    def parse_answer_content_tree(content):
        content_tree = content.xpath('./div[@class="RichContent-inner"]/span[1]')[0]
        content_str = etree.tostring(content_tree, encoding='utf-8')
        return content_str.decode("utf-8")

    def parse_answer_content(self, content):
        content_str = self.parse_answer_content_tree(content)
        regex = r'>([^<]+)<'
        matches = ''.join(re.findall(regex, content_str))
        return matches

    @staticmethod
    def parse_publish_time(content):
        text = content.xpath('./div/div[@class="ContentItem-time"]/a/span/@data-tooltip')[0]
        regex = r'于 (.*)'
        match = re.findall(regex, text)
        publish_time = datetime.strptime(match[0], '%Y-%m-%d %H:%M')
        return publish_time

    @staticmethod
    def parse_vote_up_num(content):
        text = content.xpath('./div[@class="ContentItem-actions RichContent-actions"]/span/button[1]/@aria-label')[
            0]
        regex = r'赞同 (\d+)'
        match = re.findall(regex, text)
        return int(match[0]) if match else 0

    @staticmethod
    def parse_comment_num(content):
        text = content.xpath('./div[@class="ContentItem-actions RichContent-actions"]/button[1]/text()')[0]
        regex = r'(\d+) 条评论'
        match = re.findall(regex, text)
        return int(match[0]) if match else 0
