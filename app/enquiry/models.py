from django.db import models
from django.urls import reverse


class OTA(models.Model):
    name = models.CharField(max_length=150)
    registration = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    contact_person = models.CharField(max_length=150)
    contact_number = models.CharField(max_length=15)
    contact_email = models.EmailField()

    class Meta:
        ordering = "-id",

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("enquiry:ota_detail", args=[self.id])


class Partner(models.Model):
    PARTNERS = (
        ("TRAVEL_AGENT", "Travel Agent"),
        ("DIGITAL_PARTNER", "Digital Partner"),
        ("CORPORATE", "Corporate"),
        ("TOUR_ORGANISER", "Tour Organiser"),
    )
    name = models.CharField(max_length=150)
    partner_type = models.CharField(choices=PARTNERS, max_length=30)
    contact_person = models.CharField(max_length=150)
    contact_number = models.CharField(max_length=15)
    contact_email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = "-id",

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("enquiry:partner_detail", args=[self.id])


class Review(models.Model):
    RATINGS = (
        (1.0, "Worst"),
        (2.0, "Poor"),
        (3.0, "Average"),
        (4.0, "Good"),
        (5.0, "Excellent"),
    )
    headline = models.CharField(max_length=250)
    source = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    rating = models.FloatField(choices=RATINGS)
    description = models.TextField()
    action = models.TextField()

    class Meta:
        ordering = "-id",

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse("enquiry:review_detail", args=[self.id])
