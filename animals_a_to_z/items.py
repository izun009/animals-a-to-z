# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AnimalsAToZItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    facts = scrapy.Field()
    facts_desc = scrapy.Field()
    fact = scrapy.Field()
    desc = scrapy.Field()
    # image_urls = scrapy.Field()
    # images = scrapy.Field()
