import requests
from bs4 import BeautifulSoup
from celery import shared_task

from .models import JobOffers


@shared_task
def scrape_cvbankas():
    try:
        job_offers = []
        r = requests.get("https://www.cvbankas.lt/?page=1")
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

            job_offer = {
                "title": title,
                "company": company,
                "salary": salary,
                "salary_period": salary_period,
                "salary_calculation": salary_calculation,
                "location": location,
                "job_link": job_link,
                "image_link": image_link,
                "image_width": image_width,
                "image_height": image_height,
                "source_link": "cvbankas",
            }
            job_offers.append(job_offer)
        return save_cvbankas_offers(job_offers)
    except Exception as exc:
        print("The scraping job failed. See exception:", exc, sep="\n")


@shared_task(serializer="json")
def save_cvbankas_offers(job_offers):
    print("Starting saving")
    for offer in job_offers:
        try:
            JobOffers.objects.create(
                title=offer["title"],
                company=offer["company"],
                salary=offer["salary"],
                salary_period=offer["salary_period"],
                salary_calculation=offer["salary_calculation"],
                location=offer["location"],
                job_link=offer["job_link"],
                image_link=offer["image_link"],
                image_width=offer["image_width"],
                image_height=offer["image_height"],
                source_link=offer["source_link"],
            )
        except Exception as exc:
            print("Error occuread:", exc, sep="\n")
            break
    print("Finished")
