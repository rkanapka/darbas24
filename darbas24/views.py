from django.views import generic

from scraper.models import JobOffers


class HomePageView(generic.ListView):
    paginate_by = 20
    template_name = "home.html"

    context_object_name = (
        "offers"  # assign "JobOffers" object list to the object "offers"
    )

    def get_queryset(self):  # pass news objects as queryset for listview
        return JobOffers.objects.all()
