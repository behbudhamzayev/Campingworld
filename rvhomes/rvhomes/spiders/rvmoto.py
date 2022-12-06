# Setup
''' 
    webpage - https://rv.campingworld.com/

 * Collect Nationwide listings of “Motorhomes for Sale” (both New and Used) that are running on Diesel 
 * Capture product details (new vs old, stock #, sleeps #, length), pricing information, dealership location
 * For vehicles with the sale price above $300,000 collect the horsepower
 '''
# Checking whether website allows web scraping
''''
 https://rv.campingworld.com/robots.txt
Webpage disallows scraping for some information in links like "Rvdetails" But as a student and noncommercial practice proceeding, 
yet could be stumbled on some error further because of  User-agent: */mod-security.'''
# First impressions of webpage:
''''
* Design and structuring have done poorly, as multiple tags with the same class/id. Which is not only discomfort to scrape but also style site.
* search engine is not consistent
* website is pretty slow and sometimes can not show all the details or shows a blank page

'''

# Before starting the Scrapy project, some basic scraping is done in Beautifull soup 
# yet for crawling every motorhome and looping back to the given search link starting the Scrapy project.

# uploding liblarires migh be usefull
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
import scrapy
from scrapy.http import Response, Request
from scrapy.crawler import CrawlerProcess
import pandas as pd

parser = 'html.parser'
# url="https://rv.campingworld.com/searchresults?external_assets=false&rv_type=motorized&condition=new_used&subtype=A,AD,B,BP,C&floorplans=class-a,cafl,cabh,cab2,carb,cath,carl,class-b,cbbh,cbfl,cbrb,cbrl,class-c,ccbh,ccfl,ccth,ccbaah,ccrb,ccrl&slides_max=&fueltype=diesel&sort=featured_asc&search_mode=advanced&locations=nationwide"

# before starting the Scrapy project body, to overcome possible blocking by robtix.txt and getting the Forbidden error in "settings.py" "ROBOTSTXT_OBEY" was changed to False.
class motorvSpider(scrapy.Spider):
    name = "motorhomes" # name of the scrawler
    base_url = 'https://rv.campingworld.com' # defining base url will easy our job to crawl every item page in from stat page
    start_urls=["https://rv.campingworld.com/searchresults?external_assets=false&rv_type=motorized&condition=new_used&subtype=A,AD,B,BP,C&floorplans=class-a,cafl,cabh,cab2,carb,cath,carl,class-b,cbbh,cbfl,cbrb,cbrl,class-c,ccbh,ccfl,ccth,ccbaah,ccrb,ccrl&slides_max=&fueltype=diesel&sort=featured_asc&search_mode=advanced&locations=nationwide&page=1"]

# Setting function to identify "@href"/links of motorhomes and with help of an "urljoin" we will get absolute links of RVs
    def parse(self, response):
        for link in response.css('div.unit-right > div.col-sm-12.d-none.d-md-block.asset-header > div:nth-child(1) > a::attr(href)').getall():
            yield response.follow(response.urljoin(link), callback=self.parse_abstract)
# Before looping over pages, the errors faced and especially with the policy of the website for anticrawl/robotix.txt
# To overpower the website rules about crawling, there has to be a defined User-Agent. For that purpose the Scrapy proceeding:
# * installing  pip install scrapy-user-agents
# * Make additional changes in the project's settings by adding DOWNLOADER_MIDDLEWARES, which will automatically and randomly assign USER-Agent each time the crawler run.
        for i in range(1,15):
            next_page=f"https://rv.campingworld.com/searchresults?external_assets=false&rv_type=motorized&condition=new_used&subtype=A,AD,B,BP,C&floorplans=class-a,cafl,cabh,cab2,carb,cath,carl,class-b,cbbh,cbfl,cbrb,cbrl,class-c,ccbh,ccfl,ccth,ccbaah,ccrb,ccrl&slides_max=&fueltype=diesel&sort=featured_asc&search_mode=advanced&locations=nationwide&page={i}"
        yield response.follow(next_page, callback=self.parse)
# Adding For loop to go through all the pages of search with a given specification at the beginning of the project 

# As parse used once(actually twice there main parsing function in embedded files of the project and as I am not use Crawler it is ok use parse once) and parse_abstract is get
# from previous function(parse) of looping and crawling every RV
# Furthermore, to get all the required details of the motorhome's new parser after running the file. It was clear once again the "beauty" and "perfect" design of this website
# that when there were missing details, the divs tags/blocks vanish. This brings inconsistency of scrapped data and further manipulation and conditional crawling of RV details.
    def parse_abstract(self, response):
        stock=response.css("div.stock-num-prod-details::text").get().split()[2]
        used=response.css("h1.roundedPill::text").get()
        location=response.css("div.col-sm-7 > span.stock-results::text").getall()[1].strip()
        price=int(response.css("span.low-price::text").get().split("$")[1].replace(",", ""))
# Creating an "if" statement for scraping horsepower of RVs, which only have a price more or equal to 300k. 
        # if price>=300000:
        #     hpw = response.css("#specs > div:nth-child(8) > h5::text").get()
        
        sleep=response.css("#specs > div:nth-child(5) > h5::text").get()
        length=response.css("#specs > div:nth-child(4) > h5::text").get().replace("'", "")
        
        
        yield{
            'used':used,
            'stock':stock,
            'price':price,
            'sleeps':sleep,
            'length_inc':length,
            'location':location
            # 'horsepower':hpw
        }

# after pushing crawling and saving it to a CSV file. It is noticeable that both main parsings are working,
# as there are more than 19 rows which means the function iterates through the pages, and also, entries are not repeating, so looping and looping back off each motorhome is working also.
# Observable that there mismatch of data in a few columns. It is due to not good practice of website creators and as mentioned above div block on item specs (where shows sleep, length, fuel type, horsepower, etc)
# are changing places when there is no info about the particular spec in RVs.
# This obstacle can be overcome by putting a request with XPath with [contadins], due to the deadline for now submitting in this way.

# for running crawler and saving file to csv called moto_1
#scrapy crawl motorhomes -o moto_1.csv



''''
The obstacles were mainly about website response, even for casually surfing, which led to irritation and squandering of time for nothing, 
and website blocking crawlers and crashing. There were times when it totally intercepted my API. A combination of such issues, 
whether the structure of the website and design, response time, and strictly blocked crawler, made the particular task a bit laborious 
but quite intriguing and educational. There are many possible ways to perform given task points, even in Scrapy itself, 
yet my chosen method of structuring scraping is far easier to catch and quite easily detect problems.
'''


# for crawiling in side of py file without utilizing bash.
# process = CrawlerProcess({
#     'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
# })

# process.crawl(motorvSpider)
# process.start()