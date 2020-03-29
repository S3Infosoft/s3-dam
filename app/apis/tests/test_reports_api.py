from .. import serializers
from enquiry.models import OTA, Partner, Review

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.cache import cache

from rest_framework import status
from rest_framework.test import APITestCase

import pytz
from datetime import datetime
from unittest import mock

REPORT_URL = reverse("api_report")
CURRENT_DATE = datetime(2019, 1, 1)


def create_model_instance(model, params: dict, **kwargs):

    default_time = {"year": 2019, "month": 1, "day": 1}
    if kwargs:
        default_time.update(kwargs)

    mocked_time = datetime(**default_time, tzinfo=pytz.utc)

    with mock.patch("django.utils.timezone.now",
                    mock.Mock(return_value=mocked_time)):
        model.objects.create(**params)


class TestPublicReportAPI(APITestCase):
    """Test unauthorised request to API"""

    def test_login_always_required(self):
        start_date = datetime(year=CURRENT_DATE.year,
                              month=CURRENT_DATE.month,
                              day=CURRENT_DATE.day)
        end_date = datetime(year=CURRENT_DATE.year,
                            month=CURRENT_DATE.month+2,
                            day=CURRENT_DATE.day)
        payload = {"start_date": start_date.date(),
                   "end_date": end_date.date(),
                   "enquiry_type": "OTA"}

        res = self.client.get(REPORT_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class TestPrivateReportAPI(APITestCase):
    """Test authorized API request"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "abhie@infosoft.com", "django123"
        )
        self.client.force_login(self.user)

    def test_access_to_logged_in_user(self):
        payload = {"start_date": CURRENT_DATE.date(),
                   "end_date": CURRENT_DATE.date(),
                   "enquiry_type": "OTA"}

        res = self.client.get(REPORT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_error_on_incomplete_data(self):
        payload = {"start_date": CURRENT_DATE.date(),
                   "enquiry_date": "OTA"}

        res = self.client.get(REPORT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ota_report_is_generated_from_duration_given(self):
        model_payload = {
            "contact_person": "Super Saiyan",
            "contact_number": "9988776655",
            "contact_email": "goku@dbz.com"
        }

        for i in range(4):
            curr_day = CURRENT_DATE.day
            model_payload["name"] = f"I am Number {i}"
            create_model_instance(OTA, params=model_payload, day=curr_day+i)

        for i in range(1, 4):
            curr_month = CURRENT_DATE.month
            model_payload["name"] = f"Terminator {i}"
            create_model_instance(OTA,
                                  params=model_payload,
                                  month=curr_month+1)

        self.assertEqual(OTA.objects.count(), 7)

        all_otas = OTA.objects.order_by("registration")

        start_date = all_otas[2].registration.date()
        end_date = all_otas[6].registration.date()

        payload = {"start_date": start_date,
                   "end_date": end_date,
                   "enquiry_type": "OTA"}

        otas_expected = OTA.objects.filter(registration__date__gte=start_date,
                                           registration__date__lte=end_date)

        res = self.client.get(REPORT_URL, payload)
        serializer = serializers.OTASerializer(otas_expected, many=True)

        url_params = [start_date.day, start_date.month, start_date.year,
                      end_date.day, end_date.month, end_date.year,
                      "OTA"]

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["data"], serializer.data)
        self.assertEqual(res.data["start_date"], start_date)
        self.assertEqual(res.data["end_date"], end_date)
        self.assertEqual(res.data["enquiry_type"], "OTA")
        self.assertEqual(res.data["csv_url"], reverse("activity:csv",
                                                      args=url_params))
        self.assertEqual(res.data["pdf_url"], reverse("activity:pdf",
                                                      args=url_params))
        self.assertEqual(res.data["email_url"],
                         reverse("activity:report_email", args=url_params))

    def test_partner_report_is_generated_from_duration_given(self):
        model_payload = {
            "partner_type": "TRAVEL_AGENT",
            "contact_person": "Super Saiyan",
            "contact_number": "9988776655",
            "contact_email": "goku@dbz.com"
        }

        for i in range(4):
            curr_day = CURRENT_DATE.day
            model_payload["name"] = f"I am Number {i}"
            create_model_instance(Partner, params=model_payload,
                                  day=curr_day + i)

        for i in range(1, 4):
            curr_month = CURRENT_DATE.month
            model_payload["name"] = f"Terminator {i}"
            create_model_instance(Partner,
                                  params=model_payload,
                                  month=curr_month + 1)

        self.assertEqual(Partner.objects.count(), 7)

        all_partners = Partner.objects.order_by("created")

        start_date = all_partners[2].created.date()
        end_date = all_partners[6].created.date()

        payload = {"start_date": start_date,
                   "end_date": end_date,
                   "enquiry_type": "PARTNER"}

        partners_expected = Partner.objects.filter(
            created__date__gte=start_date,
            created__date__lte=end_date
        )

        res = self.client.get(REPORT_URL, payload)
        serializer = serializers.PartnerSerializer(partners_expected,
                                                   many=True)

        url_params = [start_date.day, start_date.month, start_date.year,
                      end_date.day, end_date.month, end_date.year,
                      "PARTNER"]

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["data"], serializer.data)
        self.assertEqual(res.data["start_date"], start_date)
        self.assertEqual(res.data["end_date"], end_date)
        self.assertEqual(res.data["enquiry_type"], "PARTNER")
        self.assertEqual(res.data["csv_url"], reverse("activity:csv",
                                                      args=url_params))
        self.assertEqual(res.data["pdf_url"], reverse("activity:pdf",
                                                      args=url_params))
        self.assertEqual(res.data["email_url"],
                         reverse("activity:report_email", args=url_params))

    def test_review_report_is_generated_from_duration_given(self):
        model_payload = {
            "source": "Secret",
            "rating": 3.0,
            "description": "Don't need",
            "action": "JCB ki khudaai"
        }

        for i in range(4):
            curr_day = CURRENT_DATE.day
            model_payload["headline"] = f"I am Number {i}"
            create_model_instance(Review, params=model_payload, day=curr_day+i)

        for i in range(1, 4):
            curr_month = CURRENT_DATE.month
            model_payload["headline"] = f"Terminator {i}"
            create_model_instance(Review,
                                  params=model_payload,
                                  month=curr_month+1)

        self.assertEqual(Review.objects.count(), 7)

        all_reviews = Review.objects.order_by("created")

        start_date = all_reviews[2].created.date()
        end_date = all_reviews[6].created.date()

        payload = {"start_date": start_date,
                   "end_date": end_date,
                   "enquiry_type": "REVIEW"}

        reviews_expected = Review.objects.filter(created__date__gte=start_date,
                                                 created__date__lte=end_date)

        res = self.client.get(REPORT_URL, payload)
        serializer = serializers.ReviewSerializer(reviews_expected, many=True)

        url_params = [start_date.day, start_date.month, start_date.year,
                      end_date.day, end_date.month, end_date.year,
                      "REVIEW"]

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["data"], serializer.data)
        self.assertEqual(res.data["start_date"], start_date)
        self.assertEqual(res.data["end_date"], end_date)
        self.assertEqual(res.data["enquiry_type"], "REVIEW")
        self.assertEqual(res.data["csv_url"], reverse("activity:csv",
                                                      args=url_params))
        self.assertEqual(res.data["pdf_url"], reverse("activity:pdf",
                                                      args=url_params))
        self.assertEqual(res.data["email_url"],
                         reverse("activity:report_email", args=url_params))

    def test_ota_report_is_generated_from_duration_given_from_cache(self):
        model_payload = {
            "contact_person": "Super Saiyan",
            "contact_number": "9988776655",
            "contact_email": "goku@dbz.com"
        }

        for i in range(4):
            curr_day = CURRENT_DATE.day
            model_payload["name"] = f"I am Number {i}"
            create_model_instance(OTA, params=model_payload, day=curr_day+i)

        for i in range(1, 4):
            curr_month = CURRENT_DATE.month
            model_payload["name"] = f"Terminator {i}"
            create_model_instance(OTA,
                                  params=model_payload,
                                  month=curr_month+1)

        self.assertEqual(OTA.objects.count(), 7)

        all_otas = OTA.objects.order_by("registration")

        start_date = all_otas[2].registration.date()
        end_date = all_otas[6].registration.date()

        payload = {"start_date": start_date,
                   "end_date": end_date,
                   "enquiry_type": "OTA"}

        otas_expected = OTA.objects.filter(registration__date__gte=start_date,
                                           registration__date__lte=end_date)

        cache.set("{}-{}-{}".format("OTA", start_date, end_date),
                  otas_expected)

        res = self.client.get(REPORT_URL, payload)
        serializer = serializers.OTASerializer(otas_expected, many=True)

        url_params = [start_date.day, start_date.month, start_date.year,
                      end_date.day, end_date.month, end_date.year,
                      "OTA"]

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["data"], serializer.data)
        self.assertEqual(res.data["start_date"], start_date)
        self.assertEqual(res.data["end_date"], end_date)
        self.assertEqual(res.data["enquiry_type"], "OTA")
        self.assertEqual(res.data["csv_url"], reverse("activity:csv",
                                                      args=url_params))
        self.assertEqual(res.data["pdf_url"], reverse("activity:pdf",
                                                      args=url_params))
        self.assertEqual(res.data["email_url"],
                         reverse("activity:report_email", args=url_params))

    def test_partner_report_is_generated_from_duration_given_from_cache(self):
        model_payload = {
            "partner_type": "TRAVEL_AGENT",
            "contact_person": "Super Saiyan",
            "contact_number": "9988776655",
            "contact_email": "goku@dbz.com"
        }

        for i in range(4):
            curr_day = CURRENT_DATE.day
            model_payload["name"] = f"I am Number {i}"
            create_model_instance(Partner, params=model_payload,
                                  day=curr_day + i)

        for i in range(1, 4):
            curr_month = CURRENT_DATE.month
            model_payload["name"] = f"Terminator {i}"
            create_model_instance(Partner,
                                  params=model_payload,
                                  month=curr_month + 1)

        self.assertEqual(Partner.objects.count(), 7)

        all_partners = Partner.objects.order_by("created")

        start_date = all_partners[2].created.date()
        end_date = all_partners[6].created.date()

        payload = {"start_date": start_date,
                   "end_date": end_date,
                   "enquiry_type": "PARTNER"}

        partners_expected = Partner.objects.filter(
            created__date__gte=start_date,
            created__date__lte=end_date
        )

        cache.set("{}-{}-{}".format("PARTNER", start_date, end_date),
                  partners_expected)

        res = self.client.get(REPORT_URL, payload)
        serializer = serializers.PartnerSerializer(partners_expected,
                                                   many=True)

        url_params = [start_date.day, start_date.month, start_date.year,
                      end_date.day, end_date.month, end_date.year,
                      "PARTNER"]

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["data"], serializer.data)
        self.assertEqual(res.data["start_date"], start_date)
        self.assertEqual(res.data["end_date"], end_date)
        self.assertEqual(res.data["enquiry_type"], "PARTNER")
        self.assertEqual(res.data["csv_url"], reverse("activity:csv",
                                                      args=url_params))
        self.assertEqual(res.data["pdf_url"], reverse("activity:pdf",
                                                      args=url_params))
        self.assertEqual(res.data["email_url"],
                         reverse("activity:report_email", args=url_params))

    def test_review_report_is_generated_from_duration_given_from_cache(self):
        model_payload = {
            "source": "Secret",
            "rating": 3.0,
            "description": "Don't need",
            "action": "JCB ki khudaai"
        }

        for i in range(4):
            curr_day = CURRENT_DATE.day
            model_payload["headline"] = f"I am Number {i}"
            create_model_instance(Review, params=model_payload, day=curr_day+i)

        for i in range(1, 4):
            curr_month = CURRENT_DATE.month
            model_payload["headline"] = f"Terminator {i}"
            create_model_instance(Review,
                                  params=model_payload,
                                  month=curr_month+1)

        self.assertEqual(Review.objects.count(), 7)

        all_reviews = Review.objects.order_by("created")

        start_date = all_reviews[2].created.date()
        end_date = all_reviews[6].created.date()

        payload = {"start_date": start_date,
                   "end_date": end_date,
                   "enquiry_type": "REVIEW"}

        reviews_expected = Review.objects.filter(created__date__gte=start_date,
                                                 created__date__lte=end_date)

        cache.set("{}-{}-{}".format("REVIEW", start_date, end_date),
                  reviews_expected)

        res = self.client.get(REPORT_URL, payload)
        serializer = serializers.ReviewSerializer(reviews_expected, many=True)

        url_params = [start_date.day, start_date.month, start_date.year,
                      end_date.day, end_date.month, end_date.year,
                      "REVIEW"]

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["data"], serializer.data)
        self.assertEqual(res.data["start_date"], start_date)
        self.assertEqual(res.data["end_date"], end_date)
        self.assertEqual(res.data["enquiry_type"], "REVIEW")
        self.assertEqual(res.data["csv_url"], reverse("activity:csv",
                                                      args=url_params))
        self.assertEqual(res.data["pdf_url"], reverse("activity:pdf",
                                                      args=url_params))
        self.assertEqual(res.data["email_url"],
                         reverse("activity:report_email", args=url_params))
