from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Partner
from ..forms import PartnerForm

PARTNER_LIST_URL = reverse("enquiry:partner")


def partner_detail_url(pk):
    return reverse("enquiry:partner_detail", args=[pk])


class PartnerListViewTestCase(TestCase):

    def test_redirect_to_login_for_unauthenticated_user(self):

        res = self.client.get(PARTNER_LIST_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res,
                             reverse("login") + "?next=" + PARTNER_LIST_URL)

    def test_page_loads_for_authenticated_users(self):

        user = get_user_model().objects.create_user("test@s3-infosoft.com",
                                                    "django123")
        self.client.force_login(user)

        res = self.client.get(PARTNER_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "enquiry/partner_list.html")


class PartnerDetailViewTestCaseUnAuth(TestCase):

    def test_redirect_to_login_if_unauthenticated(self):
        partner = Partner.objects.create(name="Name",
                                         partner_type="TRAVEL_AGENT",
                                         contact_email="contact@email.partner",
                                         contact_number="1234556778",
                                         contact_person="Contact Person")

        res = self.client.get(partner_detail_url(partner.pk))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "{}?next={}".format(
            reverse("login"),
            partner_detail_url(partner.pk)
        ))


class PartnerDetailViewTestCaseAuth(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user("test@test.com",
                                                         "django123")
        self.client.force_login(self.user)

        self.obj = Partner.objects.create(name="Name",
                                          partner_type="TRAVEL_AGENT",
                                          contact_person="Contact Person",
                                          contact_number="2345567891",
                                          contact_email="contact@email.com")

    def test_page_loads_successfully(self):
        res = self.client.get(partner_detail_url(self.obj.pk))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "enquiry/partner_detail.html")

    def test_page_renders_with_correct_context(self):
        res = self.client.get(partner_detail_url(self.obj.pk))

        self.assertEqual(res.context["title"], self.obj.name)
        self.assertIsInstance(res.context["form"], PartnerForm)

    def test_get_absolute_url_works_correctly(self):
        res1 = self.client.get(partner_detail_url(self.obj.pk))
        res2 = self.client.get(self.obj.get_absolute_url())

        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res1.request["PATH_INFO"], res2.request["PATH_INFO"])
