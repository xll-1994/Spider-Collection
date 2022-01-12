# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     launch_helper
# Description:  
# CreateDate:   2021/12/25


def start_answer_spider(question_id):
    from spider.answer_spider import AnswerSpider
    AnswerSpider(question_id).run()


def start_article_spider(article_id):
    from spider.article_spider import ArticleSpider
    ArticleSpider(article_id).run()
