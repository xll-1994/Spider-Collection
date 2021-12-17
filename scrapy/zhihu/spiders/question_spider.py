import re
from abc import ABC
from datetime import datetime
import requests
import random

from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor

from zhihu.items import Question
from zhihu.util.cookies import default_cookies
from zhihu.util.user_agent_pool import user_agent_pool


class QuestionSpider(CrawlSpider, ABC):
    name = 'question_spider'
    allowed_domains = ['www.zhihu.com']
    start_urls = [
        'https://www.zhihu.com/question/437699743'
    ]
    rules = (
        Rule(
            LinkExtractor(allow=('https://www.zhihu.com/question/(\d+)$')),
            callback='parse_item',
            follow=True,
            process_request='_set_cookies'
        ),
    )

    def start_requests(self):
        for url in self.start_urls:
            cookie_value = default_cookies
            yield Request(url=url,
                          cookies={'KLBRSID': cookie_value},
                          # meta={
                          #     'dont_redirect': True,
                          #     'handle_httpstatus_list': [301, 302]
                          # }
                          )

    def parse_item(self, response):
        question_id = self._parse_question_id(response)
        if question_id:
            question = Question()
            question['question_id'] = question_id
            question['url'] = response.url
            question['title'] = self._parse_title(response)
            question['brief_intro'] = self._parse_brief_intro(response)
            question['follower_num'] = self._parse_follower_num(response)
            question['view_num'] = self._parse_view_num(response)
            question['answer_num'] = self._parse_answer_num(response)
            question['comment_num'] = self._parse_comment_num(response)
            question['vote_up_num'] = self._parse_vote_up_num(response)
            question['tag'] = self._parse_tags(response)
            regex = r'KLBRSID=(.*);'
            match = re.findall(regex, response.headers['set-cookie'].decode('utf-8'))
            question['cookies'] = match[0]
            question['proxy'] = response.request.meta['proxy']
            question_data = self._parse_related(response)
            temp = []
            for data in question_data:
                temp.append(str(data['id']))
            question['related'] = ','.join(temp)
            question['insert_time'] = datetime.now()
            yield question

        url = 'https://www.zhihu.com/api/v4/questions/{}/similar-questions?limit=5'.format(question_id)
        cookie_value = self._get_cookie_value(response)
        res = requests.get(url=url, cookies={'KLBRSID': cookie_value},
                           headers={'User-Agent': random.choice(user_agent_pool)}, timeout=5)
        for data in res.json()['data']:
            question_id = data['id']
            url = 'https://www.zhihu.com/question/' + str(question_id)
            yield Request(url=url,
                          cookies={'KLBRSID': cookie_value},
                          headers={'User-Agent': random.choice(user_agent_pool)},
                          callback=self.parse_item,
                          meta={
                              'dont_redirect': True,
                              'handle_httpstatus_list': [301, 302],
                              'download_timeout': 3
                          },
                          )

    @staticmethod
    def _set_cookies(request, response):
        regex = r'KLBRSID=(.*);'
        match = re.findall(regex, response.headers['set-cookie'].decode('utf-8'))
        if match:
            request.cookies['KLBRSID'] = match[0]
        return request

    @staticmethod
    def _parse_question_id(response):
        regex = r'https://www.zhihu.com/question/(\d+)$'
        match = re.findall(regex, response.url)
        if match:
            return match[0]
        return None

    @staticmethod
    def _parse_title(response):
        regex = '//h1[@class="QuestionHeader-title"]/text()'
        match = response.xpath(regex).get()
        if match:
            return match
        return None

    @staticmethod
    def _parse_brief_intro(response):
        regex = '//span[@itemprop="text"]/text()'
        match = response.xpath(regex).get()
        if match:
            return match
        return None

    @staticmethod
    def _parse_follower_num(response):
        regex = '//div[text()="关注者"]/following::strong/@title'
        match = response.xpath(regex).get()
        if match:
            return match
        return 0

    @staticmethod
    def _parse_view_num(response):
        regex = '//div[text()="被浏览"]/following::strong/@title'
        match = response.xpath(regex).get()
        if match:
            return match
        return 0

    @staticmethod
    def _parse_answer_num(response):
        regex = '//h4[@class="List-headerText"]/span/text()'
        match = response.xpath(regex).get()
        if match:
            temp = int(match.replace(',', ''))
            return temp
        return 0

    @staticmethod
    def _parse_comment_num(response):
        regex = '<\/path><\/svg><\/span>(\d+) 条评论<\/button>'
        match = re.findall(regex, response.text)
        if match:
            return match[0]
        return 0

    @staticmethod
    def _parse_vote_up_num(response):
        regex = r'<\/path><\/svg><\/span>好问题 (\d+)<\/button>'
        match = re.findall(regex, response.text)
        if match:
            return match[0]
        return 0

    @staticmethod
    def _parse_tags(response):
        regex = r'class=\"TopicLink\" href=\"\/\/www.zhihu.com\/topic\/(\d+)\"'
        matches = re.findall(regex, response.text)
        if matches:
            return ','.join(matches)
        return None

    def _parse_related(self, response):
        question_id = self._parse_question_id(response)
        cookie_value = self._get_cookie_value(response)
        url = 'https://www.zhihu.com/api/v4/questions/{}/similar-questions?limit=5'.format(question_id)
        res = requests.get(url=url, cookies={'KLBRSID': cookie_value},
                           headers={'User-Agent': random.choice(user_agent_pool)})
        return res.json()['data']

    @staticmethod
    def _get_cookie_value(response):
        regex = r'KLBRSID=(.*);'
        match = re.findall(regex, response.headers['set-cookie'].decode('utf-8'))
        return match[0]
