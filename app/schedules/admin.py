from . import models
from django.contrib import admin


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = "ota_name", "creator", "property_name", "created", "status",
    list_filter = "ota_name", "status", "created",
    list_editable = "status",
    list_per_page = 25
