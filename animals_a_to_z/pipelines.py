# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# import scrapy, os, environ
# from itemadapter import ItemAdapter
# from scrapy.pipelines.images import ImagesPipeline

# env = environ.Env()
# environ.Env.read_env('./.env')


# class AnimalsAToZPipeline(ImagesPipeline):
#     def set_filename(self, response):
#         new_name = response.meta['name'].replace("/", "-")
#         return f"full/{new_name}.jpg"

#     def get_media_requests(self, item, info):
#         for image_url in item['image_urls']:
#             yield scrapy.Request(image_url, meta={'name': item['name']})


#     def get_images(self, response, request, info, *, item=None):
#         for newfilename, image, newname in super(AnimalsAToZPipeline, self).get_images(response, request, info):
#             newfilename = self.set_filename(response)
#         yield newfilename, image, newname

#============================ Pake SQLite ==============================#
# class Sqlite3Pipeline(object):
#     def __init__(self):
#         # On going tambah deskripsi, image, image_urls
#         self.conn = sqlite3.connect('animals.db')
#         self.cursor = self.conn.cursor()
#         self.cursor.execute('''
#             CREATE TABLE IF NOT EXISTS animals (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT,
#                 facts TEXT,
#             )
#         ''')

#     def process_item(self, item, spider):
#         # On going tambah deskripsi, image, image_urls
#         self.cursor.execute("""
#             INSERT INTO animals (name, facts)
#             VALUES (?, ?)
#         """, (item['name'], item['facts']))
#         self.conn.commit()
#         return item

#     def close_spider(self, spider):
#         self.cursor.close()
#         self.conn.close()

#============================ Pake MySQL ==============================#
# class MySqlPipeline:

#     def __init__(self):
#         self.conn = mysql.connector.connect(
#             host = os.environ.get("SQL_HOST"),
#             user = os.environ.get("SQL_USER"),
#             password = os.environ.get("SQL_PASSWORD"),
#             database = os.environ.get("SQL_DATABASE")
#         )

#         ## Create cursor, used to execute commands
#         self.cur = self.conn.cursor()
#         self.cur.execute("""
#         CREATE TABLE IF NOT EXISTS animals(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT,
#             facts TEXT
#         )
#         """)

#     def process_item(self, item, spider):
#         # On going tambah deskripsi, image, image_urls
#         self.cursor.execute("""
#             INSERT INTO animals (name, facts)
#             VALUES (?, ?)
#         """, (item['name'], item['facts']))
#         self.conn.commit()
#         return item
    
#     def close_spider(self, spider):
#         self.cur.close()
#         self.conn.close()