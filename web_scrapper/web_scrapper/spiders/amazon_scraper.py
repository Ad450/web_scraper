from typing import Any, Iterable, Dict
from scrapy import Spider
from scrapy.http import Response, Request
from bs4 import BeautifulSoup
from ..utils import headers, amazon_url
from ..items import AmazonProduct

# from web_scrapper.items import WebScrapperItem


class AmazonScraper(Spider):
    name: str = "amazon_scraper"
    urls = [amazon_url]

    custom_settings: Dict[str, Any] = {
        "ITEM_PIPELINES": {"web_scrapper.pipelines.AmazonPipeline": 100}
    }

    def get_beautiful_soup(self, markup: str, parser: str) -> BeautifulSoup:
        return BeautifulSoup(markup, features=parser)

    def start_requests(self) -> Iterable[Request]:
        for url in self.urls:
            yield Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response: Response, **kwargs: Any) -> None:
        bs: BeautifulSoup = self.get_beautiful_soup(markup=response.text, parser="lxml")
        for category in bs.find_all(name="div", class_="puis-card-container"):
            image_url: str = category.find(name="a", class_="a-link-normal")["href"]
            description: str = category.find(
                name="span", class_="a-size-base-plus"
            ).text
            rating: str = category.find(name="span", class_="a-icon-alt").text
            price_tag = category.find(name="span", class_="a-price")

            if price_tag:
                price: str = (
                    price_tag.find(name="span", class_="a-offscreen").text
                    if price_tag.find(name="span", class_="a-offscreen") is not None
                    else ""
                )
            date_tag = category.find(name="span", class_="a-color-base a-text-bold")
            date: str = date_tag.text if date_tag is not None else ""

            yield AmazonProduct(
                image_src=image_url,
                description=description,
                rating=rating,
                price=price,
                date=date,
            )
