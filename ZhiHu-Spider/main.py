# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     main
# Description:  
# CreateDate:   2021/12/25

import click

from setting import VERSION
from helper import start_answer_spider
from helper import start_article_spider


@click.group()
@click.version_option(version=VERSION)
def cli():
    pass


@cli.command(name='answer_spider')
def answer_spider():
    question_id = input("输入要采集的问题ID：")
    start_answer_spider(question_id)


@cli.command(name='article_spider')
def article_spider():
    article_id = input("输入要采集的文章ID：")
    start_article_spider(article_id)


if __name__ == '__main__':
    cli()
