from random import randint

from django.db.models import Count, F, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from job.models import JobOffer


class InsightsView(TemplateView):
    template_name = "insights.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def job_offers_count_by_category_chart(request):
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


def job_offers_by_salary_range_chart(request):
    labels, data, colors = [], [], []
    pay_range_start, pay_range_end = 0, 0
    salary_range_query = Q(avg_salary__gte=pay_range_start) & Q(
        avg_salary__lt=pay_range_end
    )
    single_salary_query = Q(net_pay__gte=pay_range_start) & Q(net_pay__lt=pay_range_end)
    for pay_range_start in range(0, 6500, 500):
        pay_range_end = pay_range_start + 500
        job_offers = JobOffer.objects.annotate(
            avg_salary=F("net_pay_from") + F("net_pay_to") / 2
        ).filter(salary_range_query | single_salary_query)

        labels.append(f"{pay_range_start}-{pay_range_end}")
        data.append(len(job_offers))
        colors.append(generate_random_rgb())

    job_offers_over_limit = JobOffer.objects.annotate(
        avg_salary=F("net_pay_from") + F("net_pay_to") / 2
    ).filter(Q(net_pay__gte=pay_range_end) | Q(avg_salary__gte=pay_range_end))
    labels.append(f"{pay_range_end} <=")
    data.append(len(job_offers_over_limit))
    colors.append(generate_random_rgb())
    return JsonResponse(data={"labels": labels, "data": data, "colors": colors})


def generate_random_rgb(opacity=0.6):
    r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
    return f"rgba({r}, {g}, {b}, {opacity})"
