from ..serializers import PartnerSerializer
from enquiry.models import Partner

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

PARTNER_URL = reverse("partner-list")


class PublicPartnerAPITestCase(APITestCase):
    """Test the publically available Partner API"""

    def test_login_always_required(self):

        res = self.client.get(PARTNER_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


def partner_detail_url(pk):
    return reverse("partner-detail", args=[pk])


def sample_partner(name, **kwargs):
    """Create and return a sample Partner object"""

    defaults = {
        "partner_type": "TRAVEL_AGENT",
        "contact_person": "Super Saiyan",
        "contact_number": "9988776655",
        "contact_email": "goku@dbz.com"
    }

    if kwargs:
        defaults.update(kwargs)

    return Partner.objects.create(name=name, **defaults)


class PrivatePartnerAPITestCase(APITestCase):
    """Test the Partner API available to authorized users"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test@s3-infosoft.com", "django123"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_all_partners(self):

        sample_partner(name="Partner1")
        sample_partner(name='Partner2')
        sample_partner(name='Partner3')

        res = self.client.get(PARTNER_URL)

        partners = Partner.objects.all()
        serializer = PartnerSerializer(partners, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_partner(self):
        payload = {"name": "Trivago",
                   "partner_type": "TRAVEL_AGENT",
                   "contact_person": "Manager",
                   "contact_number": "9988776655",
                   "contact_email": "mynameis@slimshady.com"}

        res = self.client.post(PARTNER_URL, data=payload)
        instance = Partner.objects.first()
        serializer = PartnerSerializer(instance)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data["name"], payload["name"])
        self.assertEqual(serializer.data["contact_person"],
                         payload["contact_person"])
        self.assertEqual(serializer.data["contact_number"],
                         payload["contact_number"])
        self.assertEqual(serializer.data["contact_email"],
                         payload["contact_email"])

    def test_delete_partner(self):
        sample_partner("Trivago")
        sample_partner("Booking")
        obj = sample_partner("GoIbibo")
        sample_partner("MMT")

        self.assertEqual(Partner.objects.count(), 4)

        res = self.client.delete(partner_detail_url(obj.pk))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Partner.objects.count(), 3)

    def test_update_using_put(self):
        payload_before = {"name": "Trivago",
                          "partner_type": "TRAVEL_AGENT",
                          "contact_person": "Developer",
                          "contact_number": "9988776655",
                          "contact_email": "mynameis@slimshady.com"}
        obj = Partner.objects.create(**payload_before)

        payload_update = {"name": "Trivago",
                          "partner_type": "TRAVEL_AGENT",
                          "contact_person": "Manager",
                          "contact_number": "9988776644",
                          "contact_email": "mynameis@slimshady.com"}

        res = self.client.put(partner_detail_url(obj.pk), data=payload_update)
        obj.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(obj.contact_person,
                            payload_before["contact_person"])
        self.assertNotEqual(obj.contact_number,
                            payload_before["contact_number"])
        self.assertEqual(obj.name, payload_before["name"])
        self.assertEqual(obj.contact_email, payload_before["contact_email"])
        self.assertEqual(obj.contact_person, payload_update["contact_person"])
        self.assertEqual(obj.contact_number, payload_update["contact_number"])

    def test_update_using_patch(self):
        payload_before = {"name": "Trivago",
                          "partner_type": "TRAVEL_AGENT",
                          "contact_person": "Developer",
                          "contact_number": "9988776655",
                          "contact_email": "mynameis@slimshady.com"}

        obj = Partner.objects.create(**payload_before)

        payload_update = {"name": "MMT",
                          "contact_number": "9988776644"}

        res = self.client.patch(partner_detail_url(obj.pk), payload_update)
        obj.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(obj.name, payload_before["name"])
        self.assertNotEqual(obj.contact_number,
                            payload_before["contact_number"])
        self.assertEqual(obj.name, payload_update["name"])
        self.assertEqual(obj.contact_number, payload_update["contact_number"])
