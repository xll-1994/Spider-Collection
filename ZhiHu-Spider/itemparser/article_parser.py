# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     article_parser
# Description:  
# CreateDate:   2022/1/12

import re

from lxml import etree


class ArticleParser:

    def get_detail(self, content=None):
        article_detail = dict()
        article_detail["user_id"] = self.parse_user_id(content)
        article_detail["title"] = self.parse_title(content)
        article_detail["edit_time"] = self.parse_edit_time(content)
        article_detail["vote_up_num"] = self.parse_vote_up_num(content)
        article_detail["comment_num"] = self.parse_comment_num(content)
        article_detail["tag"] = self.parse_tag(content)
        article_detail["content_tree"] = self.parse_content_tree(content)
        article_detail["content"] = self.parse_content(content)
        return article_detail

    @staticmethod
    def parse_user_id(content):
        text = content.xpath('//script[@id="js-initialData"]/text()')[0]
        regex = r'\",\"id\":\"([^\"]+)\"'
        match = re.findall(regex, text)
        if match:
            return match[0]
        return None

    @staticmethod
    def parse_title(content):
        text = content.xpath('//h1/text()')
        if text:
            return text[0]
        return None

    @staticmethod
    def parse_vote_up_num(content):
        text = content.xpath('//header/div/span[@class="Voters"]/button/text()')[0]
        regex = r'(\d+)'
        match = re.findall(regex, text)
        if match:
            return int(match[0])
        return 0

    @staticmethod
    def parse_edit_time(content):
        text = content.xpath('//div[@class="ContentItem-time"]/text()')[0]
        regex = r'于 (.*)'
        match = re.findall(regex, text)
        if match:
            return match[0]
        return None

    @staticmethod
    def parse_comment_num(content):
        text = content.xpath(
            '//div[@class="Sticky RichContent-actions is-bottom"]/div/div[@class="css-qbubgm"]/button/text()')[0]
        regex = r'(\d+)'
        match = re.findall(regex, text)
        if match:
            return int(match[0])
        return 0

    @staticmethod
    def parse_tag(content):
        text = content.xpath('//span[@class="Tag-content"]/a/div/div/text()')
        if text:
            return ' '.join(text)
        return None

    @staticmethod
    def parse_content_tree(content):
        content_tree = content.xpath('//div[@class="RichText ztext Post-RichText css-hnrfcf"]')[0]
        content_str = etree.tostring(content_tree, encoding='utf-8')
        return content_str.decode("utf-8")

    def parse_content(self, content):
        content_str = self.parse_content_tree(content)
        regex = r'>([^<]+)<'
        matches = ''.join(re.findall(regex, content_str))
        return matches
