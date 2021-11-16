from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from data_img.spiders.leroymerlin import LeroymerlinSpider
from data_img import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinSpider, query='плитка')
    process.start()
