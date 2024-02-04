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

        self.job_offer2 = {
            "title": "Mokytojas (-a)",
            "category": "url1",
            "company": "Įmonės pavadinimas F",
            "salary": "1200-1500",
            "salary_period": "€/mėn.",
            "salary_calculation": "Neatskaičius mokesčių",
            "location": "Vilniuje",
            "job_link": "https://...",
            "image_link": "https://...",
            "image_width": 100,
            "image_height": 30,
            "offer_upload_date": "prieš 3 d.",
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

        self.assertEqual(processed_job_offers[0].net_pay_from, Decimal("1109.89"))
        self.assertEqual(processed_job_offers[1].net_pay_from, Decimal("847.80"))

        self.assertEqual(len(processed_job_offers), 2)

        for job in processed_job_offers:
            self.assertIsInstance(job, JobOffer)
