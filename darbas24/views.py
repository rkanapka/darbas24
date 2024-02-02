from django.db.models import Q
from django.views import generic

from job.models import JobCategory, JobCity, JobOffer


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
            return JobOffer.objects.filter(job_search_filter).order_by("id")
        return JobOffer.objects.all().order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cities = JobCity.objects.all()
        job_categories = JobCategory.objects.all()

        context["cities_list"] = cities
        context["job_categories_list"] = job_categories

        return context

    def build_search_filter(self, query_title, query_location, query_category):
        job_search_filter = Q(title__icontains=query_title)

        if query_location:
            locative_city = self.get_locative_case_of_city(query_location)
            job_search_filter &= Q(location=locative_city)

        if query_category:
            job_search_filter &= Q(category=query_category)
        return job_search_filter

    def get_locative_case_of_city(self, location_query):
        try:
            city = JobCity.objects.get(name=location_query)
            return city.locative_case_name
        except JobCity.DoesNotExist:
            return location_query
