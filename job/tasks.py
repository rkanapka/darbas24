from celery import shared_task

from scraper.sites.cvbankas import CVBankas

from .models import JobOffer


@shared_task(serializer="json")
def scrape_and_save_job_offers():
    cvbankas_job_offers = CVBankas().scrape()
    save_job_offers(cvbankas_job_offers)


def save_job_offers(cvbankas_job_offers):
    for offer in cvbankas_job_offers:
        try:
            JobOffer.objects.create(
                title=offer["title"],
                category=offer["category"],
                company=offer["company"],
                salary=offer["salary"],
                salary_period=offer["salary_period"],
                salary_calculation=offer["salary_calculation"],
                location=offer["location"],
                job_link=offer["job_link"],
                image_link=offer["image_link"],
                image_width=offer["image_width"],
                image_height=offer["image_height"],
                offer_upload_date=offer["offer_upload_date"],
                source_link=offer["source_link"],
            )
        except Exception as exc:
            print("Error occuread:", exc, sep="\n")
            break
    print("Finished")
