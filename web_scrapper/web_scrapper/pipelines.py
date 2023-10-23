# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from typing import Iterable


class WebScrapperPipeline:
    def process_item(self, item, spider):
        # tags : Iterable[str] = item["tags"]
        # # take only one tag - First entry in tags
        # item["tags"]  = tags[0]
        return item


class AmazonPipeline:
    def process_item(self, item, spider):
        rating: str = item["rating"].split(" ")[0]
        item["rating"] = rating
        return item
