import scrapy
from scraper.items import ScrapyDealsItem
import re

class EbaySpider(scrapy.Spider):
    name = "ebay_spider"
    allowed_domains = ["ebay.com"]
    search_terms = [
    "iphones","macbook","mac","celulares alta gama"
]
    start_urls = [f"https://www.ebay.com/sch/i.html?_nkw={term.replace(' ', '+')}" for term in search_terms]
    
   
    
    def parse(self, response):
        for product in response.xpath('//li[contains(@class, "s-item")]'):
            item = ScrapyDealsItem()
            item['name'] = product.xpath('.//div[contains(@class, "s-item__title")]/span/text()').get()
            price_text = product.xpath('.//span[contains(@class, "s-item__price")]/text()').get()
            if price_text:
                price_cleaned = re.sub(r'[^\d.]', '', price_text)
                item['price'] = float(price_cleaned) if price_cleaned else None
            else:
                item['price'] = None
            item['price'] = str(item['price']) if item['price'] else None
            item['store_id'] = 2
            item['url'] = product.xpath('.//a[contains(@class, "s-item__link")]/@href').get()
            yield item
            
        # Paginación: Extraer la URL de la siguiente página
        next_page = response.xpath('//a[contains(@class, "pagination__next")]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)
