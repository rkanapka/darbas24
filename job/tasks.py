import time

from celery import shared_task

from scraper.sites.cvbankas import CVBankas

from .models import JobOffer


@shared_task(serializer="json")
def scrape_and_save_job_offers():
    cvbankas = CVBankas()
    save_job_offers(cvbankas.job_offers)


def save_job_offers(job_offers):
    print("Saving")
    start_time = time.time()
    try:
        job_offer_objects = [create_job_offer_object(offer) for offer in job_offers]
        JobOffer.objects.bulk_create(job_offer_objects)
    except Exception as exc:
        print("Error occuread:", exc, sep="\n")
    print("Finished in --- %s seconds ---" % (time.time() - start_time))


def create_job_offer_object(offer):
    title_max_length = JobOffer._meta.get_field("title").max_length
    return JobOffer(
        title=offer["title"][:title_max_length],
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
