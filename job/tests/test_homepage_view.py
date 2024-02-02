from django.test import RequestFactory, TestCase

from darbas24.views import HomePageView
from job.models import JobCity, JobOffer


class TestHomePageView(TestCase):
    def setUp(self):
        JobCity.objects.create(name="Vilnius", locative_case_name="Vilniuje")
        JobCity.objects.create(name="Kaunas", locative_case_name="Kaune")
        JobOffer.objects.create(
            title="Komandos asistentas (-ė)",
            category="Administravimas/darbų sauga",
            company="Įmonės pavadinimas A",
            salary="1500-1900",
            salary_period="€/mėn.",
            salary_calculation="Neatskaičius mokesčių",
            pay_keyword="",
            gross_pay=None,
            net_pay=None,
            gross_pay_from="1500.00",
            gross_pay_to="1900.00",
            net_pay_from="999.00",
            net_pay_to="1201.00",
            location="Vilniuje",
            job_link="https://...",
            image_link="https://...",
            image_width=100,
            image_height=24,
            offer_upload_date="prieš 8 val.",
            source_link="cvbankas",
        )
        JobOffer.objects.create(
            title="TEISĖS PSICHOLOGAS (-Ė)",
            category="Valstybinis/viešasis administravimas",
            company="Įmonės pavadinimas B",
            salary="1719-1900",
            salary_period="€/mėn.",
            salary_calculation="Neatskaičius mokesčių",
            pay_keyword="",
            gross_pay=None,
            net_pay=None,
            gross_pay_from="1719.00",
            gross_pay_to="1900.00",
            net_pay_from="1110.00",
            net_pay_to="1201.00",
            location="Kaune",
            job_link="https://...",
            image_link="https://...",
            image_width=100,
            image_height=30,
            offer_upload_date="prieš 21 d.",
            source_link="cvbankas",
        )

    def test_home_page_view_with_no_filters(self):
        request = RequestFactory().get(
            "/", {"title": "", "category": "", "location": ""}
        )
        view = HomePageView()
        view.setup(request)

        qs = view.get_queryset()
        self.assertQuerysetEqual(qs, JobOffer.objects.all())

    def test_home_page_view_with_title_filter(self):
        title = "TEISĖS PSICHOLOGAS (-Ė)"
        request = RequestFactory().get(
            "/", {"title": title, "category": "", "location": ""}
        )
        view = HomePageView()
        view.setup(request)

        qs = view.get_queryset()
        expected_job_offer = JobOffer.objects.get(title=title)

        self.assertQuerysetEqual(qs, [expected_job_offer])

    def test_home_page_view_with_invalid_title_filter(self):
        request = RequestFactory().get(
            "/", {"title": "NonExistingName", "category": "", "location": ""}
        )
        view = HomePageView()
        view.setup(request)

        qs = view.get_queryset()
        self.assertQuerysetEqual(qs, [])

    def test_home_page_view_with_location_filter(self):
        request = RequestFactory().get(
            "/", {"title": "", "category": "", "location": "Kaunas"}
        )
        view = HomePageView()
        view.setup(request)

        qs = view.get_queryset()
        expected_job_offer = JobOffer.objects.get(location="Kaune")

        self.assertQuerysetEqual(qs, [expected_job_offer])

    def test_home_page_view_with_invalid_location_filter(self):
        request = RequestFactory().get(
            "/", {"title": "", "category": "", "location": "NonExistingCity"}
        )
        view = HomePageView()
        view.setup(request)

        qs = view.get_queryset()

        self.assertQuerysetEqual(qs, [])

    def test_home_page_view_with_category_filter(self):
        category = "Administravimas/darbų sauga"
        request = RequestFactory().get(
            "/", {"title": "", "category": category, "location": ""}
        )
        view = HomePageView()
        view.setup(request)

        qs = view.get_queryset()
        expected_job_offer = JobOffer.objects.get(category=category)

        self.assertQuerysetEqual(qs, [expected_job_offer])

    def test_home_page_view_with_invalid_category_filter(self):
        request = RequestFactory().get(
            "/", {"title": "", "category": "NonExistingCategory", "location": ""}
        )
        view = HomePageView()
        view.setup(request)

        qs = view.get_queryset()

        self.assertQuerysetEqual(qs, [])

    def test_home_page_view_with_multiple_filters(self):
        category = "Valstybinis/viešasis administravimas"
        request = RequestFactory().get(
            "/", {"title": "TEISĖS PSIC", "category": category, "location": "Kaunas"}
        )
        view = HomePageView()
        view.setup(request)

        qs = view.get_queryset()
        expected_job_offer = JobOffer.objects.get(
            title="TEISĖS PSICHOLOGAS (-Ė)", category=category, location="Kaune"
        )

        self.assertQuerysetEqual(qs, [expected_job_offer])
