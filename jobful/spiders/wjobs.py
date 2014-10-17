from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from jobful.items import Job


class DmozSpider(CrawlSpider):
    name = "wjobs"
    allowed_domains = ["jobs.walmart.com"]
    start_urls = ["http://jobs.walmart.com/careers/it-&-software-development-jobs/job-list-1"]

    def parse(self, response):
        for sel in Selector(response).xpath('//td[@class="jobTitle"]'):
            meta = sel.xpath('//td[@class="jobTitle"]/a/@href').extract()

        for m in meta:
            yield Request("http://jobs.walmart.com" + m, callback=self.parse_link)

    def parse_link(self, response):
        sel = Selector(response)
        job = Job()

        job["title"] = sel.xpath('//span[@itemprop="title"]//text()')[0].extract()
        job["description"] = sel.xpath('//span[@itemprop="description"]//ul//text()').extract()

        print job