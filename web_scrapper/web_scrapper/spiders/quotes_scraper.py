
"""
Simple Quotes scraper
"""

from typing import Any, Iterable
from scrapy import Spider
from scrapy.http import Request, Response
from web_scrapper.items import WebScrapperItem
class QuotesScraper(Spider):

    name:str = "quotes"
    urls= ["https://quotes.toscrape.com/page/1",
        "https://quotes.toscrape.com/page/2/" ]
    
    #override
    def start_requests (self) -> Iterable[Request] :
        for url in self.urls:
            yield  Request(url=url, callback=self.parse)

    def parse(self, response: Response, **kwargs: Any) -> Any:
        for quote in response.css("div.quote") :
            yield WebScrapperItem(
                 text = quote.css("span.text::text").get(),
                 author =  quote.css("small.author::text").get(),
                 tags = quote.css("div.tags a.tag::text").getall()
            )