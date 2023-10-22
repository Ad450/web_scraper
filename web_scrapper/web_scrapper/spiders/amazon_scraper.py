
from typing import Any
from scrapy import Spider
from scrapy.http import  Response
# from web_scrapper.items import WebScrapperItem

class AmazonScraper(Spider):
    name:str = "amazon_scraper"
    start_urls = ["https://www.amazon.com/s?k=amazon+shopping+online+website&adgrpid=152753934915&hvadid=673397238237&hvdev=c&hvlocphy=9070372&hvnetw=g&hvqmt=b&hvrand=9675813140351476259&hvtargid=kwd-1283712009298&hydadcr=22394_13507777&tag=hydglogoo-20&ref=pd_sl_42mumgtcax_b"]

    def parse(self, response: Response,**kwargs: Any)-> None:
        category_selector = response.css("div.puis-card-container")
        for category in category_selector:
            image_url = category.css("a.a-link-normal::attr(href)").get()
            description = category.css("span.a-size-base-plus::text").get()
            rating = category.css("span.a-icon-alt::text").get()
            price = category.css("span.a-price span.a-offscreen::text").get()
            save_percentage = category.css("span.a-color.base::text").get()

            yield {
                "img_src":image_url,
                "description":description,
                "rating":rating,
                "price":price,
                "save_percentage":save_percentage
            }
        print(len(category_selector))


