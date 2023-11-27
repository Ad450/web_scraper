from typing import Any, Iterable, Dict
import re
from scrapy import Spider
from scrapy.http import Response, Request
from bs4 import BeautifulSoup

# from scrapy_playwright.page import PageMethod

# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium import webdriver
from ..utils import headers, GHANA_JOBS_URL, ContentNotFoundException


# from web_scrapper.items import WebScrapperItem

# dynamically getting last pagionation
# dynamic delays


class GhanaJobsScraper(Spider):
    name: str = "ghanajobs"
    urls = [GHANA_JOBS_URL]

    custom_settings: Dict[str, Any] = {
        "ITEM_PIPELINES": {"web_scrapper.pipelines.GhanaJobsPipeline": 100},
        "DOWNLOAD_DELAY": 2,
    }

    def get_beautiful_soup(self, markup: str, parser: str) -> BeautifulSoup:
        return BeautifulSoup(markup, features=parser)

    def start_requests(self) -> Iterable[Request]:
        for url in self.urls:
            yield Request(
                url=url,
                callback=self.parse,
                headers=headers,
            )

    def parse(self, response: Response, **kwargs: Any) -> None:
        bs: BeautifulSoup = self.get_beautiful_soup(markup=response.text, parser="lxml")

        category_url: str = self.__parse_all_jobs_by_category(bs)
        if len(category_url) != 0:
            yield Request(
                url=category_url,
                callback=self.__parse_jobs_in_category,
                headers=headers,
                # meta=dict(
                #     playwright=True,
                #     playwright_include_page=True,
                #     playwright_page_coroutines=[
                #         PageMethod(
                #             "wait_for_selector",
                #             "div.jobsearch-search-results-box",
                #         )
                #     ],
                # ),
            )
        follow_urls = []
        for i in range(1, 6):
            url = GHANA_JOBS_URL + "job-vacancies-search-ghana?page=" + str(i)
            follow_urls.append(url)

        for url in follow_urls:
            yield Request(
                url=url,
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

    async def __parse_jobs_in_category(
        self,
        response: Response,
    ) -> None:
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

    async def __parse_job_details(
        self,
        response: Response,
    ) -> None:
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

        company_title_link = GHANA_JOBS_URL.rstrip("/") + company_title_node["href"]
        company_title = company_title_node.text

        company_logo_node = job_node.find(name="div", class_="company-logo-mobile")

        if company_logo_node is None:
            raise ContentNotFoundException(message="company_logo_node not found")

        company_logo_image = company_logo_node.find(name="img")
        if company_logo_image is None:
            company_logo_image = None
        # print(company_logo_image["src"])

        company_info_node = company_profile_node.find(
            name="table", class_="company-info"
        )
        if company_info_node is None:
            raise ContentNotFoundException(message="company_info_node not found")
        website_label = company_info_node.find(name="td", class_="website-label")
        website_url_node = company_info_node.find(name="td", class_="website-url")

        website_url = (
            website_url_node.find(name="a")["href"]
            if website_url_node is not None
            else None
        )

        sector_label = company_info_node.find(name="td", class_="sector-label")
        sector_title = company_info_node.find(name="td", class_="sector-title")

        if sector_title is None:
            raise ContentNotFoundException(message="sector_title not found")
        fields = []
        for sector_field in sector_title.find_all(name="div", class_="field-item"):
            fields.append(sector_field.text)

        job_ad_details_node = job_node.find(name="div", id="job-ad-details-" + job_id)
        job_title_node = job_ad_details_node.find(name="span", class_="ad-ss-title")
        job_description_node = job_ad_details_node.find_all(name="p")

        descriptions = []
        job_description = ""
        for description in job_description_node:
            descriptions.append(description.text)

        job_description = job_description.join(descriptions)

        job_criteria = {}
        job_criteria_node = job_node.find(name="table", class_="job-ad-criteria")
        if job_criteria_node is None:
            raise ContentNotFoundException(message="job_criteria_node not found")

        for criteria in job_criteria_node.find_all(name="tr"):
            criteria_key = criteria.find_all(name="td")[0]
            criteria_value_node = criteria.find_all(name="td")[1]
            criteria_value = ""
            if criteria_value_node is None:
                criteria_value_node = None
            else:
                criteria_value_field = criteria_value_node.find(
                    name="div", class_="field-item"
                )
                if criteria_value_field is None:
                    criteria_value = None
                else:
                    criteria_value = criteria_value_field.get_text(strip=True)

            if criteria_key is not None and criteria_value is not None:
                key = criteria_key.get_text(strip=True).replace(":", "")
                job_criteria[key] = criteria_value

        yield Request(
            url=company_title_link,
            callback=self.__parse_company_description,
            headers=headers,
            meta={
                "job_details": {
                    "company-title-link": company_title_link,
                    "company-title": company_title,
                    "company-image-url": company_logo_image["src"]
                    if company_logo_image is not None
                    else None,
                    "company-website-label": website_label.text
                    if website_label is not None
                    else None,
                    "company-website-url": website_url,
                    "company-sector": sector_label.text,
                    "company-sector-fields": fields,
                    "job-title": job_title_node.text
                    if job_title_node is not None
                    else None,
                    "job-description": job_description,
                },
                "job_criteria": job_criteria,
            },
        )

    async def __parse_company_description(
        self,
        response: Response,
    ) -> str:
        bs: BeautifulSoup = self.get_beautiful_soup(markup=response.text, parser="lxml")
        company_profile_description = bs.find(
            name="div", class_="company-profile-description"
        )
        if company_profile_description is None:
            raise ContentNotFoundException(message="sector_title not found")

        company_description_node = company_profile_description.find_all(name="p")
        company_description = ""
        if company_description_node is None or len(company_description_node) == 0:
            company_description_node = None
        else:
            descriptions = []
            for description in company_description_node:
                descriptions.append(description.text)
            company_description = company_description.join(descriptions)

        yield {
            **response.meta["job_details"],
            **response.meta["job_criteria"],
            "company-description": company_description,
        }
