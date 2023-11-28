from typing import Any, Iterable, Dict
import re
from scrapy import Spider
from scrapy.http import Response, Request
from bs4 import BeautifulSoup

from ..utils import headers, GHANA_JOBS_URL, ContentNotFoundException


class GhanaJobsScraper(Spider):
    name: str = "ghanajobsv2"
    urls = ["https://www.ghanajob.com/job-vacancies-search-ghana"]

    def __init__(self, name: str = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        follow_urls = []
        for i in range(1, 10):
            url = "https://www.ghanajob.com/job-vacancies-search-ghana?page=" + str(i)
            follow_urls.append(url)
        self.urls = self.urls + follow_urls

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
        job_wrappers = response.xpath("//div[@class='job-description-wrapper']")
        if len(job_wrappers) != 0:
            for job_wrapper in job_wrappers:
                job_row = job_wrapper.xpath('.//div[@class="row"]')
                link = job_row.xpath("./div/h5/a/@href")

                if link:
                    yield Request(
                        url=GHANA_JOBS_URL.rstrip("/") + link.get(),
                        callback=self.parse_job_details,
                        headers=headers,
                    )

    def parse_job_details(self, response: Response) -> Any:
        company_title = response.xpath('//div[@class="company-title"]//text()')
        company_title_link = response.xpath('//div[@class="company-title"]/a/@href')

        company_website_url = response.xpath('//tr/td[@class="website-url"]/a/@href')

        industries = response.xpath('//tr/td[@class="sector-title"]//div/text()')

        company_description = response.xpath(
            'string(//div[@class="job-ad-company-description"])'
        )

        company_description = (
            company_description.get().replace("\n", "").replace("\t", "").strip()
        )
        company_description = re.sub(r"\s+", " ", company_description)
        # get Id
        is_match = re.search(r"\d+$", response.url)
        job_id = ""
        if is_match:
            job_id = is_match.group()
        else:
            raise ContentNotFoundException(message="extracting-job-id errored")

        job_title = response.xpath("//span[@class='ad-ss-title']/text()")

        job_details = ""
        job_details_tag = response.xpath(
            f'//div[@id="job-ad-details-{job_id}"]//p/text()'
        ).getall()

        job_details = job_details.join(job_details_tag)
        job_criteria = {}
        job_criteri_tag = response.css("table.job-ad-criteria tr")

        for job_criteria_row in job_criteri_tag:
            criteria_key_tag = job_criteria_row.css("td")[0]
            criteria_value_tag = job_criteria_row.css("td")[1]

            criteria_key = (
                criteria_key_tag.xpath("string()").get().replace(":", "").strip()
            )

            if criteria_value_tag.css("div.field-item"):
                criteria_value = criteria_value_tag.css("div.field-item ::text").get()
            else:
                criteria_value = criteria_value_tag.css("::text").get()

            if criteria_key is not None and criteria_value is not None:
                job_criteria[criteria_key] = criteria_value

        print(job_criteria)

        yield {
            "company_title": company_title.get(),
            "company-link": company_title_link.get(),
            "company-website-url": company_website_url.get(),
            "industries": industries.getall(),
            "company-description": self.refine_company_description(company_description),
            "job_title": job_title.get(),
            "job_details": job_details.replace("\xa0", ""),
            "job_criteria": job_criteria,
        }

    def refine_company_description(self, description: str) -> str:
        index = description.find("Company description")

        if index != -1:
            modified_text = (
                description[:index]
                + description[index + len("Company description") :].lstrip()
            )
        else:
            modified_text = description

        return modified_text
