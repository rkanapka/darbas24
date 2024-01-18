from django.contrib import admin

from .models import City, JobCategory


class CityAdmin(admin.ModelAdmin):
    list_display = ("name",)


class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(City, CityAdmin)
admin.site.register(JobCategory, JobCategoryAdmin)
