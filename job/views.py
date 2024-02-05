from random import randint

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from job.models import JobOffer


class InsightsView(TemplateView):
    template_name = "insights.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def population_chart(request):
    labels, data, colors = [], [], []

    queryset = (
        JobOffer.objects.values("category")
        .annotate(total=Count("category"))
        .order_by("total")
    )
    for entry in queryset:
        labels.append(entry["category"])
        data.append(entry["total"])
        colors.append(generate_random_rgb())

    return JsonResponse(data={"labels": labels, "data": data, "colors": colors})


def generate_random_rgb(opacity=0.6):
    r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
    return f"rgba({r}, {g}, {b}, {opacity})"
