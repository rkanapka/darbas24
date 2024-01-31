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
        category_url_slugs_with_names = {
            category.cvbankas_url: category.name
            for category in JobCategory.objects.all()
        }
        title_max_length = JobOffer._meta.get_field("title").max_length
        processed_job_offers = []
        # TODO solve edge cases: €/d. or €/val
        for offer in job_offers:
            offer["title"] = offer["title"][:title_max_length]
            offer["category"] = category_url_slugs_with_names.get(offer["category"])

            offer["gross_pay"] = ""
            offer["net_pay"] = ""

            if offer["salary"]:
                pay_range_start, pay_range_end, pay, pay_keyword = (
                    None,
                    None,
                    None,
                    None,
                )
                if "mėn" in offer["salary_period"]:
                    if "-" in offer["salary"]:
                        pay_range_start, pay_range_end = offer["salary"].split("-")
                    else:
                        pay = [int(s) for s in offer["salary"].split() if s.isdigit()][
                            0
                        ]
                        pay_keyword = [
                            str(s) for s in offer["salary"].split() if s.isalpha()
                        ]
                        pay_keyword = pay_keyword[0] + " " if pay_keyword else ""

                    is_payment_net = (
                        True if offer["salary_calculation"] == "Į rankas" else False
                    )

                    salary_calculation = SalaryService()
                    if pay is not None:
                        pay = salary_calculation.calculate_pay(pay, is_payment_net)
                        if offer["salary_calculation"] == "Į rankas":
                            offer["gross_pay"], offer["net_pay"] = (
                                f"{pay_keyword}{pay}",
                                offer["salary"],
                            )
                        else:
                            offer["gross_pay"], offer["net_pay"] = (
                                offer["salary"],
                                f"{pay_keyword}{pay}",
                            )
                    else:
                        pay_from = salary_calculation.calculate_pay(
                            int(pay_range_start), is_payment_net
                        )
                        pay_to = salary_calculation.calculate_pay(
                            int(pay_range_end), is_payment_net
                        )

                        if offer["salary_calculation"] == "Į rankas":
                            offer["gross_pay"], offer["net_pay"] = (
                                f"{pay_from}-{pay_to}",
                                offer["salary"],
                            )
                        else:
                            offer["gross_pay"], offer["net_pay"] = (
                                offer["salary"],
                                f"{pay_from}-{pay_to}",
                            )

            processed_job_offers.append(create_job_offer_object(offer))
        print("Finished processing in: %s seconds" % (time.time() - start_time))
        return processed_job_offers
    except Exception as exc:
        print("Error occuread:", exc, sep="\n")


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
