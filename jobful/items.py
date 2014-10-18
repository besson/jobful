# -*- coding: utf-8 -*-
from scrapy.item import Item, Field


class Job(Item):
    title = Field()
    description = Field()
    company = Field()
    date = Field()