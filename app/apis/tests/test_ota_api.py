from ..serializers import OTASerializer
from enquiry.models import OTA

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

OTA_URL = reverse("ota-list")


class PublicOTAAPITestCase(APITestCase):
    """Test the publically available OTA API"""

    def test_login_always_required(self):

        res = self.client.get(OTA_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


def ota_detail_url(pk):
    return reverse("ota-detail", args=[pk])


def sample_ota(name, **kwargs):
    """Create and return a sample OTA object"""

    defaults = {
        "contact_person": "Super Saiyan",
        "contact_number": "9988776655",
        "contact_email": "goku@dbz.com"
    }

    if kwargs:
        defaults.update(kwargs)

    return OTA.objects.create(name=name, **defaults)


class PrivateOTAAPITestCase(APITestCase):
    """Test the OTA API available to authorized users"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test@s3-infosoft.com", "django123"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_all_otas(self):

        sample_ota(name="OTA1")
        sample_ota(name='OTA2')
        sample_ota(name='OTA3')

        res = self.client.get(OTA_URL)

        otas = OTA.objects.all()
        serializer = OTASerializer(otas, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_ota(self):
        payload = {"name": "Trivago",
                   "contact_person": "Manager",
                   "contact_number": "9988776655",
                   "contact_email": "mynameis@slimshady.com"}

        res = self.client.post(OTA_URL, data=payload)
        instance = OTA.objects.first()
        serializer = OTASerializer(instance)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data["name"], payload["name"])
        self.assertEqual(serializer.data["contact_person"],
                         payload["contact_person"])
        self.assertEqual(serializer.data["contact_number"],
                         payload["contact_number"])
        self.assertEqual(serializer.data["contact_email"],
                         payload["contact_email"])

    def test_delete_ota(self):
        sample_ota("Trivago")
        sample_ota("Booking")
        obj = sample_ota("GoIbibo")
        sample_ota("MMT")

        self.assertEqual(OTA.objects.count(), 4)

        res = self.client.delete(ota_detail_url(obj.pk))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OTA.objects.count(), 3)

    def test_update_using_put(self):
        payload_before = {"name": "Trivago",
                          "contact_person": "Developer",
                          "contact_number": "9988776655",
                          "contact_email": "mynameis@slimshady.com"}
        obj = OTA.objects.create(**payload_before)

        payload_update = {"name": "Trivago",
                          "contact_person": "Manager",
                          "contact_number": "Mr. Manager",
                          "contact_email": "mynameis@slimshady.com"}

        res = self.client.put(ota_detail_url(obj.pk), data=payload_update)
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
                          "contact_person": "Developer",
                          "contact_number": "9988776655",
                          "contact_email": "mynameis@slimshady.com"}

        obj = OTA.objects.create(**payload_before)

        payload_update = {"name": "MMT",
                          "contact_number": "9988776644"}

        res = self.client.patch(ota_detail_url(obj.pk), payload_update)
        obj.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(obj.name, payload_before["name"])
        self.assertNotEqual(obj.contact_number,
                            payload_before["contact_number"])
        self.assertEqual(obj.name, payload_update["name"])
        self.assertEqual(obj.contact_number, payload_update["contact_number"])
