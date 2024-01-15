from django.db import models


class JobOffers(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    salary = models.CharField(max_length=50)
    salary_period = models.CharField(max_length=25)
    salary_calculation = models.CharField(max_length=25)
    location = models.CharField(max_length=50)
    job_link = models.CharField(max_length=2083, default="", unique=True)
    image_link = models.CharField(max_length=2083, default="")
    image_width = models.SmallIntegerField()
    image_height = models.SmallIntegerField()
    source_link = models.CharField(max_length=30, default="", blank=True, null=True)
