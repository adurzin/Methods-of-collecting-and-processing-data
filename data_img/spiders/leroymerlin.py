import scrapy
from scrapy.http import HtmlResponse
from data_img.items import DataImgItem


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']

    def parse(self, response: HtmlResponse):
        # next_page = response.xpath()
        links = response.xpath("//a[@data-qa-product-name]")
        for link in links:
            yield response.follow(link, callback=self.good_parse)

    def good_parse(self, response: HtmlResponse):
        link = response.url
        name = response.xpath("//h1/text()").get()
        price = response.xpath("//uc-pdp-price-view[@slot='primary-price']/span/text()").getall()
        photos = response.xpath("//img[@alt='product image']/@data-origin").getall()
        yield DataImgItem(name=name, link=link, price=price, photos=photos)
