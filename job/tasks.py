import time
from decimal import Decimal

from celery import shared_task

from .models import JobCategory, JobOffer
from .scrapers.cvbankas import CVBankas
from .services.salary import SalaryService

WORK_HOURS_IN_MONTH = 168
WORK_DAYS_IN_MONTH = 21


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

    if offer["salary"]:
        offer = process_salary(offer, salary_service)
    return create_job_offer_object(offer)


def process_salary(offer, salary_service):
    pay_range_start, pay_range_end, pay, scraped_pay_keyword = None, None, None, None
    is_payment_net = offer["salary_calculation"] == "Į rankas"
    offer["salary"] = offer["salary"].replace(",", ".")

    if "-" in offer["salary"]:
        pay_range_start, pay_range_end = [
            Decimal(amount) for amount in offer["salary"].split("-")
        ]
        pay_range_start, pay_range_end = calculate_monthly_rate_pay_range(
            offer, pay_range_start, pay_range_end
        )
    else:
        scraped_pay_parts = offer["salary"].split()
        scraped_pay_keyword = parse_payment_keyword(scraped_pay_parts)
        scraped_pay = next(
            (Decimal(s) for s in scraped_pay_parts if s.replace(".", "").isdigit()),
            None,
        )
        pay = calculate_monthly_rate_for_single_pay(offer, scraped_pay)

    if pay is not None:
        calculated_pay = salary_service.calculate_pay(pay, is_payment_net)
        processed_offer = set_single_payment(
            offer, pay, scraped_pay_keyword, is_payment_net, calculated_pay
        )
    else:
        pay_from = salary_service.calculate_pay(pay_range_start, is_payment_net)
        pay_to = salary_service.calculate_pay(pay_range_end, is_payment_net)
        processed_offer = set_payment_range(
            offer, pay_range_start, pay_range_end, is_payment_net, pay_from, pay_to
        )
    return processed_offer


def parse_payment_keyword(pay_parts):
    pay_keyword = next((s for s in pay_parts if s.isalpha()), "")
    pay_keyword += " " if pay_keyword else ""
    return pay_keyword


def set_single_payment(offer, pay, scraped_pay_keyword, is_payment_net, calculated_pay):
    offer["pay_keyword"] = scraped_pay_keyword
    if is_payment_net:
        offer["gross_pay"], offer["net_pay"] = calculated_pay, pay
    else:
        offer["gross_pay"], offer["net_pay"] = pay, calculated_pay
    return offer


def set_payment_range(
    offer, pay_range_start, pay_range_end, is_payment_net, pay_from, pay_to
):
    if is_payment_net:
        offer["gross_pay_from"], offer["gross_pay_to"] = pay_from, pay_to
        offer["net_pay_from"], offer["net_pay_to"] = pay_range_start, pay_range_end
    else:
        offer["gross_pay_from"], offer["gross_pay_to"] = pay_range_start, pay_range_end
        offer["net_pay_from"], offer["net_pay_to"] = pay_from, pay_to
    return offer


def calculate_monthly_rate_pay_range(offer, pay_range_start, pay_range_end):
    if "€/val." in offer["salary_period"]:
        pay_range_start = pay_range_start * WORK_HOURS_IN_MONTH
        pay_range_end = pay_range_end * WORK_HOURS_IN_MONTH
    if "€/d." in offer["salary_period"]:
        pay_range_start = pay_range_start * WORK_DAYS_IN_MONTH
        pay_range_end = pay_range_end * WORK_DAYS_IN_MONTH
    return pay_range_start, pay_range_end


def calculate_monthly_rate_for_single_pay(offer, pay):
    if "€/val." in offer["salary_period"]:
        pay = pay * WORK_HOURS_IN_MONTH
    if "€/d." in offer["salary_period"]:
        pay = pay * WORK_DAYS_IN_MONTH
    return pay


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
        pay_keyword=offer.get("pay_keyword", ""),
        gross_pay=offer.get("gross_pay", None),
        net_pay=offer.get("net_pay", None),
        gross_pay_from=offer.get("gross_pay_from", None),
        gross_pay_to=offer.get("gross_pay_to", None),
        net_pay_from=offer.get("net_pay_from", None),
        net_pay_to=offer.get("net_pay_to", None),
        location=offer["location"],
        job_link=offer["job_link"],
        image_link=offer["image_link"],
        image_width=offer["image_width"],
        image_height=offer["image_height"],
        offer_upload_date=offer["offer_upload_date"],
        source_link=offer["source_link"],
    )
