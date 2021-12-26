# -*- coding: utf-8 -*-
# ProjectName:  LianJiaZuFangSpider
# FileName:     main
# Description:
# CreateDate:   2021/12/3

import random
import time
import re
from datetime import datetime

from database.database import Client
from setting import MONGODB_DATABASE, MONGODB_COLLECTION, INTERVAL_MIN_TIME, INTERVAL_MAX_TIME, REST_MAX_TIME, \
    REST_MIN_TIME
from spiders.model_spider import ModelSpider
from proxy_pool.proxy_pool import ProxyPool

# 配置IP代理池
proxy_pool = ProxyPool()

# 连接数据库
database = MONGODB_DATABASE
collection = MONGODB_COLLECTION
db = Client[database]
db[collection].create_index('house_code', unique=True)


class RentSpider(ModelSpider):

    def __init__(self):
        self.rest_min_time = INTERVAL_MIN_TIME
        self.rest_max_time = INTERVAL_MAX_TIME
        self.interval_min_time = REST_MIN_TIME
        self.interval_max_time = REST_MAX_TIME

    def get_city(self, url="https://www.lianjia.com/city/"):
        res = proxy_pool.get_response(url, headers=self._random_headers())
        regex = r'<li>\s*<a href=\"(.*com\/)\">(.*)<\/a>\s*<\/li>'
        matches = re.findall(regex, res.text)
        if matches:
            old_dict = dict(matches)
            new_dict = {}
            for key, value in old_dict.items():
                new_dict[value] = key
            return new_dict
        return None

    def get_district(self, url, city_id):
        time.sleep(self.interval_min_time)
        url = url + 'zufang'
        res = proxy_pool.get_response(url, headers=self._random_headers(), city_id=city_id)
        regex = r'data-type=\"district\" class=\"filter__item--level2  \">\s*<a href=\"\/zufang\/(.*)\/\"\s*>(.*)<\/a>'
        matches = re.findall(regex, res.text)
        if matches:
            old_dict = dict(matches)
            new_dict = {}
            for key, value in old_dict.items():
                new_dict[value] = key
            return new_dict
        return None

    def get_biz_circle(self, url, city_id):
        time.sleep(self.interval_min_time)
        res = proxy_pool.get_response(url, headers=self._random_headers(), city_id=city_id)
        regex = r'data-type=\"bizcircle\"\s+class=\"filter__item--level3  \">\s+<a href=\"\/zufang\/(.*)\/\">(.*)<'
        matches = re.findall(regex, res.text)
        old_dict = dict(matches)
        new_dict = {}
        for key, value in old_dict.items():
            new_dict[value] = key
        return new_dict

    def get_city_id(self, url):
        url = url + 'ershoufang'
        res = proxy_pool.get_response(url, headers=self._random_headers())
        regex = r'city_id: \'(\d+)\''
        match = re.findall(regex, res.text)
        if match:
            return match[0]
        return None

    def get_data(self, city_id=110000, city_name="北京", district_letters=None, district_name=None,
                 biz_circle_letters='andingmen', biz_circle_name='安定门'):
        idx = 0
        has_more = 1
        while has_more:
            try:
                url = 'https://app.api.lianjia.com/Rentplat/v1/house/list/'
                params = {
                    'city_id': city_id,
                    'condition': biz_circle_letters,
                    'limit': 30,
                    'offset': idx * 30,
                    'request_ts': int(time.time()),
                    'scene': 'list',
                }
                res = proxy_pool.get_response(
                    url=url,
                    params=params,
                    headers=self._random_headers()
                )
                item = {
                    'city_id': city_id,
                    'city_name': city_name,
                    'district_name': district_name,
                    'district_letters': district_letters,
                    'biz_circle_name': biz_circle_name,
                    'biz_circle_letters': biz_circle_letters
                }
                total = res.json()['data']['total']
                if total > 0:
                    self._parse_item(res.json()['data']['list'], item)
                idx += 1
                if total / 30 <= idx:
                    has_more = 0
            except Exception:
                print("没有可以获取的数据")
        print("{}-{}-{}的出租数据已成功保存到数据库中！".format(city_name, district_name, biz_circle_name))
        time.sleep(random.randint(self.rest_min_time, self.rest_max_time))

    def _parse_item(self, dataset, item):
        if len(dataset) > 0:
            for data in dataset:
                print("正在获取 {} 的详细数据...".format(data.get('house_title')))
                time.sleep(random.randint(self.interval_min_time, self.interval_max_time))
                item['rent_type'] = data.get('rent_type')
                item['house_code'] = data.get('house_code')
                item['lianjia_house_code'] = data.get('lianjia_house_code')
                item['bedroom_num'] = data.get('frame_bedroom_num')
                item['hall_num'] = data.get('frame_hall_num')
                item['bathroom_num'] = data.get('frame_bathroom_num')
                item['kitchen_num'] = data.get('frame_kitchen_num')
                item['rent_area'] = data.get('rent_area')
                item['house_title'] = data.get('house_title')
                item['resblock_name'] = data.get('resblock_name')
                item['layout'] = data.get('layout')
                item['rent_price_listing'] = data.get('rent_price_listing')
                item['orientation'] = data.get('frame_orientation')
                item['pc_url'] = data.get('pc_url')
                item['rent_price_unit'] = data.get('rent_price_unit')
                item['house_tag'] = self._parse_house_tags(data.get('house_tags'))
                item['insert_time'] = datetime.now()

                res = proxy_pool.get_response(
                    url=item['pc_url'],
                    headers=self._random_headers(),
                    city_id=item['city_id']
                )

                item['longitude'] = self._parse_longitude_tag(res)
                item['latitude'] = self._parse_latitude_tag(res)
                item['maintenance'] = self._parse_maintenance_tag(res)
                item['check_in'] = self._parse_check_in_tag(res)
                item['floor'] = self._parse_floor_tag(res)
                item['heating'] = self._parse_heating_tag(res)
                item['term'] = self._parse_term_tag(res)
                item['visit'] = self._parse_visit_tag(res)

                self._save_data(item)

    @staticmethod
    def _save_data(item):
        db[collection].update_one({'house_code': item['house_code']}, {'$set': item}, upsert=True)

    @staticmethod
    def _parse_longitude_tag(res):
        regex = r'longitude: \'(.*)\','
        match = re.findall(regex, res.text)
        if match:
            return match[0]
        return None

    @staticmethod
    def _parse_latitude_tag(res):
        regex = r'latitude: \'(.*)\''
        match = re.findall(regex, res.text)
        if match:
            return match[0]
        return None

    @staticmethod
    def _parse_maintenance_tag(res):
        regex = r'房源维护时间：(\d+-\d+-\d+)\s'
        match = re.findall(regex, res.text)
        if match:
            return match[0]
        return None

    @staticmethod
    def _parse_check_in_tag(res):
        regex = r'<li class=\"fl oneline\">入住：(.*)<\/li>'
        match = re.findall(regex, res.text)
        if match:
            return match[0]
        return None

    @staticmethod
    def _parse_floor_tag(res):
        regex = r'<li class=\"fl oneline\">楼层：(.*)<\/li>'
        match = re.findall(regex, res.text)
        if match:
            return match[0]
        return None

    @staticmethod
    def _parse_heating_tag(res):
        regex = r'<li class=\"fl oneline\">采暖：(.*)<\/li>'
        match = re.findall(regex, res.text)
        if match:
            return match[0]
        return None

    @staticmethod
    def _parse_term_tag(res):
        regex = r'<li class=\"fl oneline\">租期：(.*)<\/li>'
        match = re.findall(regex, res.text)
        if match:
            return match[0]
        return None

    @staticmethod
    def _parse_visit_tag(res):
        regex = r'<li class=\"fl oneline\">看房：(.*)<\/li>'
        match = re.findall(regex, res.text)
        if match:
            return match[0]
        return None

    @staticmethod
    def _parse_house_tags(house_tag):
        if len(house_tag) > 0:
            st = ''
            for tag in house_tag:
                st += tag.get('name') + ' '
            return st.strip()
        return None
