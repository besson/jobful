import scrapy

class DmozSpider(scrapy.Spider): 
    name = "wjobs"
    allowed_domains = ["jobs.walmart.com"]
    #start_urls = ["http://jobs.walmart.com/searches.aspx?keyword=advanced+search&ISAdvanceSearch=True&ASCategory=ecommerce&ASPostedDate=-1&ASCountry=USA&ASState=-1&ASCity=-1&ASLocation=-1&ASCompanyName=-1&ASCustom1=-1&ASCustom2=-1&ASCustom3=-1&ASCustom4=-1&ASCustom5=-1&ASIsRadius=False&ASCityStateZipcode=-1&ASDistance=-1&ASLatitude=-1&ASLongitude=-1&ASDistanceType=-1&jobtitlekeyword=filter%20by%20job%20title&locationkeyword=filter%20by%20job%20location&dateKeyword=&categoryKeyword=&issearchpaging=True&isdate=True&pagenumber=1", "http://jobs.walmart.com/searches.aspx?keyword=advanced+search&ISAdvanceSearch=True&ASCategory=ecommerce&ASPostedDate=-1&ASCountry=USA&ASState=-1&ASCity=-1&ASLocation=-1&ASCompanyName=-1&ASCustom1=-1&ASCustom2=-1&ASCustom3=-1&ASCustom4=-1&ASCustom5=-1&ASIsRadius=False&ASCityStateZipcode=-1&ASDistance=-1&ASLatitude=-1&ASLongitude=-1&ASDistanceType=-1&jobtitlekeyword=filter%20by%20job%20title&locationkeyword=filter%20by%20job%20location&dateKeyword=&categoryKeyword=&issearchpaging=True&isdate=True&pagenumber=2"] 
    #curl
    start_urls = ["http://jobs.walmart.com/careers/it-&-software-development-jobs/job-list-1"]
    def parse(self, response):
       for sel in response.xpath('//tr'):
          jobdesc = sel.xpath('//td[@class="jobTitle"]//text()').extract()
          jobdate = sel.xpath('//td[@class="location"]//text()').extract()
          jobplace = sel.xpath('//td[@class="date"]//text()').extract()
       print jobdesc
       print jobdate
       print jobplace
          #response.xpath('//td[@class="td2"]').extract()