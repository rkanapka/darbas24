from django.db.models import Q
from django.views import generic

from scraper.models import City, JobCategory, JobOffers


class HomePageView(generic.ListView):
    paginate_by = 20
    template_name = "home.html"

    context_object_name = "offers"

    def get_queryset(self):
        query_title = self.request.GET.get("title")
        query_location = self.request.GET.get("location")
        query_category = self.request.GET.get("category")

        job_search_filter = self.build_search_filter(
            query_title, query_location, query_category
        )

        if query_title or query_location or query_category:
            return JobOffers.objects.filter(job_search_filter)
        return JobOffers.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cities = City.objects.all()
        job_categories = JobCategory.objects.all()

        context["cities_list"] = cities
        context["job_categories_list"] = job_categories

        return context

    def build_search_filter(self, query_title, query_location, query_category):
        job_search_filter = Q(title__icontains=query_title)

        if query_location:
            locative_city = self.transform_city_to_locative_case(query_location)
            job_search_filter &= Q(location=locative_city)

        if query_category:
            job_search_filter &= Q(category=query_category)
        return job_search_filter

    def transform_city_to_locative_case(self, location_query):
        city_mappings = {
            "Vilnius": "Vilniuje",
            "Kaunas": "Kaune",
            "Klaipėda": "Klaipėdoje",
            "Šiauliai": "Šiauliuose",
            "Panevėžys": "Panevėžyje",
            "Akmenė": "Akmėnėje",
            "Alytus": "Alytuje",
            "Anykščiai": "Anykščiuose",
            "Birštonas": "Birštone",
            "Biržai": "Biržuose",
            "Druskininkai": "Druskininkuose",
            "Elektrėnai": "Elektrėnuose",
            "Gargždai": "Gargžduose",
            "Ignalina": "Ignalinoje",
            "Jonava": "Jonavoje",
            "Joniškis": "Joniškyje",
            "Jurbarkas": "Jurbarkuose",
            "Kaišiadorys": "Kaišiadoryse",
            "Kalvarija": "Kalvarijoje",
            "Kazlų Rūda": "Kazlų Rūdoje",
            "Kėdainiai": "Kėdainiuose",
            "Kelmė": "Kelmėje",
            "Krekenava": "Krekenavoje",
            "Kretinga": "Kretingoje",
            "Kupiškis": "Kupiškyje",
            "Kuršėnai": "Kuršėnuose",
            "Lazdijai": "Lazdijuose",
            "Lentvaris": "Lentvaryje",
            "Marijampolė": "Marijampolėje",
            "Mažeikiai": "Mažeikiuose",
            "Molėtai": "Molėtuose",
            "Naujoji Akmenė": "Naujojoje Akmėnėje",
            "Nemenčinė": "Nemenčinėje",
            "Neringa": "Neringoje",
            "Pabradė": "Pabradėje",
            "Pagėgiai": "Pagėgiuose",
            "Pakruojis": "Pakruojoje",
            "Palanga": "Palangoje",
            "Pasvalys": "Pasvaliuose",
            "Plungė": "Plungėje",
            "Prienai": "Prienųose",
            "Radviliškis": "Radviliškyje",
            "Raseiniai": "Raseiniuose",
            "Rietavas": "Rietave",
            "Rokiškis": "Rokiškyje",
            "Šakiai": "Šakiuose",
            "Šalčininkai": "Šalčininkuose",
            "Šilalė": "Šilalėje",
            "Šilutė": "Šilutėje",
            "Širvintos": "Širvintuose",
            "Skuodas": "Skuode",
            "Švenčionys": "Švenčionyse",
            "Tauragė": "Tauragėje",
            "Telšiai": "Telšiuose",
            "Trakai": "Trakuose",
            "Ukmergė": "Ukmergėje",
            "Utena": "Utenoje",
            "Varėna": "Varėnoje",
            "Vievis": "Vievyje",
            "Vilkaviškis": "Vilkaviškyje",
            "Visaginas": "Visagine",
            "Zarasai": "Zarase",
            "Darbas namuose": "Namie",
            "Užsienis": "Užsienyje",
        }
        return city_mappings.get(location_query)
