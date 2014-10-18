# -*- coding: utf-8 -*-
from utils.mongo_connector import get_db


class MongoPipeline(object):

    def __init__(self):
        db = get_db()
        self._jobs = db.jobs

    def process_item(self, item, spider):
        d_item = dict(item)

        if (not self._jobs.find_one(d_item)):
            self._jobs.save(d_item)

        return item
