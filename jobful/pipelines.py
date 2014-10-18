# -*- coding: utf-8 -*-
import pymongo


class MongoPipeline(object):

    def __init__(self):
        client = pymongo.MongoClient("localhost", 27017)
        db = client.jobful
        self._jobs = db.jobs

    def process_item(self, item, spider):
        d_item = dict(item)

        if (not self._jobs.find_one(d_item)):
            print "adding %s" % item["title"]
            self._jobs.save(d_item)

        return item
