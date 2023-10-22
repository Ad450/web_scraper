
from typing import Optional
from scrapy.spiders import Spider
from scrapy.http import Response
from web_scrapper.items import WebScrapperItem


class QuotesCrawler (Spider):
    name:str = "quotes_crawler"
    start_urls = ["https://quotes.toscrape.com"]

    def parse (self, response:Response, **kwargs) -> None :
         next_page:Optional[str] = response.css("li.next a::attr(href)").get()
         for quote in response.css("div.quote") :
             yield WebScrapperItem(
                 text = quote.css("span.text::text").get(),
                 author =  quote.css("small.author::text").get(),
                 tags = quote.css("div.tags a.tag::text").getall()
             )      
         if next_page is not None:
                 yield response.follow(url =response.urljoin(next_page),callback=self.parse)               
