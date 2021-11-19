import scrapy
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
import hashlib


class InstparsePipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['instagram']

    def process_item(self, item, spider):
        collection = self.mongo_base[item['account']]
        collection.update_one({'user_id': item['user_id'], 'user_type': item['user_type']}, {'$set': item}, upsert=True)
        return item


class UserPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            try:
                return scrapy.Request(item['photo'])
            except Exception as e:
                print(e)

    def item_completed(self, results, item, info):
        item['photo'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(bytes(request.url, encoding='utf8')).hexdigest()
        return f'{item["account"]}/{item["user_type"]}/{item["username"]}/{image_guid}.jpg'
