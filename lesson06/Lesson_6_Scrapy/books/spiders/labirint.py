import scrapy
from scrapy.http import HtmlResponse
from books.items import BooksItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/best/sale/?page=1']

    def parse(self, response:HtmlResponse):
        links = response.xpath('//a[@class="product-title-link"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.book_parser)
        next_page = response.xpath('//a[@class="pagination-next__text"]/@href').get()
        if next_page:
            yield response.follow(next_page,callback=self.parse)
        pass

    def book_parser(self, response:HtmlResponse):
        b_link = response.xpath('//meta[@property="og:url"]/@content').get()
        b_name = response.xpath('//meta[@property="og:title"]/@content').get()
        b_authors = response.xpath('//a[@data-event-label="author"]/text()').getall()
        b_base_price = int(response.xpath('//span[@class="buying-priceold-val-number"]/text()').get())
        b_sale_price = int(response.xpath('//span[@class="buying-pricenew-val-number"]/text()').get())
        b_rate = float(response.xpath('//div[@id="rate"]/text()').get())

        item = BooksItem(name=b_name,
                         link=b_link,
                         authors=b_authors,
                         base_price=b_base_price,
                         sale_price=b_sale_price,
                         rate=b_rate,
                         _id=b_link)

        yield item
        pass


