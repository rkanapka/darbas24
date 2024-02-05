"""
URL configuration for darbas24 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from job.views import (
    InsightsView,
    job_categories_by_average_salary_chart,
    job_offers_by_salary_range_chart,
    job_offers_count_by_category_chart,
)

from .views import HomePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("insights/", InsightsView.as_view(), name="insights"),
    path(
        "offers-count-by-category-chart/",
        job_offers_count_by_category_chart,
        name="offers-count-by-category-chart",
    ),
    path(
        "job-categories-by-average-salary-chart/",
        job_categories_by_average_salary_chart,
        name="job-categories-by-average-salary-chart",
    ),
    path(
        "job-offers-by-salary-range-chart/",
        job_offers_by_salary_range_chart,
        name="job-offers-by-salary-range-chart",
    ),
]
