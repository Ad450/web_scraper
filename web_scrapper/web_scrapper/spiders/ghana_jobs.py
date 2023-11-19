from typing import Any, Iterable, Dict
import re
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

        category_url: str = self.__parse_all_jobs_by_category(bs)
        if len(category_url) != 0:
            yield Request(
                url=category_url,
                callback=self.__parse_jobs_in_category,
                headers=headers,
            )

    def __parse_all_jobs_by_category(self, bs: BeautifulSoup) -> str:
        candidate_job_search_container = bs.find(
            name="div", id="candidate-jobsearch-container"
        )

        if candidate_job_search_container is None:
            raise ContentNotFoundException(
                message="candidate_job_search_container not found"
            )

        search_job_frontpage_container: Iterable[
            Any
        ] = candidate_job_search_container.find_all(
            name="div", class_="search-job-frontpage"
        )

        if len(search_job_frontpage_container) == 0:
            raise ContentNotFoundException(
                message="search_job_frontpage_container array empty"
            )

        i = 0
        url: str = ""
        for category in search_job_frontpage_container:
            category_link = category.find(name="a", class_="last-term")
            if category_link is None:
                raise ContentNotFoundException(message="category_link not found")

            if i == 0:
                url = GHANA_JOBS_URL.rstrip("/") + category_link["href"]

                return url
            i += 1
        return url

    def __parse_jobs_in_category(self, response: Response, **kwargs: Any) -> None:
        bs: BeautifulSoup = self.get_beautiful_soup(markup=response.text, parser="lxml")
        job_search_results_box = bs.find(name="div", id="jobsearch-search-results-box")

        if job_search_results_box is None:
            raise ContentNotFoundException(message="job_search_results_box not found")

        search_results = job_search_results_box.find(
            name="div", class_="search-results jobsearch-results"
        )

        if search_results is None:
            raise ContentNotFoundException(message="search_results not found")

        job_description_wrapper = search_results.find_all(
            name="div", class_="job-description-wrapper"
        )

        if len(job_description_wrapper) == 0:
            raise ContentNotFoundException(message="job_description_wrapper not found")

        for row in job_description_wrapper:
            job_row = row.find(name="div", class_="row")

            if job_row is None:
                raise ContentNotFoundException(message="job_row not found")

            job_title = job_row.find(name="h5")

            if job_title is None:
                raise ContentNotFoundException(message="job_title not found")
            job_title_link = job_title.find(name="a")
            if job_title_link is None:
                raise ContentNotFoundException(message="job_title_link not found")

            job_details_url = GHANA_JOBS_URL.rstrip("/") + job_title_link["href"]

            yield Request(
                url=job_details_url,
                callback=self.__parse_job_details,
                headers=headers,
            )

    def __parse_job_details(self, response: Response, **kwargs: Any) -> None:
        bs: BeautifulSoup = self.get_beautiful_soup(markup=response.text, parser="lxml")
        container_page_content = bs.find(name="div", class_="container-page-content")

        if container_page_content is None:
            raise ContentNotFoundException(message="container_page_content not found")

        # parse the url and extracts the last number, id
        is_match = re.search(r"\d+$", response.url)
        job_id = ""
        if is_match:
            job_id = is_match.group()
        else:
            raise ContentNotFoundException(message="extracting-job-id errored")

        job_node = container_page_content.find(name="div", id="node-" + job_id)

        if job_node is None:
            raise ContentNotFoundException(message="job_node not found")

        company_profile_node = job_node.find(name="div", id="company-profile-" + job_id)

        if company_profile_node is None:
            raise ContentNotFoundException(message="company_profile_node not found")

        company_title_node = company_profile_node.find(
            name="div", class_="company-title"
        )

        if company_title_node is None:
            raise ContentNotFoundException(message="company_title not found")

        company_title_node = company_title_node.find(name="a")

        if company_title_node is None:
            raise ContentNotFoundException(message="company_title_node not found")

        # company_title_link = GHANA_JOBS_URL.rstrip("/") + company_title_node["href"]
        # company_title = company_title_node.text

        company_logo_node = job_node.find(name="div", class_="company-logo-mobile")

        if company_logo_node is None:
            raise ContentNotFoundException(message="company_logo_node not found")

        company_logo_image = company_logo_node.find(name="img")
        if company_logo_node is None:
            raise ContentNotFoundException(message="company_logo_node not found")
        # print(company_logo_image["src"])
