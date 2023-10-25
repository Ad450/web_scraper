# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import asyncio
from web_scrapper.db.mongo import MongoClient, MongoHelper
from web_scrapper.db.models.amazon_product_model import AmazonProductModel


class WebScrapperPipeline:
    def process_item(self, item, spider):
        # tags : Iterable[str] = item["tags"]
        # # take only one tag - First entry in tags
        # item["tags"]  = tags[0]
        return item


class AmazonPipeline:
    def __init__(self) -> None:
        self.mongo_instance: MongoClient = MongoClient.get_instance()

    def process_item(self, item, spider):
        rating: str = item["rating"].split(" ")[0]
        item["rating"] = rating

        asyncio.gather(
            MongoHelper.save(
                AmazonProductModel(
                    rating=item["rating"],
                    description=item["description"],
                    image_src=item["image_src"],
                    price=item["price"],
                    date=item["date"],
                )
            )
        )
        return item


class JobbermanPipeline:
    pass
