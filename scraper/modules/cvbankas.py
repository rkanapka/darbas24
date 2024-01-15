import requests
from bs4 import BeautifulSoup
from celery import shared_task

from ..models import JobOffers


@shared_task
def scrape_cvbankas():
    try:
        print("Starting the scraping tool")
        job_offers = []
        # execute my request, parse the data using XML
        # parser in BS4
        r = requests.get("https://www.cvbankas.lt/?page=1")
        soup = BeautifulSoup(r.content, features="xml")
        # select only the "items" I want from the data
        articles = soup.findAll("article")

        # for each "item" I want, parse it into a list
        for a in articles:
            print(a)
            title = a.find("h3").text
            company = [
                span for span in soup.find_all("span", {"class": "dib mt5 mr5"})
            ][0].text
            salary = [
                span for span in soup.find_all("span", {"class": "salary_amount"})
            ][0].text
            salary_period = [
                span for span in soup.find_all("span", {"class": "salary_period"})
            ][0].text
            salary_calculation = [
                span for span in soup.find_all("span", {"class": "salary_calculation"})
            ][0].text
            location = soup.find("span", {"class": "list_city"}).text
            job_link = a.find("a").get("href")
            image_link = a.find("img").get("src")

            job_offer = {
                "title": title,
                "company": company,
                "salary": salary,
                "salary_period": salary_period,
                "salary_calculation": salary_calculation,
                "location": location,
                "job_link": job_link,
                "image_link": image_link,
                "source_link": "cvbankas",
            }
            print(
                title, company, salary, salary_calculation, location, job_link, sep="\n"
            )
            job_offers.append(job_offer)
        return save_cvbankas_offers(job_offers)
    except Exception as e:
        print("The scraping job failed. See exception:")
        print(e)


@shared_task(serializer="json")
def save_cvbankas_offers(job_offers):
    print("starting")
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
                source_link=offer["source_link"],
            )
        except Exception as e:
            print("Error occuread:")
            print(e)
            break
    print("finished")
