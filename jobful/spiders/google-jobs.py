from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from jobful.items import Job
from datetime import date
from selenium import webdriver
import time


class GoogleJobsSpider(CrawlSpider):
    name = "google-jobs"
    allowed_domains = ["google.com"]
    start_urls = ["https://www.google.com/about/careers"]

    def parse(self, response):
        driver = webdriver.PhantomJS()
        page_prefix = "https://www.google.com/about/careers/search#t=sq&q=j&li=10&st"
        pages = ["%s=%d" % (page_prefix, i*10) for i in range(0, 10)]

        for page in pages:
            driver.get(page)
            urls = driver.find_elements_by_xpath("//a[@itemprop='url']")

            for url in urls:
                clean_url = str(url.get_attribute("href")).replace("https", "http") 
                yield Request(clean_url, meta = {'dont_redirect': True, 'handle_httpstatus_list': [302]}, callback=self.parse_link)
                time.sleep(5)

        driver.quit()

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