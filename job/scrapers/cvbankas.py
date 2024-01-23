import asyncio

from aiolimiter import AsyncLimiter
from bs4 import BeautifulSoup
from httpx import AsyncClient

from .scraper import IScraper


class CVBankas(IScraper):
    def __init__(self):
        self.url = "https://www.cvbankas.lt"
        self.source = "cvbankas"
        self.job_offers = []

        asyncio.run(self.fetch())

    async def fetch(self):
        try:
            tasks = []
            throttler = AsyncLimiter(max_rate=10, time_period=6)
            async with AsyncClient() as session:
                last_page_number = await self.get_last_page_number(session=session)
                tasks = [
                    asyncio.create_task(
                        self.scrape_page(
                            page_number, session=session, throttler=throttler
                        ),
                        name=f"Page {page_number}",
                    )
                    for page_number in range(1, last_page_number + 1)
                ]
                done, pending = await asyncio.wait(
                    tasks, return_when=asyncio.ALL_COMPLETED
                )

                for task in done:
                    print(f"Done: {task.get_name()}")
                for task in pending:
                    task.cancel()
        except Exception as exc:
            print("The scraping job failed. See exception:", exc, sep="\n")

    async def scrape_page(self, page_number, session, throttler):
        async with throttler:
            r = await session.get(f"{self.url}?page={page_number}")
            soup = BeautifulSoup(r.content, features="xml")
            articles = soup.findAll("article")
            for a in articles:
                title = a.find("h3")
                title = "" if title is None else title.text
                company = a.find("span", {"class": "dib mt5 mr5"})
                company = "" if company is None else company.text
                salary = a.find("span", {"class": "salary_amount"})
                salary = "" if salary is None else salary.text
                salary_period = a.find("span", {"class": "salary_period"})
                salary_period = "" if salary_period is None else salary_period.text
                salary_calculation = a.find("span", {"class": "salary_calculation"})
                salary_calculation = (
                    "" if salary_calculation is None else salary_calculation.text
                )
                location = a.find("span", {"class": "list_city"})
                location = "" if location is None else location.text
                job_link = a.find("a").get("href")
                image_link = a.find("img").get("src")
                image_width = a.find("img").get("width")
                image_height = a.find("img").get("height")
                offer_upload_date = a.find("span", {"class": "txt_list_2"})
                offer_upload_date = (
                    "" if offer_upload_date is None else offer_upload_date.text
                )

                # category = await self.get_job_offer_category(job_link, session=session)

                self.job_offers.append(
                    {
                        "title": title,
                        "category": "test",
                        "company": company,
                        "salary": salary,
                        "salary_period": salary_period,
                        "salary_calculation": salary_calculation,
                        "location": location,
                        "job_link": job_link,
                        "image_link": image_link,
                        "image_width": image_width,
                        "image_height": image_height,
                        "offer_upload_date": offer_upload_date,
                        "source_link": self.source,
                    }
                )

    async def get_last_page_number(self, session):
        home_request = await session.get(f"{self.url}")
        home_soup = BeautifulSoup(home_request.content, features="xml")
        ul_pages_element = home_soup.find("ul", {"class": "pages_ul_inner"})
        il_pages_elements = ul_pages_element.find_all("li")
        return int(il_pages_elements[-1].text)

    async def get_job_offer_category(self, job_link, session):
        offer_request = await session.get(job_link)
        offer_soup = BeautifulSoup(offer_request.content, features="xml")
        li_elements = offer_soup.find_all("li", {"class": "nav_additional_li"})
        return li_elements[-1].text
