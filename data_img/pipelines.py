# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
<<<<<<< HEAD
import hashlib
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


def price_convert(value):
    try:
        value = [el for el in value if el.isdigit()]
        value = float(".".join(value))
    except Exception as ex:
        print(ex)
    finally:
        return value


class DataImgPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['leroymerlin']

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item['price'] = price_convert(item['price'])
        collection.update_one({'link': item['link']}, {'$set': item}, upsert=True)
        return item


class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as exc:
                    print(exc)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(bytes(request.url, encoding='utf8')).hexdigest()
        return f'{item["name"]}/{image_guid}.jpg'
=======
from itemadapter import ItemAdapter


class DataImgPipeline:
    def process_item(self, item, spider):
        print()
        return item
>>>>>>> lesson_7
