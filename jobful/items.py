# -*- coding: utf-8 -*-
from scrapy.item import Item, Field


class TestwalmartItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    jobdesc = Field()
    jobdate = Field()
    jobplace = Field()


class Job(Item):
    title = Field()
    description = Field()