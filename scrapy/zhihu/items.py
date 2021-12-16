# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class Question(Item):
    question_id = Field()
    url = Field()
    title = Field()
    brief_intro = Field()
    follower_num = Field()
    view_num = Field()
    answer_num = Field()
    comment_num = Field()
    vote_up_num = Field()
    tag = Field()
    related = Field()
    cookies = Field()
    proxy = Field()
    insert_time = Field()


class User(Item):
    user_id = Field()
    user_token = Field()
    homepage = Field()
    nickname = Field()
    gender = Field()
    brief_intro = Field()
    type = Field()
    description = Field()
    industry = Field()
    school = Field()
    major = Field()
    following_num = Field()
    follower_num = Field()
    answer_num = Field()
    video_num = Field()
    ask_num = Field()
    article_num = Field()
    column_num = Field()
    idea_num = Field()
    collection_num = Field()
    following_topic_num = Field()
    following_ask_num = Field()
    following_column_num = Field()
    following_collection_num = Field()
    authentication = Field()
    location = Field()
    like_num = Field()
    vote_up_num = Field()
    collect_num = Field()
    log_num = Field()
    live_num = Field()
    insert_time = Field()


class Topic(Item):
    topic_id = Field()
    title = Field()
    url = Field()
    brief_intro = Field()
    follower_num = Field()
    question_num = Field()
    insert_time = Field()


class Answer(Item):
    question_id = Field()
    question_title = Field()
    answer_id = Field()
    answer_name = Field()
    user_homepage = Field()
    answer_content = Field()
    vote_up_num = Field()
    comment_num = Field()
    answer_time = Field()
    insert_time = Field()
