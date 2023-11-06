from typing import Dict, Any
from bs4 import BeautifulSoup
from web_scrapper.spiders.observer import PageObserver


class AmazonPageObserver(PageObserver):
    hashes: Dict[str, Any] = {}

    def __init__(self, hashes: Dict[str, Any]) -> None:
        super().__init__(hashes)

    def save_hash_to_db(self) -> None:
        pass

    def compare_hashes(self) -> None:
        pass

    def compute_hash(self, **Kwargs: any) -> None:
        pass

    def __get_beautiful_soup(self, markup: str, parser: str) -> BeautifulSoup:
        return BeautifulSoup(markup, features=parser)

    def __get_page_element(self, bs: BeautifulSoup) -> str:
        pass
