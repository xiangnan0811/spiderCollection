import re
from datetime import datetime

import scrapy
from fangtianxia.items import NewHouseItem, ESFHouseItem


class FtxSpider(scrapy.Spider):
    name = 'ftx'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        """从官网下的所有城市入手，获取各城市url，并构建各城市新房和二手房链接."""
        trs = response.xpath('//div[@class="outCont"]//tr')[:-1]  # 过滤掉海外城市
        province = None
        for tr in trs:
            tds = tr.xpath('.//td[not(@class)]')
            # 获取省份并装入meta传入下一个函数
            province_text = re.sub(r'\s', '', tds[0].xpath('.//text()').get())
            # 某省城市多的话第二行没有省份信息，故而使用上一次的省份信息
            if province_text:
                province = province_text
            # 获取城市信息
            city_links = tds[1].xpath('.//a')
            for city_link in city_links:
                city = city_link.xpath('.//text()').get()
                city_url = city_link.xpath('.//@href').get()
                # 构建新房、二手房的url链接
                url_module = city_url.split('//')
                if 'bj.' in url_module[1]:
                    newhouse_url = 'https://newhouse.fang.com/house/s/'
                    esf_url = 'https://esf.fang.com/'
                else:
                    url_city = url_module[1].split('.')[0]
                    newhouse_url = 'https://' + url_city + '.newhouse.fang.com/house/s/'
                    esf_url = 'https://' + url_city + '.esf.fang.com'
                # 新房链接
                yield scrapy.Request(url=newhouse_url, callback=self.parse_newhouse, meta={'info': (province, city)}, dont_filter=True)
                # 二手房链接
                yield scrapy.Request(url=esf_url, callback=self.parse_esf, meta={'info': (province, city)}, dont_filter=True)

    def parse_newhouse(self, response):
        """新房列表解析函数."""
        # 实例化新房item
        item = NewHouseItem()
        # 获取上一步得到的省份和城市信息
        item['province'], item['city'] = response.meta.get('info')
        lis = response.xpath('//div[contains(@class,"nl_con")]/ul/li[contains(@id,"lp_")]')
        for li in lis:
            # 商品ID
            item['_id'] = int(li.xpath('./@id').get().replace("lp_", ""))
            # 小区名称
            item['name'] = li.xpath('.//div[@class="nlcd_name"]/a/text()').get().strip()
            # 户型，去除特殊字符、空白符，并转换为字符串
            item['house_type'] = ','.join(list(filter(lambda x: re.match(r'\d', x), li.xpath(
                './/div[contains(@class,"house_type")]/a/text()').getall())))
            # 新房面积，同样去除一些特殊字符
            item['area'] = re.sub(r'[－/]', '', ''.join(li.xpath('.//div[contains(@class,"house_type")]/text()').getall())).strip().replace("㎡", "").replace("平米", "")
            # 详细地址
            item['address'] = li.xpath('.//div[@class="address"]/a/@title').get()
            # 行政区
            district = re.search(r'.*\[(.+)\].*', ''.join(li.xpath('.//div[@class="address"]/a//text()').getall()))
            if district:
                item['district'] = district.group(1)
            # 是否在售
            item['sale'] = li.xpath('.//div[contains(@class,"fangyuan")]/span/text()').get()
            # 详情页链接
            item['origin_url'] = response.urljoin(li.xpath('.//div[@class="nlcd_name"]/a/@href').get())
            # 价格
            item['price'] = re.sub(r'\s|广告', '', ''.join(li.xpath('.//div[@class="nhouse_price"]//text()').getall())).strip()
            # 采集时间
            item['gather_time'] = datetime.now()

            # yield item
            print(item)

        # 自动获取下一页
        next_page = response.xpath('//div[@class="page"]//a[@class="next"]/@href').get()
        if next_page:
            next_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_url, callback=self.parse_newhouse, meta={'info': (item['province'], item['city'])})

    def parse_esf(self, response):
        """二手房网页解析函数."""
        # 实例化二手房item
        item = ESFHouseItem()
        # 获取上一步得到的省份和城市信息
        item['province'], item['city'] = response.meta.get('info')
        dls = response.xpath('//div[contains(@class,"shop_list")]/dl[@dataflag="bg"]')
        for dl in dls:
            href = dl.xpath('.//dd/h4/a/@href').get()
            # 商品ID
            item['_id'] = int(href.split('_')[-1].split('.')[0])
            # 介绍名，就是那一行唬人的一长串
            item['intro_name'] = dl.xpath('.//dd/h4/a/span/text()').get().strip()
            # 小区名称
            item['name'] = dl.xpath('.//dd/p[@class="add_shop"]/a/text()').get().strip()
            # 详情页链接
            item['origin_url'] = response.urljoin(href)
            # 获取房屋信息
            house_infos = re.sub(r'[\s]', '', ''.join(dl.xpath('.//dd/p[@class="tel_shop"]//text()').getall())).split('|')
            for house_info in house_infos:
                # 户型
                if '室' in house_info:
                    item['house_type'] = house_info
                # 面积
                elif '㎡' in house_info:
                    item['area'] = float(house_info.replace("㎡", ""))
                # 香港澳门面积
                elif '呎' in house_info:
                    item['area'] = house_info
                # 楼层
                elif '层' in house_info:
                    item['floor'] = house_info
                # 朝向
                elif '向' in house_info:
                    item['towards'] = house_info
                # 建造时间
                elif '年建' in house_info:
                    item['year'] = int(house_info[:-2])
            # 详细地址
            item['address'] = dl.xpath('.//dd/p[@class="add_shop"]/span/text()').get()
            # 总价
            price = ''.join(dl.xpath('.//dd[@class="price_right"]/span[1]//text()').getall()).strip()
            if '$' in price:  # 港澳价格
                item['price'] = price
            else:             # 国内价格
                item['price'] = float(price.replace("万", "").replace("$", ""))

            # 单价
            unit = dl.xpath('.//dd[@class="price_right"]/span[2]/text()').get().strip()
            if '$' in unit:  # 港澳价格
                item['unit'] = unit
            else:             # 国内价格
                item['unit'] = float(unit.replace("元/㎡", "").replace("$", ""))
            # 采集时间
            item['gather_time'] = datetime.now()

            # yield item
            print(item)

        # 自动获取下一页
        next_page = response.xpath('//div[@class="page_al"]/p[last()-2]')
        next_text = next_page.xpath('.//a/text()').get()
        if next_text and next_text == '下一页':
            next_url = response.urljoin(next_page.xpath('.//a/@href').get())
            yield scrapy.Request(url=next_url, callback=self.parse_esf, meta={'info': (item['province'], item['city'])})
