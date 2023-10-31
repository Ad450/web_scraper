from typing import Any, Iterable, Optional, Dict
from scrapy import Spider
from scrapy.http import Response
from bs4 import BeautifulSoup


class JobbermanScraper(Spider):
    name: str = "jobberman"

    custom_settings: Dict[str, Any] = {
        "ITEM_PIPELINES": {"web_scrapper.pipelines.JobbermanPipeline": 100}
    }

    def __init__(self, name: Optional[str] = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        self.start_urls = self.__get_urls()

    def get_beautiful_soup(self, markup: str, parser: str) -> BeautifulSoup:
        return BeautifulSoup(markup, features=parser)

    def __get_urls(self) -> Iterable[str]:
        url: str = "https://www.jobberman.com.gh/jobs"
        all_urls: Iterable[str] = []
        for i in range(2, 100):
            all_urls.append(f"https://www.jobberman.com.gh/jobs?page={i}")
        return [url, *all_urls]

    def parse(self, response: Response, **kwargs: Any) -> None:
        bs: BeautifulSoup = self.get_beautiful_soup(markup=response.text, parser="lxml")
        for job in bs.find_all(
            name="div",
            class_="mx-5 md:mx-0 flex flex-wrap col-span-1 mb-5 bg-white rounded-lg border border-gray-300 hover:border-gray-400 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-gray-500",
        ):
            job_title: str = job.find(
                name="p", class_="text-lg font-medium break-words text-link-500"
            ).text

            company: str = job.find(name="p", class_="text-sm text-link-500").text

            job_type_tag = job.find(
                name="div", class_="flex flex-wrap mt-3 text-sm text-gray-500 md:py-0"
            )

            job_type_arr = job_type_tag.find_all(
                name="span",
                class_="mb-3 px-3 py-1 rounded bg-brand-secondary-100 mr-2 text-loading-hide",
            )

            salary = (
                job_type_arr[2].find(name="span", class_="mr-1").text
                if job_type_arr[2].find(name="span", class_="mr-1") is not None
                else "Confidential"
            )

            job_function = job.find(
                name="p",
                class_="text-sm text-gray-500 text-loading-animate inline-block",
            ).text

            company_logo_tag = job.find(
                name="div",
                class_="flex justify-center items-center p-1 w-[100px] h-[100px] align-middle bg-white rounded-md border-2 border-gray-300",
            )

            company_logo = ""
            if company_logo_tag is not None:
                img_tag = company_logo_tag.find(name="img")
                if img_tag is not None:
                    company_logo = img_tag["src"]
                else:
                    alt_tag = company_logo_tag.find(name="span")
                    if alt_tag:
                        company_logo = alt_tag.text

            job_description = ""
            job_description_tag = job.find(
                name="p",
                class_="text-sm font-normal text-gray-700 md:text-gray-500 md:pl-5",
            )
            if job_description_tag:
                job_description = job_description_tag.text

            yield {
                "job-title": str(job_title).strip("\n"),
                "company-name": company.strip("\n"),
                "location": str(job_type_arr[0].text).strip("\n"),
                "type": job_type_arr[1].text.strip("\n"),
                "salary": salary.strip("\n"),
                "job-function": job_function.replace("\n", ""),
                "company-logo": company_logo,
                "job_description": job_description.strip("\n"),
            }
