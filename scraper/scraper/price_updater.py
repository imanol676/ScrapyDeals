import scrapy
import psycopg2
#import schedule
import time
from settings import POSTGRES_DBNAME,POSTGRES_USER,POSTGRES_PORT,POSTGRES_PASSWORD,POSTGRES_HOST




def connect_db():
    return psycopg2.connect(
       dbname = POSTGRES_DBNAME,
       user = POSTGRES_USER,
       host = POSTGRES_HOST,
       port = POSTGRES_PORT,
       password = POSTGRES_PASSWORD
    )
       

def update_prices():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, url, price, store_id FROM products")
    
    productos = cursor.fetchall()
    
    for producto in productos:
        id_producto,url,precio_actual,store_id = producto
        nuevo_precio = None
        
        print(f"verificando el producto: {id_producto} ({url})")
        
        #que tienda scrapear
        if store_id == 1:
            nuevo_precio,disponible = scrap_ml(url)   
        elif store_id == 2:
            nuevo_precio,disponible = scrap_ebay(url)
      
        if nuevo_precio and nuevo_precio != precio_actual:
            print(f"precio actualizado para: {id_producto} el precio cambió de: {precio_actual} => {nuevo_precio}")
            cursor.execute("UPDATE products SET price = %s WHERE id = %s", (nuevo_precio, id_producto))
        else:
             print(f"Precio sin cambios para {id_producto}")
            
    
    conn.commit()
    cursor.close()
    conn.close()
    

#Scrapear las paginas para actualizar los precios

def scrap_ml(url):
    try:
        response = scrapy.request(url)
        precio = response.css(".andes-money-amount__fraction::text").get()
        
        if precio:
            return float(precio.replace(".", "").replace(",", ".")), True
        
        return None,False
    except Exception:
        return None,False
    
    
def scrap_ebay(url):
    try:
        response = scrapy.request(url)
        precio = response.css(".x-price-primary::text").get()
        
        if precio:
            return float(precio.replace(",", "").replace("$", "").strip()), True
        
        return None,False
    except Exception:
        return None,False
    


# para cada 6 horas se ejectua la actualización
#schedule.every(6).hours.do(update_prices)

if __name__ == "__main__":
   update_prices()
        
    
        
    