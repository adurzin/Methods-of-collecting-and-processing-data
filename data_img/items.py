# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
<<<<<<< HEAD
from itemloaders.processors import MapCompose, TakeFirst


class DataImgItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    _id = scrapy.Field()
=======


class DataImgItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    photos = scrapy.Field()
    _id = scrapy.Field()
    pass
>>>>>>> lesson_7
