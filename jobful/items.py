# -*- coding: utf-8 -*-
from scrapy.item import Item, Field


class Job(Item):
    title = Field()
    description = Field()
    company = Field()
    location = Field()
    qualifications = Field()
    url = Field()
    updated_at = Field()