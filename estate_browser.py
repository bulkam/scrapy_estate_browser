import logging
import json
import scrapy
from scrapy.crawler import CrawlerRunner
from database import DB

from twisted.internet import reactor

class EstateSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page=500",
    ]
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
    }
    
    def parse(self, response):
        data = json.loads(response.body)["_embedded"]["estates"]
        db = DB("estates.db")
        db.create_table()
        for i, estate in enumerate(data):
            img_links = estate["_links"]["images"]
            link = "" if len(img_links) == 0 else img_links[0]["href"]
            db.insert_row((i, estate["name"], link))


def run():
    process = CrawlerRunner({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process.crawl(EstateSpider)
    d = process.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    process.start()

if __name__ == "__main__":
    run()