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
        return os.environ.get("crawling_table", setting.CRAWLING_TABLE)

    @property
    def crawling_answer(self):
        return os.environ.get("crawling_answer", setting.CRAWLING_ANSWER)
