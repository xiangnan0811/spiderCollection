import scrapy


class NewHouseItem(scrapy.Item):
    """新房item."""
    _id = scrapy.Field()                               # ID
    province = scrapy.Field()                          # 省份
    city = scrapy.Field()                              # 城市
    name = scrapy.Field()                              # 小区名字
    price = scrapy.Field()                             # 价格
    house_type = scrapy.Field()                        # 房型
    area = scrapy.Field()                              # 面积
    address = scrapy.Field()                           # 地址
    district = scrapy.Field()                          # 行政区
    sale = scrapy.Field()                              # 是否在售
    origin_url = scrapy.Field()                        # 详情页链接
    gather_time = scrapy.Field()                       # 采集时间
    # update_time = scrapy.Field()                       # 入库时间


class ESFHouseItem(scrapy.Item):
    """二手房item."""
    _id = scrapy.Field()                               # ID
    province = scrapy.Field()                          # 省份
    city = scrapy.Field()                              # 城市
    name = scrapy.Field()                              # 小区名字
    intro_name = scrapy.Field()                        # 房名
    house_type = scrapy.Field()                        # 房型
    floor = scrapy.Field()                             # 楼层
    towards = scrapy.Field()                           # 朝向
    year = scrapy.Field()                              # 年代
    area = scrapy.Field()                              # 面积
    address = scrapy.Field()                           # 地址
    price = scrapy.Field()                             # 总价
    unit = scrapy.Field()                              # 单价
    origin_url = scrapy.Field()                        # 详情页链接
    gather_time = scrapy.Field()                       # 采集时间
    # update_time = scrapy.Field()                       # 入库时间
