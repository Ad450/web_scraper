from typing import Any, Iterable, Dict
from scrapy import Spider
from scrapy.http import Response, Request
from bs4 import BeautifulSoup
from ..utils import headers, GHANA_JOBS_URL, ContentNotFoundException


# from web_scrapper.items import WebScrapperItem


class GhanaJobsScraper(Spider):
    name: str = "ghanajobs"
    urls = [GHANA_JOBS_URL]

    custom_settings: Dict[str, Any] = {
        "ITEM_PIPELINES": {"web_scrapper.pipelines.GhanaJobsPipeline": 100}
    }

    def get_beautiful_soup(self, markup: str, parser: str) -> BeautifulSoup:
        return BeautifulSoup(markup, features=parser)

    def start_requests(self) -> Iterable[Request]:
        for url in self.urls:
            yield Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response: Response, **kwargs: Any) -> None:
        bs: BeautifulSoup = self.get_beautiful_soup(markup=response.text, parser="lxml")
        self.__parse_all_jobs_by_category(bs)

    def __parse_all_jobs_by_category(self, bs: BeautifulSoup) -> None:
        candidate_job_search_container = bs.find(
            name="div", id="candidate-jobsearch-container"
        )

        if candidate_job_search_container is None:
            raise ContentNotFoundException(
                message="candidate_job_search_container not found"
            )
        # print(candidate_job_search_container.prettify())

        search_job_frontpage_container: Iterable[
            Any
        ] = candidate_job_search_container.find_all(
            name="div", class_="search-job-frontpage"
        )

        if len(search_job_frontpage_container) == 0:
            raise ContentNotFoundException(
                message="search_job_frontpage_container array empty"
            )
        for i, category in enumerate(search_job_frontpage_container):
            category_link = category.find(name="a", class_="last-term")
            if category_link is None:
                raise ContentNotFoundException(message="category_link not found")

            url: str = GHANA_JOBS_URL.rstrip("/") + category_link["href"]
            print("..........url is" + " " + url)
            if i == 0:
                print("....inside of first yield.....")
                yield Request(
                    url=url,
                    callback=self.parse_jobs_in_category,
                    headers=headers,
                )

    def parse_jobs_in_category(self, response: Response, **kwargs: Any) -> None:
        print("..........got in parse in jobs in category.........")
        bs: BeautifulSoup = self.get_beautiful_soup(markup=response.text, parser="lxml")
        search_results = bs.find(name="div", class_="search-results")

        if search_results is None:
            raise ContentNotFoundException(message="search_results not found")

        job_description_wrapper = search_results.find_all(
            name="div", class_="job_description_wrapper"
        )

        if len(job_description_wrapper) == 0:
            raise ContentNotFoundException(message="job_description_wrapper not found")

        for job_row in job_description_wrapper.find_all(name="div", class_="row"):
            if job_row is None:
                raise ContentNotFoundException(message="job_row not found")
            job_title = job_row.find(name="h5")

            if job_title is None:
                raise ContentNotFoundException(message="job_title not found")

            print(job_title.text)
