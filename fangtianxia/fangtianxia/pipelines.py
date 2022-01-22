import pymongo


class FangtianxiaPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    """MongoDB管道."""
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.__class__.__name__
        data = dict(item)
        self.db[name].update_one({"_id": data['_id']}, {"$set": data}, upsert=True)
        return item

    def close_spider(self, spider):
        self.client.close()
