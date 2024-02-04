from decimal import Decimal

from django.test import TestCase

from job.models import JobCategory, JobOffer
from job.parser.parser import JobParser  # Import the JobParser class


class TestJobParser(TestCase):
    def setUp(self):
        self.parser = JobParser()
        self.job_offer1 = {
            "title": "TEISĖS PSICHOLOGAS (-Ė)",
            "category": "url1",
            "company": "Įmonės pavadinimas B",
            "salary": "1719-1900",
            "salary_period": "€/mėn.",
            "salary_calculation": "Neatskaičius mokesčių",
            "location": "Kaune",
            "job_link": "https://...",
            "image_link": "https://...",
            "image_width": 100,
            "image_height": 30,
            "offer_upload_date": "prieš 21 d.",
            "source_link": "cvbankas",
        }
        self.pay_keyword = "Nuo "
        self.job_offer2 = {
            "title": "Mokytojas (-a)",
            "category": "url1",
            "company": "Įmonės pavadinimas F",
            "salary": f"{self.pay_keyword} 1200",
            "salary_period": "€/mėn.",
            "salary_calculation": "Į rankas",
            "location": "Vilniuje",
            "job_link": "https://...",
            "image_link": "https://...",
            "image_width": 100,
            "image_height": 30,
            "offer_upload_date": "prieš 3 d.",
            "source_link": "cvbankas",
        }

        self.job_offer3 = {
            "title": "Vairuotojas (-a)",
            "category": "url3",
            "company": "Įmonės pavadinimas G",
            "salary": f"{self.pay_keyword} 120",
            "salary_period": "€/d.",
            "salary_calculation": "Ant popieriaus",
            "location": "Palangoje",
            "job_link": "https://...",
            "image_link": "https://...",
            "image_width": 100,
            "image_height": 30,
            "offer_upload_date": "prieš 10 d.",
            "source_link": "cvbankas",
        }

        self.job_offer4 = {
            "title": "Programuotojas (-a)",
            "category": "url4",
            "company": "Įmonės pavadinimas H",
            "salary": "20,5-35",
            "salary_period": "€/val.",
            "salary_calculation": "Į rankas",
            "location": "Alytuje",
            "job_link": "https://...",
            "image_link": "https://...",
            "image_width": 100,
            "image_height": 30,
            "offer_upload_date": "prieš 5 d.",
            "source_link": "cvbankas",
        }
        self.category_name = "Valstybinis/viešasis administravimas"
        JobCategory.objects.create(cvbankas_url="url1", name=self.category_name)

    def test_process_single_job_offer(self):
        processed_job_offers = self.parser.process_job_offers([self.job_offer1])

        self.assertEqual(processed_job_offers[0].title, self.job_offer1["title"])
        self.assertEqual(processed_job_offers[0].category, self.category_name)
        self.assertEqual(processed_job_offers[0].company, self.job_offer1["company"])
        self.assertEqual(processed_job_offers[0].salary, self.job_offer1["salary"])
        self.assertEqual(
            processed_job_offers[0].salary_calculation,
            self.job_offer1["salary_calculation"],
        )
        self.assertEqual(processed_job_offers[0].location, self.job_offer1["location"])
        self.assertEqual(processed_job_offers[0].job_link, self.job_offer1["job_link"])
        self.assertEqual(
            processed_job_offers[0].image_link, self.job_offer1["image_link"]
        )
        self.assertEqual(
            processed_job_offers[0].image_width, self.job_offer1["image_width"]
        )
        self.assertEqual(
            processed_job_offers[0].image_height, self.job_offer1["image_height"]
        )
        self.assertEqual(
            processed_job_offers[0].offer_upload_date,
            self.job_offer1["offer_upload_date"],
        )
        self.assertEqual(
            processed_job_offers[0].source_link, self.job_offer1["source_link"]
        )

        self.assertEqual(processed_job_offers[0].gross_pay_from, Decimal("1719"))
        self.assertEqual(processed_job_offers[0].gross_pay_to, Decimal("1900"))
        self.assertEqual(processed_job_offers[0].net_pay_from, Decimal("1109.89"))
        self.assertEqual(processed_job_offers[0].net_pay_to, Decimal("1201.30"))

        self.assertEqual(len(processed_job_offers), 1)
        self.assertIsInstance(processed_job_offers[0], JobOffer)

    def test_process_multiple_job_offers(self):
        processed_job_offers = self.parser.process_job_offers(
            [self.job_offer1, self.job_offer2]
        )

        self.assertEqual(processed_job_offers[0].title, self.job_offer1["title"])
        self.assertEqual(processed_job_offers[1].title, self.job_offer2["title"])

        self.assertEqual(processed_job_offers[1].pay_keyword, self.pay_keyword)
        self.assertEqual(processed_job_offers[1].net_pay, Decimal("1200"))
        self.assertEqual(processed_job_offers[1].gross_pay, Decimal("1897.43"))

        self.assertEqual(len(processed_job_offers), 2)

        for job in processed_job_offers:
            self.assertIsInstance(job, JobOffer)

    def test_process_hourly_and_daily_job_offers(self):
        processed_job_offers = self.parser.process_job_offers(
            [self.job_offer3, self.job_offer4]
        )

        self.assertEqual(len(processed_job_offers), 2)

        for job in processed_job_offers:
            self.assertIsInstance(job, JobOffer)

        self.assertEqual(processed_job_offers[0].title, self.job_offer3["title"])
        self.assertEqual(processed_job_offers[1].title, self.job_offer4["title"])

        self.assertEqual(processed_job_offers[0].pay_keyword, self.pay_keyword)
        self.assertEqual(processed_job_offers[0].net_pay, Decimal("1514.40"))
        self.assertEqual(processed_job_offers[0].gross_pay, Decimal("2520"))

        self.assertEqual(processed_job_offers[1].gross_pay_from, Decimal("5692.56"))
        self.assertEqual(processed_job_offers[1].gross_pay_to, Decimal("9719.01"))
        self.assertEqual(processed_job_offers[1].net_pay_from, Decimal("3444.0"))
        self.assertEqual(processed_job_offers[1].net_pay_to, Decimal("5880"))
