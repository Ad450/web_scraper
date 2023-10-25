from typing import Any, Iterable, Optional, Dict
from scrapy import Spider
from scrapy.http import Response


class JobbermanScraper(Spider):
    name: str = "jobberman"

    custom_settings: Dict[str, Any] = {
        "ITEM_PIPELINES": {"web_scrapper.pipelines.JobbermanPipeline": 100}
    }

    def __init__(self, name: Optional[str] = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        self.start_urls = self.__get_urls()

    def __get_urls(self) -> Iterable[str]:
        url: str = "https://www.jobberman.com.gh/jobs"
        all_urls: Iterable[str] = []
        for i in range(2, 100):
            all_urls.append(f"https://www.jobberman.com.gh/jobs?page={i}")
        return [url, *all_urls]

    def parse(self, response: Response, **kwargs: Any) -> None:
        print(response.text)
