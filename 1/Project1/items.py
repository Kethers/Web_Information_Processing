# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TeacherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name        = scrapy.Field()    # 姓名
    position    = scrapy.Field()    # 职位
    phone       = scrapy.Field()    # 电话
    email       = scrapy.Field()    # 邮箱
    fax         = scrapy.Field()    # 传真
    research    = scrapy.Field()    # 研究方向
    # profile     = scrapy.Field()    # 个人介绍
    # education   = scrapy.Field()    # 教育经历
    # employment  = scrapy.Field()    # 工作经历
    
    pass
