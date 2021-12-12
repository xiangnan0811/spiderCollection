# -*- coding: utf-8 -*-
import re
import scrapy
from yitu.items import YituItem


class YtSpider(scrapy.Spider):
    name = 'yt'
    allowed_domains = ['www.yeitu.net']
    start_urls = ['https://www.yeitu.net/meinv/']

    def parse(self, response):
        category = response.xpath('//div[@class="column-list"]/ul/li/a/@href').extract()
        for url in category:
            yield scrapy.Request(url=url, callback=self.parse_album)

    def parse_album(self, response):
        next_pages = response.xpath('//a[@class="a1"]/@href').extract()[1]
        current_page = int(response.xpath('//div[@id="pages"]/span/text()').extract_first())
        next_page = int(re.findall(r'/(\d+).html', next_pages)[0])
        if next_page > current_page:
            next_url = response.urljoin(next_pages)
            yield scrapy.Request(url=next_url, callback=self.parse_album)

        links = response.xpath('//div[@class="list-box"]/ul/li/a/@href').extract()
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_img)

    def parse_img(self, response):
        next_pages = response.xpath('//div[@id="pages"]/a[last()]/@href').extract_first()
        current_page = int(response.xpath('//div[@id="pages"]/span/text()').extract_first())
        next_page = int(re.findall(r'/\d+_\d+_(\d+).html', next_pages)[0])
        if next_page > current_page:
            yield scrapy.Request(next_pages, callback=self.parse_img)

        item = YituItem()
        item['title'] = response.xpath('//h1/text()').extract_first()
        item['url'] = response.xpath('//div[@class="img_box"]/a/img/@src').extract_first()
        item['original_url'] = response.url

        yield item
