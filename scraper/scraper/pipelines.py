from itemadapter import ItemAdapter
import psycopg2
from scrapy.exceptions import DropItem

class PostgresPipeline:
    def open_spider(self, spider):
        self.connection = psycopg2.connect(
            host=spider.settings.get("POSTGRES_HOST"),
            port=spider.settings.get("POSTGRES_PORT"),
            dbname=spider.settings.get("POSTGRES_DBNAME"),
            user=spider.settings.get("POSTGRES_USER"),
            password=spider.settings.get("POSTGRES_PASSWORD"),
        )
        self.cursor = self.connection.cursor()
    
    def close_spider(self, spider):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        
    def process_item(self, item, spider):
        try:
              self.cursor.execute("""
                INSERT INTO products (name, store_id, price, url)
                VALUES (%s, %s, %s, %s)
            """, (
                item['name'], 
                item['store_id'], 
                float(item['price'].replace(",",".")), 
                item['url'], 
            ))
              self.connection.commit()
              return item
        except Exception as e:
            self.connection.rollback()
            spider.logger.error(f"Error al insertar en la BD: {e}")
            raise DropItem(f"Failed to insert item: {e}")


