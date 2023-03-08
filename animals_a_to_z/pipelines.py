# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import scrapy, sqlite3, pymongo
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from animals_a_to_z.items import AnimalsAToZItem

import mysql.connector

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
#                 fact TEXT,
#                 desc TEXT,
#                 image_urls TEXT
#             )
#         ''')

#     def process_item(self, item, spider):
#         # On going tambah deskripsi, image, image_urls
#         self.cursor.execute("""
#             INSERT INTO animals (name, fact, desc, image_urls)
#             VALUES (?, ?)
#         """, (item['name'], item['fact'], item['desc'], item['image_urls']))
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
#             INSERT INTO animals (name, facts, fact, description, image_urls)
#             VALUES (?, ?, ?, ?)
#         """, (item['name'], item['facts'], item['fact'], item['description'], item['image_urls']))
#         self.conn.commit()
#         return item
    
#     def close_spider(self, spider):
#         self.cur.close()
#         self.conn.close()


# MYSQL===============
class MySqlPipeline(object):
    def __init__(self, mysql_user, mysql_password, mysql_host, mysql_db, mysql_port):
        self.mysql_user = mysql_user
        self.mysql_port = mysql_port
        self.mysql_password = mysql_password
        self.mysql_host = mysql_host
        self.mysql_db = mysql_db

    @classmethod
    def from_crawler(cls, crawler):
        mysql_user = crawler.settings.get('MYSQL_USER')
        mysql_password = crawler.settings.get('MYSQL_PASSWORD')
        mysql_host = crawler.settings.get('MYSQL_HOST')
        mysql_db = crawler.settings.get('MYSQL_DB')
        mysql_port = crawler.settings.get('MYSQL_PORT')

        return cls(mysql_user, mysql_password, mysql_host, mysql_db, mysql_port)

    def open_spider(self, spider):
        self.connection = mysql.connector.connect(
            user=self.mysql_user,
            password=self.mysql_password,
            host=self.mysql_host,
            database=self.mysql_db,
            port=self.mysql_port
        )
        self.cursor = self.connection.cursor()

        # Create table if doesnt exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS animals (
                id INT NOT NULL auto_increment, 
                name TEXT,
                image_urls TEXT,
                PRIMARY KEY (id)
            ) # end of sql
        """)
        self.connection.commit()


    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):

        try:
           

            self.cursor.execute("""
                INSERT INTO animals (name, image_urls)
                VALUES (%s, %s)
            """, (
                item['name'],
                str(item['image_urls'])
            ))
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise DropItem(f"Failed to insert item into MySQL database: {e}")
        return item


# class MongoPipeline(object):
#     collection_name = 'animals'

#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db

#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
#         )

#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]

#     def close_spider(self, spider):
#         self.client.close()

#     def process_item(self, item, spider):
#         self.db[self.collection_name].insert_one(dict(item))
#         return item