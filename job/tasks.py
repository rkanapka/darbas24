import time

from celery import shared_task

from .models import JobCategory, JobOffer
from .scrapers.cvbankas import CVBankas
from .services.salary import SalaryService


@shared_task(serializer="json")
def scrape_cvbankas():
    category_url_slugs = (
        category.cvbankas_url for category in JobCategory.objects.all()
    )
    cvbankas = CVBankas(category_url_slugs)
    job_offer_objects = process_job_offers(cvbankas.job_offers)
    save_job_offers(job_offer_objects)


def process_job_offers(job_offers):
    print("Processing offers")
    start_time = time.time()
    try:
        category_slugs_with_names = get_category_slugs_with_names()
        title_max_length = JobOffer._meta.get_field("title").max_length
        salary_service = SalaryService()
        processed_job_offers = []
        for offer in job_offers:
            processed_offer = process_single_job_offer(
                offer, category_slugs_with_names, title_max_length, salary_service
            )
            processed_job_offers.append(processed_offer)
        print("Finished processing in: %s seconds" % (time.time() - start_time))
        return processed_job_offers
    except Exception as exc:
        print("Error occuread:", exc, sep="\n")


def get_category_slugs_with_names():
    return {
        category.cvbankas_url: category.name for category in JobCategory.objects.all()
    }


def process_single_job_offer(
    offer, category_slugs_with_names, title_max_length, salary_service
):
    offer["title"] = offer["title"][:title_max_length]
    offer["category"] = category_slugs_with_names.get(offer["category"], "")
    offer["gross_pay"], offer["net_pay"] = "", ""

    if offer["salary"]:
        process_salary(offer, salary_service)

    return create_job_offer_object(offer)


def process_salary(offer, salary_service):
    pay_range_start, pay_range_end, pay, pay_keyword = None, None, None, None

    if "mėn" in offer["salary_period"]:  # TODO solve edge cases: €/d. or €/val
        if "-" in offer["salary"]:
            pay_range_start, pay_range_end = offer["salary"].split("-")
        else:
            pay_parts = offer["salary"].split()
            pay = next((int(s) for s in pay_parts if s.isdigit()), None)
            pay_keyword = next((s for s in pay_parts if s.isalpha()), "")
            pay_keyword += " " if pay_keyword else ""

        is_payment_net = offer["salary_calculation"] == "Į rankas"

        if pay is not None:
            pay = salary_service.calculate_pay(pay, is_payment_net)
            offer["gross_pay"], offer["net_pay"] = (
                (f"{pay_keyword}{pay}", offer["salary"])
                if offer["salary_calculation"] == "Į rankas"
                else (offer["salary"], f"{pay_keyword}{pay}")
            )
        else:
            pay_from = salary_service.calculate_pay(
                int(pay_range_start), is_payment_net
            )
            pay_to = salary_service.calculate_pay(int(pay_range_end), is_payment_net)

            offer["gross_pay"], offer["net_pay"] = (
                (f"{pay_from}-{pay_to}", offer["salary"])
                if offer["salary_calculation"] == "Į rankas"
                else (offer["salary"], f"{pay_from}-{pay_to}")
            )


def save_job_offers(job_offer_objects):
    print("Saving offers")
    start_time = time.time()
    try:
        JobOffer.objects.bulk_create(job_offer_objects)
    except Exception as exc:
        print("Error occuread:", exc, sep="\n")
    print("Finished saving in: %s seconds" % (time.time() - start_time))


def create_job_offer_object(offer):
    return JobOffer(
        title=offer["title"],
        category=offer["category"],
        company=offer["company"],
        salary=offer["salary"],
        salary_period=offer["salary_period"],
        salary_calculation=offer["salary_calculation"],
        gross_pay=offer["gross_pay"],
        net_pay=offer["net_pay"],
        location=offer["location"],
        job_link=offer["job_link"],
        image_link=offer["image_link"],
        image_width=offer["image_width"],
        image_height=offer["image_height"],
        offer_upload_date=offer["offer_upload_date"],
        source_link=offer["source_link"],
    )
