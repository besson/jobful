from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from jobful.items import Job
from datetime import date


class FacebookJobsSpider(CrawlSpider):
    name = "fb-jobs"
    allowed_domains = ["facebook.com"]

    prefix = "https://www.facebook.com/careers/search?q=&location"
    _file = "spiders/facebook/us-locations.txt"

    start_urls = ["%s=%s" % (prefix, loc.strip()) for loc in open(_file).readlines()]

    def parse(self, response):
        partial_urls = Selector(response).xpath("//a[contains(@href, '/department')]/@href").extract()

        for url in partial_urls:
            yield Request("https://www.facebook.com" + url, callback=self.parse_link)

    def parse_link(self, response):
        sel = Selector(response)
        job = Job()

        job["title"] = sel.xpath("//h3[contains(@class,'mvs careersSubPageSubTitle')]//text()").extract()
        job["location"] = sel.xpath("//div[contains(@class, 'mf')]//text()")[0].extract()
        job["description"] = sel.xpath("//ul[contains(@class,'uiList mts')]//li//text()").extract()
        job["company"] = "facebook"
        job["url"] = response.url
        job["updated_at"] = date.today().isoformat()

        return job