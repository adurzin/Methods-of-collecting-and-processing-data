from itemadapter import ItemAdapter
from pymongo import MongoClient


class InstparsePipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['instagram']

    def process_item(self, item, spider):
        collection = self.mongo_base[item['user_type']]
        collection.update_one({'_id': item['_id']}, {'$set': item}, upsert=True)
        return item
