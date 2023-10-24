# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebScrapperItem(scrapy.Item):
    text = scrapy.Field(serializer=str)
    author = scrapy.Field(serializer=str)
    tags = scrapy.Field()


class AmazonProduct(scrapy.Item):
    description = scrapy.Field(serializer=str)
    image_src = scrapy.Field(serializer=str)
    price = scrapy.Field(serializer=str)
    rating = scrapy.Field(serializer=str)
    date = scrapy.Field(serializer=str)
