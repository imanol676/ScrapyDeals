import scrapy
from scraper.items import ScrapyDealsItem

class MpSpider(scrapy.Spider):
    name = "mp_spider"
    allowed_domains = ["mercadolibre.com.ar"]
    search_terms = ["playstation 5", "xbox series x", "nintendo switch", "smart tv"]
    start_urls = [
        "https://listado.mercadolibre.com.ar/{term}".format(term=term) for term in search_terms
    ]

    def parse(self, response):
        for product in response.xpath('//div[@class="ui-search-result__wrapper"]'):
            item = ScrapyDealsItem()
            item['name'] = product.xpath('.//a[@class="poly-component__title"]/text()').get()
            item['store_id'] = 1
            item['price'] = product.xpath('.//span[@class="andes-money-amount__fraction"]/text()').get()
            item['url'] = product.xpath('.//a[@class="poly-component__title"]/@href').get()
            yield item

        # Paginación: Extraer la URL de la siguiente página
        next_page = response.xpath('//li[@class="andes-pagination__button andes-pagination__button--next"]/a/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)
