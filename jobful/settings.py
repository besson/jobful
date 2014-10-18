# -*- coding: utf-8 -*-

BOT_NAME = 'ajobful'

SPIDER_MODULES = ['jobful.spiders']
NEWSPIDER_MODULE = 'jobful.spiders'
ITEM_PIPELINES = ['jobful.pipelines.MongoPipeline']
