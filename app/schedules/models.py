from enquiry.models import OTA

from django.conf import settings
from django.db import models


class Schedule(models.Model):
    STATUS = (
        ("PENDING", "Pending"),
        ("EXECUTING", "Executing"),
        ("FINISHED", "Finished"),
        ("FAILED", "Failed"),
    )

    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    property_name = models.CharField(max_length=150, blank=True,
                                     null=True)
    ota_name = models.ForeignKey(OTA, on_delete=models.CASCADE)
    check_in_date = models.DateTimeField(blank=True, null=True)
    check_out_date = models.DateTimeField(blank=True, null=True)
    listing_position_number = models.PositiveIntegerField(blank=True,
                                                          null=True)
    room_category_and_rates = models.TextField(max_length=200,
                                               blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True,
                                   db_index=True)
    status = models.CharField(choices=STATUS, max_length=10,
                              blank=True, null=True,
                              default="PENDING", db_index=True)
    comments = models.TextField(blank=True, null=True)

    class Meta:
        ordering = "-id",

    def __str__(self):
        return self.ota_name.name
