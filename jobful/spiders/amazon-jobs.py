from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from jobful.items import Job
from datetime import date
import urllib
import ijson


class AmazonJobsSpider(CrawlSpider):
    name = "amazon-jobs"
    allowed_domains = ["amazon.jobs"]
    start_urls = ["http://www.amazon.jobs"]

    def parse(self, response):
        f = urllib.urlopen(open("spiders/amazon/query.txt").read())
        parser = ijson.parse(f)

        for prefix, event, value in parser:
            if prefix == "jobs.item.url":
                yield Request("http://www.amazon.jobs%s" % value, callback=self.parse_link)

    def parse_link(self, response):
        sel = Selector(response)
        job = Job()

        job["title"] = sel.xpath("//h1[@class='job-title']//text()")[0].extract()
        job["location"] = sel.xpath("//p//text()").re(r'\w{2}, \w{2}, \w*')[0]
        job["description"] = sel.xpath("//p//text()").re('\xb7.*')
        job["company"] = "amazon"
        job["url"] = response.url
        job["updated_at"] = date.today().isoformat()

        return job