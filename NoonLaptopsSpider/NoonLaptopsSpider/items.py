# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NoonlaptopsspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LaptopsItem(scrapy.Item):
    brand = scrapy.Field()
    product_name = scrapy.Field()
    model_number = scrapy.Field()
    # rating = scrapy.Field()
    # stock = scrapy.Field()
    was_price = scrapy.Field()
    now_price = scrapy.Field()
    saving = scrapy.Field()