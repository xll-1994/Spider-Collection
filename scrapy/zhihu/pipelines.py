# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging

from zhihu.database import CONNECTION
from zhihu.items import Question

cursor = CONNECTION.cursor()


class ZhiHuPipeline:

    def process_item(self, item, spider):
        try:
            if isinstance(item, Question):
                exist = self.get_question(item)
                if not exist:
                    self.save_question(item)
        except Exception as e:
            logging.warning(item)
            logging.error(e)
        return item

    @staticmethod
    def get_question(item):
        sql = 'SELECT question_id FROM question WHERE question_id=%s' % item['question_id']
        cursor.execute(sql)
        return cursor.fetchone()

    @staticmethod
    def save_question(item):
        keys = item.keys()
        values = tuple(item.values())
        fields = ','.join(keys)
        temp = ','.join(['%s'] * len(keys))
        sql = 'INSERT INTO question (%s) VALUES (%s)' % (fields, temp)
        cursor.execute(sql, values)
        return CONNECTION.commit()
