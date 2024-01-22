from celery import shared_task

from scraper.sites.cvbankas import CVBankas

from .models import JobOffer


@shared_task(serializer="json")
def scrape_and_save_job_offers():
    cvbankas = CVBankas()
    save_job_offers(cvbankas.job_offers)


def save_job_offers(job_offers):
    print("Saving")
    for offer in job_offers:
        try:
            title_max_length = JobOffer._meta.get_field("title").max_length
            if len(offer["title"]) > title_max_length:
                print(f"Title exceeds {title_max_length} characters: {offer['title']}")
                continue

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
