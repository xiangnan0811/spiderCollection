# -*- coding: utf-8 -*-

import scrapy


class YituItem(scrapy.Item):
    title = scrapy.Field()                    # 标题
    url = scrapy.Field()                      # 链接
    original_url = scrapy.Field()             # 原链接
