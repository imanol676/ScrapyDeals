import scrapy

class ScrapyDealsItem(scrapy.Item):
    name = scrapy.Field()
    store_id = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    
    
    