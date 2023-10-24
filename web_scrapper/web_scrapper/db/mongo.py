from typing import Optional, Iterable, Callable
from asyncio import run
from mongoengine import connect, Document, QuerySet
from web_scrapper.utils import mongo_connection_string


class MongoClient:
    __instance: Optional["MongoClient"] = None

    def __init__(self) -> None:
        run(self._initialize_mongo(host=mongo_connection_string))

    @staticmethod
    def get_instance() -> "MongoClient":
        if MongoClient.__instance is None:
            MongoClient.__instance = MongoClient()
            return MongoClient.__instance
        else:
            return MongoClient.__instance

    async def _initialize_mongo(self, host: str) -> None:
        try:
            connect(host=host)
            return
        except Exception as e:
            raise e


class MongoHelper:
    @staticmethod
    async def save(model: Document) -> None:
        model.save()

    @staticmethod
    async def get_unique_identity(query: Callable) -> QuerySet:
        return query()

    @staticmethod
    async def get_all(query: Callable) -> Iterable[QuerySet]:
        return query()
