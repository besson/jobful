from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from jobful.items import Job
from datetime import date
from google.position_url_extractor import get_urls_from
import time


class GoogleJobsSpider(CrawlSpider):
    name = "google-jobs"
    allowed_domains = ["google.com"]
    start_urls = ["https://www.google.com/about/careers"]

    def parse(self, response):
        page_prefix = "https://www.google.com/about/careers/search#t=sq&q=j&li=10&st"
        pages = ["%s=%d" % (page_prefix, i*10) for i in range(0, 100)]

        for page in pages:
            urls = get_urls_from(page)
            print urls

            for url in urls:
                yield Request(url, meta = {'dont_redirect': True, 'handle_httpstatus_list': [301,302], 'dont_merge_cookies': True}, callback=self.parse_link)
                time.sleep(5)

    def parse_link(self, response):
        sel = Selector(response)
        job = Job()

        job["title"] = sel.xpath('//span[@itemprop="name"]//text()')[0].extract()
        job["description"] = sel.xpath('//div[@class="detail-item"]//text()').extract()
        job["location"] = sel.xpath('//div[@class="info-text"]//text()')[0].extract()
        job["company"] = "google.com"
        job["url"] = response.url
        job["updated_at"] = date.today().isoformat()

        return job