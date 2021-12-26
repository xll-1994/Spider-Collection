# -*- coding: utf-8 -*-
# ProjectName:  LianJiaZuFangSpider
# FileName:     model_spider
# Description:  
# CreateDate:   2021/12/11

import random
from config import constants as base


class ModelSpider(object):

    def _random_headers(self):
        headers = {
            "User-Agent": random.choice(base.USER_AGENT_POOL)
        }
        return headers
