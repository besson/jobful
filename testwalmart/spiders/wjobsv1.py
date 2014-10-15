from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

class DmozSpider(CrawlSpider): 
    name = "wjobs"
    allowed_domains = ["jobs.walmart.com"]
    #start_urls = ["http://jobs.walmart.com/searches.aspx?keyword=advanced+search&ISAdvanceSearch=True&ASCategory=ecommerce&ASPostedDate=-1&ASCountry=USA&ASState=-1&ASCity=-1&ASLocation=-1&ASCompanyName=-1&ASCustom1=-1&ASCustom2=-1&ASCustom3=-1&ASCustom4=-1&ASCustom5=-1&ASIsRadius=False&ASCityStateZipcode=-1&ASDistance=-1&ASLatitude=-1&ASLongitude=-1&ASDistanceType=-1&jobtitlekeyword=filter%20by%20job%20title&locationkeyword=filter%20by%20job%20location&dateKeyword=&categoryKeyword=&issearchpaging=True&isdate=True&pagenumber=1", "http://jobs.walmart.com/searches.aspx?keyword=advanced+search&ISAdvanceSearch=True&ASCategory=ecommerce&ASPostedDate=-1&ASCountry=USA&ASState=-1&ASCity=-1&ASLocation=-1&ASCompanyName=-1&ASCustom1=-1&ASCustom2=-1&ASCustom3=-1&ASCustom4=-1&ASCustom5=-1&ASIsRadius=False&ASCityStateZipcode=-1&ASDistance=-1&ASLatitude=-1&ASLongitude=-1&ASDistanceType=-1&jobtitlekeyword=filter%20by%20job%20title&locationkeyword=filter%20by%20job%20location&dateKeyword=&categoryKeyword=&issearchpaging=True&isdate=True&pagenumber=2"] 
    #curl
    start_urls = ["http://jobs.walmart.com/careers/it-&-software-development-jobs/job-list-1"]
    rules = [Rule(SgmlLinkExtractor(restrict_xpaths=('//td[@class="jobTitle"]')), follow=True),]
    def parse(self, response):
       for sel in response.xpath('//tr'):
          jobdesc = sel.xpath('//td[@class="jobTitle"]//text()').extract()
          jobdate = sel.xpath('//td[@class="location"]//text()').extract()
          jobplace = sel.xpath('//td[@class="date"]//text()').extract()
          meta = sel.xpath('//td[@class="jobTitle"]/a/@href').extract()
       #i = 0
       #while (i < len(jobdesc)):
       #    print jobdesc[i] + " " + meta[i]
       #    i = i + 1;
          
       
       for m in meta:
          yield Request("http://jobs.walmart.com" + m, callback = self.parse_link)
 
       

    def parse_link(self, response):
        sel = response.xpath('//span')

        fulljobdescription = sel.xpath('//span[@itemprop="description"]//text()').extract()
        print fulljobdescription
        print "**********\n"