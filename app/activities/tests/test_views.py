from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.cache import cache

from ..forms import ReportForm, ReportEmailForm
from enquiry.models import OTA, Partner, Review

TODAY = datetime.now()

REPORT_URL = reverse("activity:report")
ACTIVITY_LOG_URL = reverse("activity:activity-log")


def pdf_url(model_name):
    return reverse("activity:pdf",
                   args=[TODAY.day, TODAY.month, TODAY.year,
                         TODAY.day, TODAY.month, TODAY.year,
                         model_name])


def csv_url(model_name):
    return reverse("activity:csv",
                   args=[TODAY.day, TODAY.month, TODAY.year,
                         TODAY.day, TODAY.month, TODAY.year,
                         model_name])


def email_url(model_name):
    return reverse("activity:report_email",
                   args=[TODAY.day, TODAY.month, TODAY.year,
                         TODAY.day, TODAY.month, TODAY.year,
                         model_name])


class TestForUnauthenticated(TestCase):
    """Test for the views on unauthenticated visits"""

    def test_activity_log_redirects_to_login(self):
        res = self.client.get(ACTIVITY_LOG_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "{}?next={}".format(
            reverse("login"),
            ACTIVITY_LOG_URL
        ))

    def test_export_csv_redirects_to_login(self):
        res = self.client.get(csv_url("OTA"))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "{}?next={}".format(
            reverse("login"),
            csv_url("OTA")
        ))

    def test_export_pdf_redirects_to_login(self):
        res = self.client.get(pdf_url("OTA"))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "{}?next={}".format(
            reverse("login"),
            pdf_url("OTA")
        ))

    def test_export_report_redirects_to_login(self):
        res = self.client.get(REPORT_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "{}?next={}".format(
            reverse("login"),
            REPORT_URL
        ))

    def test_export_email_report_redirects_to_login(self):
        res = self.client.get(email_url("OTA"))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "{}?next={}".format(
            reverse("login"),
            email_url("OTA")
        ))


class TestCaseWithUserLogged(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user(
            "test@test.com", "django123"
        )
        self.client.force_login(user)


class TestActitvityLog(TestCaseWithUserLogged):
    """Test for views on authenticated visits"""

    def test_activity_log_loads_successfully_for_authenticated(self):

        res = self.client.get(ACTIVITY_LOG_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "activities/activity_log.html")


class TestReportView(TestCaseWithUserLogged):
    """Tests for generate_report view"""

    def test_report_page_loads_successfully(self):
        res = self.client.get(REPORT_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "activities/report.html")

    def test_report_page_contains_correct_forms(self):
        res = self.client.get(REPORT_URL)

        self.assertIsInstance(res.context["form"], ReportForm)
        self.assertIsInstance(res.context["email_form"],
                              ReportEmailForm)


class TestPDFGeneration(TestCaseWithUserLogged):

    def setUp(self):
        super(TestPDFGeneration, self).setUp()
        self.cache_format = "{}-{}-{}"

    def test_pdf_is_generated_for_ota(self):
        OTA.objects.create(name="OTA1", contact_email="contact@email.com",
                           contact_number="1234567890", contact_person="Mr. X")
        cache.clear()
        res = self.client.get(pdf_url('OTA'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["title"], "OTA")

    def test_pdf_is_generated_for_partner(self):
        Partner.objects.create(name="Partner1", partner_type="CORPORATE",
                               contact_person="Mr. X", contact_number="12345",
                               contact_email="contact@email.com")
        cache.clear()
        res = self.client.get(pdf_url('PARTNER'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["title"], "PARTNER")

    def test_pdf_is_generated_for_review(self):
        Review.objects.create(headline="REVIEW", source="Source", rating=4.0,
                              action="Action Taken")
        cache.clear()
        res = self.client.get(pdf_url('REVIEW'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["title"], "REVIEW")

    def test_pdf_is_generated_for_ota_from_cache(self):
        OTA.objects.create(name="OTA1", contact_email="contact@email.com",
                           contact_number="1234567890", contact_person="Mr. X")
        cache.set(self.cache_format.format("OTA", TODAY.date(), TODAY.date()),
                  OTA.objects.all())

        res = self.client.get(pdf_url('OTA'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["title"], "OTA")

    def test_pdf_is_generated_for_partner_from_cache(self):
        Partner.objects.create(name="Partner1", partner_type="CORPORATE",
                               contact_person="Mr. X", contact_number="12345",
                               contact_email="contact@email.com")
        cache.set(
            self.cache_format.format("PARTNER", TODAY.date(), TODAY.date()),
            Partner.objects.all()
        )
        res = self.client.get(pdf_url('PARTNER'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["title"], "PARTNER")

    def test_pdf_is_generated_for_review_from_cache(self):
        Review.objects.create(headline="REVIEW", source="Source", rating=4.0,
                              action="Action Taken")
        cache.set(
            self.cache_format.format("REVIEW", TODAY.date(), TODAY.date()),
            Review.objects.all()
        )
        res = self.client.get(pdf_url('REVIEW'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context["title"], "REVIEW")


class TestCSVGeneration(TestCaseWithUserLogged):
    def setUp(self):
        super(TestCSVGeneration, self).setUp()
        self.cache_format = "{}-{}-{}"

    def test_csv_is_generated_for_ota(self):
        OTA.objects.create(name="OTA1", contact_email="contact@email.com",
                           contact_number="1234567890", contact_person="Mr. X")

        res = self.client.get(csv_url('OTA'))

        self.assertEqual(res.status_code, 200)

    def test_csv_is_generated_for_partner(self):
        Partner.objects.create(name="Partner1", partner_type="CORPORATE",
                               contact_person="Mr. X", contact_number="12345",
                               contact_email="contact@email.com")

        res = self.client.get(csv_url('PARTNER'))

        self.assertEqual(res.status_code, 200)

    def test_csv_is_generated_for_review(self):
        Review.objects.create(headline="REVIEW", source="Source", rating=4.0,
                              action="Action Taken")
        res = self.client.get(csv_url('REVIEW'))

        self.assertEqual(res.status_code, 200)

    def test_csv_is_generated_for_ota_from_cache(self):
        OTA.objects.create(name="OTA1", contact_email="contact@email.com",
                           contact_number="1234567890", contact_person="Mr. X")
        cache.set(self.cache_format.format("OTA", TODAY.date(), TODAY.date()),
                  OTA.objects.all())
        res = self.client.get(csv_url('OTA'))

        self.assertEqual(res.status_code, 200)

    def test_csv_is_generated_for_partner_from_cache(self):
        Partner.objects.create(name="Partner1", partner_type="CORPORATE",
                               contact_person="Mr. X", contact_number="12345",
                               contact_email="contact@email.com")
        cache.set(
            self.cache_format.format("PARTNER", TODAY.date(), TODAY.date()),
            Partner.objects.all()
        )
        res = self.client.get(csv_url('PARTNER'))

        self.assertEqual(res.status_code, 200)

    def test_csv_is_generated_for_review_from_cache(self):
        Review.objects.create(headline="REVIEW", source="Source", rating=4.0,
                              action="Action Taken")
        cache.set(
            self.cache_format.format("REVIEW", TODAY.date(), TODAY.date()),
            Review.objects.all()
        )
        res = self.client.get(csv_url('REVIEW'))

        self.assertEqual(res.status_code, 200)
