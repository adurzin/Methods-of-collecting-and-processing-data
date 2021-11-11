import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Br%5D%5B0%5D=3',
                  'https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Br%5D%5B0%5D=4',
                  'https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Br%5D%5B0%5D=5',
                  'https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Br%5D%5B0%5D=2',
                  'https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Br%5D%5B0%5D=6',
                  'https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Br%5D%5B0%5D=7',
                  'https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Br%5D%5B0%5D=8']

    def parse(self, response: HtmlResponse, **kwargs):
        next_page = response.xpath("//a[contains(@class, 'f-test-button-dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[contains(@class, 'icMQ_ _6AfZ9')]/@href").getall()
        for link in links:
            link = 'https://voronezh.superjob.ru' + link
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        _id = response.url[-6:-14:-1]
        name = response.xpath("//h1/text()").get()
        salary = response.xpath("//span[@class='_2Wp8I _185V- _1_rZy Ml4Nx']/text()").getall()
        url = response.url
        yield JobparserItem(_id=_id, name=name, salary=salary, url=url)
