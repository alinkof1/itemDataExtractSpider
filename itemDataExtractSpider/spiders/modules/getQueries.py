#getQueries.py
#queries a search result through http://www.nextag.com/'s search engine
#returns an object list of the top results' webpage links

#	python script load up search results
#	--parse through for links to product pages
#		---load up individual product, seller, rating
#	--resultscol element in html

from lxml import html
import requests
import re
import logging
import scrapy
import os
import start_logger

#Xpath Constants
XPATH_BASE = '//div[@class="searchList cursorPointer clickout"]'
XPATH_NAME = './/h2/text()'
XPATH_LINK = './/a[@class="bl stopPropagation"]/@href'


#Website Constants
#Specify which website to base requests from and browser emulator here
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
DOMAIN = 'http://www.nextag.com'
BASE_URL = "http://www.nextag.com/shopping/products?search="

#specify number of products crawled per item
NUM_PRODUCTS = 1

#select if logging is to be used
logger = start_logger.start_log()

class results(object):
	def __init__(self):
		self.products = []
		
		self.user_query = []
		self.all_queries = []
		
		#read file that contains the items to be searched through online marketplaces
		if __name__ == '__main__':
			cwd = os.getcwd() + "/reqs.txt"
		else:
			#use this if running as part of scrapy spider
			cwd = os.getcwd() + "/spiders/modules/reqs.txt"
			
		with open(cwd, 'r') as reqs:
			self.user_query = (reqs.read()).split('\n')
			
		#format each item query to replace whitespace with "+"s
		for w in (self.user_query):
			if (w):
				w = re.sub(r"\s+", '+', w)
				self.all_queries.append(w)
		print self.all_queries
		
	
	def search_query(self):
		product_names = ""
		product_links = ""
		
		for w in self.all_queries:
			if(w):
				#for each search on an online marketplace, append the specific search query
				req = BASE_URL
				req = req + (str(w))
				
				#send an HTML request to the webpage with the appended search query
				page = requests.get(req,headers=headers)
				
				#pull the html from the retrieved webpage
				tree = html.fromstring(page.content)
				
				#Iterate through the specified # of results per query
				for i in range(NUM_PRODUCTS):
					items = tree.xpath(XPATH_BASE)
					
					try:
						#iterate through each product result on amazon
						product_links = items[0].xpath(XPATH_LINK) #good?
						product_link = DOMAIN + str(product_links[0])
						if (product_link):
							self.products.append(product_link)
						logger.info('SUCCESS: product link sucessfully extracted:')
					except:
						#throw exception if error encountered in url search, but don't exit program
						logger.exception("ERR: ----exception occured----")
					finally:	
						product_links = ""
					
		return self.products
				
if __name__ == "__main__":
	amzn = results()
	print amzn.search_query()
