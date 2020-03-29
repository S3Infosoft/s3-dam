from . import models
from django.contrib import admin


@admin.register(models.OTA)
class OTAAdmin(admin.ModelAdmin):
    list_display = "name", "registration", "contact_person", "contact_number",\
                   "contact_email",
    search_fields = "name", "contact_person",


@admin.register(models.Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = "name", "partner_type", "created", "contact_person", \
                   "contact_number", "contact_email",
    search_fields = "name", "contact_person",


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = "headline_slim", "source_slim", "rating", "created",
    list_filter = "rating",
    search_fields = "headline",
    list_editable = "rating",

    @staticmethod
    def headline_slim(inst):
        return inst.headline[:70]

    @staticmethod
    def source_slim(inst):
        return inst.source[:70]
