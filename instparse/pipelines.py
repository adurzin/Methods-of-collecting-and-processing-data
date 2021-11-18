from itemadapter import ItemAdapter
from pymongo import MongoClient


class InstparsePipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['instagram']

    def process_item(self, item, spider):
        collection = self.mongo_base[item['account']]
        collection.update_one({'user_id': item['user_id']}, {'$set': item}, upsert=True)
        return item
