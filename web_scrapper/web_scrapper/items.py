# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebScrapperItem(scrapy.Item):
  text = scrapy.Field(serializer=str)
  author = scrapy.Field(serializer=str)
  tags = scrapy.Field()
    

