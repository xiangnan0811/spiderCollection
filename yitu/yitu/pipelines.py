# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class YituPipeline(object):
    def process_item(self, item, spider):
        return item


class SaveImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # 下载图片，如果传过来的是集合需要循环下载
        # meta里面的数据是从spider获取，然后通过meta传递给下面方法：file_path
        yield scrapy.Request(
            url=item['url'],
            meta={'name': item['title']},
            headers={
                'Referer': item['original_url'],
            },
        )

    def item_completed(self, results, item, info):
        # 是一个元组，第一个元素是布尔值表示是否成功
        if not results[0][0]:
            raise DropItem('下载失败')
        return item

    # 重命名，若不重写这函数，图片名为哈希，就是一串乱七八糟的名字
    def file_path(self, request, response=None, info=None):
        # 接收上面meta传递过来的图片名称
        name = request.meta['name']
        # 提取url前面名称作为图片名
        image_name = request.url.split('/')[-1]
        # 清洗Windows系统的文件夹非法字符，避免无法创建目录
        folder_strip = re.sub(r'[？\\*|“<>:/]', '', str(name))
        # 分文件夹存储的关键：{0}对应着name；{1}对应着image_guid
        filename = '{0}/{1}'.format(folder_strip, image_name)
        return filename