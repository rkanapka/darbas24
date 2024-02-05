from random import randint

from django.db.models import Count, F, Q, Sum
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
        .order_by("-total")
    )
    for entry in queryset:
        labels.append(entry["category"])
        data.append(entry["total"])
        colors.append(generate_random_rgb())

    return JsonResponse(data={"labels": labels, "data": data, "colors": colors})


def job_categories_by_average_salary_chart(request):
    labels, data, colors = [], [], []
    salary_amount_to_ignore_offers = 10000
    jobs_with_pay_range = (
        JobOffer.objects.values("category")
        .filter(
            Q(net_pay_from__isnull=False)
            & Q(net_pay_from__lt=salary_amount_to_ignore_offers)
        )
        .annotate(
            net_pay_range_average=(Sum("net_pay_from") + Sum("net_pay_to"))
            / Count("category")
        )
    )
    jobs_with_single_pay = (
        JobOffer.objects.values("category")
        .filter(
            Q(net_pay__isnull=False) & Q(net_pay__lt=salary_amount_to_ignore_offers)
        )
        .annotate(net_pay_average=(Sum("net_pay") / Count("category")))
    )

    for job_with_pay_range in jobs_with_pay_range:
        for job_with_single_pay in jobs_with_single_pay:
            if job_with_pay_range["category"] == job_with_single_pay["category"]:
                job_with_pay_range["net_pay_range_average"] += job_with_single_pay[
                    "net_pay_average"
                ]
                job_with_pay_range["net_pay_range_average"] /= 2
                break
        labels.append(job_with_pay_range["category"])
        payment_amount = job_with_pay_range["net_pay_range_average"]
        data.append(f"{payment_amount:.2f}")
        colors.append(generate_random_rgb())
    data, labels = zip(*sorted(zip(data, labels)))
    return JsonResponse(data={"labels": labels, "data": data, "colors": colors})


def job_offers_by_salary_range_chart(request):
    labels, data, colors = [], [], []
    pay_range_start, pay_range_end = 0, 0

    for pay_range_start in range(0, 6500, 500):
        pay_range_end = pay_range_start + 500

        salary_range_query = Q(avg_salary__gte=pay_range_start) & Q(
            avg_salary__lt=pay_range_end
        )
        single_salary_query = Q(net_pay__gte=pay_range_start) & Q(
            net_pay__lt=pay_range_end
        )

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


def companies_with_most_offers_chart(request):
    labels, data, colors = [], [], []

    query_set = (
        JobOffer.objects.values("company")
        .annotate(total=Count("company"))
        .order_by("-total")[:10]
    )
    for entry in query_set:
        labels.append(entry["company"])
        data.append(entry["total"])
        colors.append(generate_random_rgb())

    return JsonResponse(data={"labels": labels, "data": data, "colors": colors})


def generate_random_rgb(opacity=0.6):
    r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
    return f"rgba({r}, {g}, {b}, {opacity})"
