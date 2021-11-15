import scrapy
from scrapy.http import HtmlResponse
from data_img.items import DataImgItem
<<<<<<< HEAD
from scrapy.loader import ItemLoader
=======
>>>>>>> lesson_7


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']

    def parse(self, response: HtmlResponse):
<<<<<<< HEAD
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
=======

>>>>>>> lesson_7
        links = response.xpath("//a[@data-qa-product-name]")
        for link in links:
            yield response.follow(link, callback=self.good_parse)

    def good_parse(self, response: HtmlResponse):
<<<<<<< HEAD
        loader = ItemLoader(item=DataImgItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//uc-pdp-price-view[@slot='primary-price']/span/text()")
        loader.add_xpath("photos", "//img[@alt='product image']/@data-origin")
        loader.add_value("link", response.url)
        yield loader.load_item()
=======
        link = response.url
        name = response.xpath("//h1/text()").get()
        price = response.xpath("//uc-pdp-price-view[@slot='primary-price']/span/text()").getall()
        photos = response.xpath("//img[@alt='product image']/@data-origin").getall()
        yield DataImgItem(name=name, link=link, price=price, photos=photos)
>>>>>>> lesson_7
