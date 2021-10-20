import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from leroymerlin.items import LeroymerlinItem
from itemloaders.processors import TakeFirst, MapCompose, Join, Compose



class LmerlinSpider(scrapy.Spider):
    name = 'lmerlin'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/snegouborochnye-mashiny/']

    def parse(self, response:HtmlResponse):
        products = response.xpath('//div[@class="phytpj4_plp largeCard"]/a/@href')
        for product in products:
            yield response.follow(product, callback=self.product_parser)
        next_page = response.xpath("//a[contains(@aria-label,'Следующая страница')]")
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        print(products)

    def product_parser(self, response:HtmlResponse):
        item = ItemLoader(item=LeroymerlinItem(),response=response)
        item.add_xpath('name', '//h1/text()')
        item.add_value('link', response.url)
        item.add_xpath('price', "//span[@slot='price']/text()")
        item.add_xpath('photos', "//img[@alt='product image']/@src")
        return item.load_item()
        print()
        pass
