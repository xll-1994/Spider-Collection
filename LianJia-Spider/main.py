# -*- coding: utf-8 -*-
# ProjectName:  LianJiaZuFangSpider
# FileName:     main
# Description:  
# CreateDate:   2021/12/11

from spiders.rent_spider import RentSpider

# 项目将获取链家网的以下信息
# 城市编号 city_id          城市名称 city_name
# 区县名称 district_name    区县缩写 district_letters
# 商圈名称 biz_circle_name  商圈缩写 biz_circle_letters
# 租赁编号 house_code       租赁名称 house_title

if __name__ == '__main__':
    rent_spider = RentSpider()
    city = rent_spider.get_city()
    if city:
        for city_name, city_url in city.items():
            if city_name == "杭州":
                city_id = rent_spider.get_city_id(city_url)
                district = rent_spider.get_district(url=city_url, city_id=city_id)
                if district:
                    for district_name, district_letters in district.items():
                        district_url = city_url + 'zufang/' + district_letters
                        biz_circle = rent_spider.get_biz_circle(url=district_url, city_id=city_id)
                        if biz_circle:
                            for biz_circle_name, biz_circle_letters in biz_circle.items():
                                if True:
                                    print("准备获取{}-{}-{}的出租数据".format(city_name, district_name, biz_circle_name))
                                    rent_spider.get_data(city_id=city_id,
                                                         city_name=city_name,
                                                         district_letters=district_letters,
                                                         district_name=district_name,
                                                         biz_circle_letters=biz_circle_letters,
                                                         biz_circle_name=biz_circle_name
                                                         )
                else:
                    new_url = city_url + 'zufang'
                    biz_circle = rent_spider.get_biz_circle(url=new_url, city_id=city_id)
                    if biz_circle:
                        for biz_circle_name, biz_circle_letters in biz_circle.items():
                            if True:
                                print("准备获取{}-{}的出租数据".format(city_name, biz_circle_name))
                                rent_spider.get_data(city_id=city_id,
                                                     city_name=city_name,
                                                     biz_circle_letters=biz_circle_letters,
                                                     biz_circle_name=biz_circle_name
                                                     )
