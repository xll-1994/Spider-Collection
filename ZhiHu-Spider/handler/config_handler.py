# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     config_handler
# Description:  
# CreateDate:   2021/12/25

import os

import setting


class ConfigHandler(object):

    @property
    def mysql_host(self):
        return os.environ.get("MYSQL_HOST", setting.MYSQL_HOST)

    @property
    def mysql_port(self):
        return int(os.environ.get("MYSQL_PORT", setting.MYSQL_PORT))

    @property
    def mysql_username(self):
        return os.environ.get("MYSQL_USERNAME", setting.MYSQL_USERNAME)

    @property
    def mysql_password(self):
        return os.environ.get("MYSQL_PASSWORD", setting.MYSQL_PASSWORD)

    @property
    def mysql_database(self):
        return os.environ.get("MYSQL_DATABASE", setting.MYSQL_DATABASE)

    @property
    def proxy_host(self):
        return os.environ.get("PROXY_HOST", setting.PROXY_HOST)

    @property
    def proxy_port(self):
        return int(os.environ.get("PROXY_PORT", setting.PROXY_PORT))

    @property
    def retry_time(self):
        return int(os.environ.get("RETRY_TIME", setting.RETRY_TIME))

    @property
    def retry_interval(self):
        return int(os.environ.get("RETRY_INTERVAL", setting.RETRY_INTERVAL))

    @property
    def timeout(self):
        return int(os.environ.get("TIMEOUT", setting.TIMEOUT))

    @property
    def use_redis(self):
        return int(os.environ.get('USE_REDIS', setting.USE_REDIS))

    @property
    def redis_host(self):
        return os.environ.get("REDIS_HOST", setting.REDIS_HOST)

    @property
    def redis_port(self):
        return os.environ.get("REDIS_PORT", setting.REDIS_PORT)

    @property
    def redis_db(self):
        return os.environ.get("REDIS_DB", setting.REDIS_DB)

    @property
    def redis_password(self):
        return os.environ.get("REDIS_PASSWORD", setting.REDIS_PASSWORD)

    @property
    def crawled_table(self):
        return os.environ.get("CRAWLED_TABLE", setting.CRAWLED_TABLE)

    @property
    def crawling_table(self):
        return os.environ.get("CRAWLING_TABLE", setting.CRAWLING_TABLE)

    @property
    def crawling_answer(self):
        return os.environ.get("CRAWLING_ANSWER", setting.CRAWLING_ANSWER)

    @property
    def mongo_host(self):
        return os.environ.get('MONGO_HOST', setting.MONGO_HOST)

    @property
    def mongo_port(self):
        return int(os.environ.get('MONGO_PORT', setting.MONGO_PORT))

    @property
    def mongo_username(self):
        return os.environ.get('MONGO_USERNAME', setting.MONGO_USERNAME)

    @property
    def mongo_password(self):
        return os.environ.get('MONGO_PASSWORD', setting.MONGO_PASSWORD)

    @property
    def mongo_database(self):
        return os.environ.get('MONGO_DATABASE', setting.MONGO_DATABASE)

    @property
    def use_mysql(self):
        return int(os.environ.get('USE_MYSQL', setting.USE_MYSQL))

    @property
    def use_mongo(self):
        return int(os.environ.get('USE_MONGO', setting.USE_MONGO))

    @property
    def use_xls(self):
        return int(os.environ.get('USE_XLS', setting.USE_XLS))

    @property
    def use_proxy(self):
        return int(os.environ.get('USE_PROXY', setting.USE_PROXY))

    @property
    def thread_num(self):
        return int(os.environ.get('THREAD_NUM', setting.THREAD_NUM))

    @property
    def interval_time(self):
        return float(os.environ.get('INTERVAL_TIME', setting.INTERVAL_TIME))
