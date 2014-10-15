# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TestwalmartItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	jobdesc = scrapy.Field() 
	jobdate = scrapy.Field() 
	jobplace = scrapy.Field()

class JobDescription(scrapy.Item)
	fulljobdescription = scrapy.Field()