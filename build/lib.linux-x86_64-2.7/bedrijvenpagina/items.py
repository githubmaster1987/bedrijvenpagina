# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BedrijvenpaginaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    postal_code = scrapy.Field()
    city = scrapy.Field()
    phoneno = scrapy.Field()
    email = scrapy.Field()
    kvk = scrapy.Field()
    website = scrapy.Field()
    url = scrapy.Field()
    sub_url = scrapy.Field()
