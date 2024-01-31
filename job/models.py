from django.db import models


class JobOffer(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    salary = models.CharField(max_length=50)
    salary_period = models.CharField(max_length=25)
    salary_calculation = models.CharField(max_length=25)
    gross_pay = models.CharField(max_length=50, default="")
    net_pay = models.CharField(max_length=50, default="")
    location = models.CharField(max_length=50)
    job_link = models.CharField(max_length=2083, default="")
    image_link = models.CharField(max_length=2083, default="")
    image_width = models.SmallIntegerField()
    image_height = models.SmallIntegerField()
    offer_upload_date = models.CharField(max_length=50)
    source_link = models.CharField(max_length=30, default="", blank=True, null=True)

    @property
    def category_color(self):
        category = JobCategory.objects.get(name=self.category)
        return category.bg_color


class JobCity(models.Model):
    name = models.CharField(max_length=255)
    locative_case_name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return self.name


class JobCategory(models.Model):
    name = models.CharField(max_length=255)
    bg_color = models.CharField(max_length=50)
    cvbankas_url = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "catgories"

    def __str__(self):
        return self.name
