import scrapy
from scrapy.spiders import Spider
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from itemDataExtractSpider.items import ItemdataextractspiderItem
from modules import getQueries
from modules import start_logger

#define XPATH selectors here (for use in extracting data from webpages)
XPATH_NAME = '//title/text()'
XPATH_LINK = 'a/@href'

class itemCrawler(CrawlSpider):
	#use name to call spider in "scrapy crawl crwler"
	name = "crwler"
	
	#use query to find starting URLs from nextag.com
	query = getQueries.results()
	
	start_urls = []
	
	#get urls to start with from getQueries.py file
	for url in query.search_query():
		if(url):
	            start_urls.append(url)
	            
	#specify this rule so we can extract information from crawled websites
	rules = (Rule(SgmlLinkExtractor(), callback='parse', follow=False),)

	def parse(self,response):
        #instantiate item class from items.py earlier and 
        #assign values to each member of that class to be returned
		item = ItemdataextractspiderItem()
		item['product'] = response.selector.xpath(XPATH_NAME).extract()
		item['link'] = response.url
		return item