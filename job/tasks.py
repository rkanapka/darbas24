import time

from celery import shared_task

from .models import JobCategory, JobOffer
from .parser.parser import JobParser
from .scrapers.cvbankas import CVBankas


@shared_task(serializer="json")
def scrape_cvbankas():
    category_url_slugs = (
        category.cvbankas_url for category in JobCategory.objects.all()
    )
    cvbankas = CVBankas(category_url_slugs)
    job_offer_objects = JobParser().process_job_offers(cvbankas.job_offers)
    save_job_offers(job_offer_objects)


def save_job_offers(job_offer_objects):
    print("Saving offers")
    start_time = time.time()
    try:
        JobOffer.objects.bulk_create(job_offer_objects)
    except Exception as exc:
        print("Error occuread:", exc, sep="\n")
    print("Finished saving in: %s seconds" % (time.time() - start_time))
