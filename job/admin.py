from django.contrib import admin

from .models import JobCategory, JobCity


class CityAdmin(admin.ModelAdmin):
    list_display = ("name",)


class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(JobCity, CityAdmin)
admin.site.register(JobCategory, JobCategoryAdmin)
