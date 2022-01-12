# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     article_spider
# Description:  
# CreateDate:   2022/1/12

from datetime import datetime

from util import WebRequest
from util import SaveData
from itemparser import ArticleParser
from handler import LogHandler


class ArticleSpider:

    def __init__(self, article_id=None):
        self.article_id = article_id
        self.log = LogHandler("article_spider")

    def run(self):
        url = "https://zhuanlan.zhihu.com/p/" + str(self.article_id)
        html_content = WebRequest().get(url).tree
        article_detail = ArticleParser().get_detail(html_content)
        article_detail["article_id"] = self.article_id
        article_detail["insert_time"] = datetime.now()
        output = list()
        output.append(article_detail)
        SaveData(data=output, table_name='article', unique_id='article_id').run()
        self.log.info("文章数据已成功保存！")


if __name__ == "__main__":
    pass
