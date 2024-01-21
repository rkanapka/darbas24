import requests
from bs4 import BeautifulSoup


class CVBankas:
    def __init__(self):
        self.url = "https://www.cvbankas.lt"
        self.source = "cvbankas"

    def scrape(self):
        try:
            last_page_number = self.get_last_page_number()
            return self.scrape_job_offers(last_page_number)
        except Exception as exc:
            print("The scraping job failed. See exception:", exc, sep="\n")

    def scrape_job_offers(self, last_page_number):
        job_offers = []
        for page_number in range(1, last_page_number + 1):
            r = requests.get(f"{self.url}/?page={page_number}")
            soup = BeautifulSoup(r.content, features="xml")
            articles = soup.findAll("article")
            for a in articles:
                print(a)
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

                category = self.get_job_offer_category(job_link)

                job_offer = {
                    "title": title,
                    "category": category,
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
                job_offers.append(job_offer)
        return job_offers

    def get_last_page_number(self):
        home_request = requests.get(f"{self.url}")
        home_soup = BeautifulSoup(home_request.content, features="xml")
        ul_pages_element = home_soup.find("ul", {"class": "pages_ul_inner"})
        il_pages_elements = ul_pages_element.find_all("li")
        last_page = int(il_pages_elements[-1].text)
        return last_page

    def get_job_offer_category(self, job_link):
        offer_request = requests.get(job_link)
        offer_soup = BeautifulSoup(offer_request.content, features="xml")
        li_elements = offer_soup.find_all("li", {"class": "nav_additional_li"})
        category = li_elements[-1].text
        return category
