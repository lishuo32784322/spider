# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    key, user_pic_url, user_name, gender, address, job, education, description =scrapy.Field(), scrapy.Field(),scrapy.Field(),scrapy.Field(),scrapy.Field(),scrapy.Field(),scrapy.Field(),scrapy.Field()
