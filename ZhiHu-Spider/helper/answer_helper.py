# -*- coding: utf-8 -*-
# ProjectName:  ZhiHu-Spider
# FileName:     answer_helper
# Description:  
# CreateDate:   2021/12/25

import json


class AnswerHelper(object):

    def __init__(self, answer_id='', user_id='', question_id=''):
        self._answer_id = answer_id
        self._user_id = user_id
        self._question_id = question_id

    @classmethod
    def create_from_json(cls, obj_json):
        _dict = json.loads(obj_json)
        return cls(
            answer_id=_dict.get('answer_id', ''),
            user_id=_dict.get('user_id', ''),
            question_id=_dict.get('question_id', '')
        )

    @property
    def answer_id(self):
        return self._answer_id

    @property
    def to_dict(self):
        return {
            'answer_id': self._answer_id,
            'user_id': self._user_id,
            'question_id': self._question_id
        }

    @property
    def to_json(self):
        return json.dumps(self.to_dict, ensure_ascii=False)
