# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     log_handler
# Description:  
# CreateDate:   2021/12/25

import logging
import os
from logging.handlers import TimedRotatingFileHandler

# 日志级别
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(CURRENT_PATH, os.pardir)
LOG_PATH = os.path.join(ROOT_PATH, 'log')

if not os.path.exists(LOG_PATH):
    try:
        os.mkdir(LOG_PATH)
    except FileExistsError:
        pass


class LogHandler(logging.Logger):

    def __init__(self, name, level=DEBUG, stream=True, file=True):
        self.name = name
        self.level = level
        logging.Logger.__init__(self, self.name, self.level)
        if stream:
            self._set_stream_handler()
        if file:
            self._set_file_handler()

    def _set_file_handler(self, level=None):
        file_name = os.path.join(LOG_PATH, '{name}.log'.format(name=self.name))
        file_handler = TimedRotatingFileHandler(filename=file_name, when='D', interval=1, backupCount=15)
        file_handler.suffix = '%Y%m%d.log'
        if not level:
            file_handler.setLevel(self.level)
        else:
            file_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s %(filename)s [%(lineno)d] %(levelname)s %(message)s')
        formatter.datefmt = '%Y-%m-%d %H:%M:%S'
        file_handler.setFormatter(formatter)
        self.file_handler = file_handler
        self.addHandler(file_handler)

    def _set_stream_handler(self, level=None):
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        formatter.datefmt = '%Y-%m-%d %H:%M:%S'
        stream_handler.setFormatter(formatter)
        if not level:
            stream_handler.setLevel(self.level)
        else:
            stream_handler.setLevel(level)
        self.addHandler(stream_handler)
