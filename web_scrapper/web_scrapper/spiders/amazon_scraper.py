
from typing import Any, Dict, Iterable
from scrapy import Spider
from scrapy.http import  Response, Request
# from web_scrapper.items import WebScrapperItem

class AmazonScraper(Spider):
    name:str = "amazon_scraper"
    urls = ["https://www.amazon.com/s?k=amazon+shopping+online+website&adgrpid=152753934915&hvadid=673397238237&hvdev=c&hvlocphy=9070372&hvnetw=g&hvqmt=b&hvrand=9675813140351476259&hvtargid=kwd-1283712009298&hydadcr=22394_13507777&tag=hydglogoo-20&ref=pd_sl_42mumgtcax_b"]
    
    headers: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    def start_requests(self) -> Iterable[Request]:
        for url in self.urls:
            yield Request(url=url, callback=self.parse, headers=self.headers)
    
    
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


