from ..serializers import ReviewSerializer
from enquiry.models import Review

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

REVIEW_URL = reverse("review-list")


class PublicReviewAPITestCase(APITestCase):
    """Test the publically available Review API"""
    def test_login_always_required(self):

        res = self.client.get(REVIEW_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


def review_detail_url(pk):
    return reverse("review-detail", args=[pk])


def sample_review(headline, **kwargs):
    """Create and return a sample Review object"""

    defaults = {
        "source": "Khhoofiya",
        "rating": 4,
        "description": "Its just a test, no need.",
        "action": "packup",
    }

    if kwargs:
        defaults.update(kwargs)

    return Review.objects.create(headline=headline, **defaults)


class PrivateReviewAPITestCase(APITestCase):
    """Test the Review API available to authorized users"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test@s3-infosoft.com", "django123"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_all_reviews(self):

        sample_review(headline="REVIEW1")
        sample_review(headline='REVIEW2')
        sample_review(headline='REVIEW3')

        res = self.client.get(REVIEW_URL)

        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_review(self):
        payload = {"headline": "This is headline",
                   "source": "Top Secret",
                   "rating": "5.0",
                   "description": "Leave it blank",
                   "action": "Packup"}

        res = self.client.post(REVIEW_URL, data=payload)
        instance = Review.objects.all()[0]
        serializer = ReviewSerializer(instance)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data["headline"], payload["headline"])
        self.assertEqual(serializer.data["source"], payload["source"])
        self.assertEqual(serializer.data["rating"], float(payload["rating"]))
        self.assertEqual(serializer.data["description"],
                         payload["description"])
        self.assertEqual(serializer.data["action"], payload["action"])

    def test_delete_review(self):
        sample_review("Trivago")
        sample_review("Booking")
        obj = sample_review("GoIbibo")
        sample_review("MMT")

        self.assertEqual(Review.objects.count(), 4)

        res = self.client.delete(review_detail_url(obj.pk))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 3)

    def test_update_using_put(self):
        payload_before = {"headline": "This is headline",
                          "source": "Top Secret",
                          "rating": "5.0",
                          "description": "Leave it blank",
                          "action": "Packup"}
        obj = Review.objects.create(**payload_before)

        payload_update = {"headline": "With great power, become lazy",
                          "source": "Open Source",
                          "rating": "5.0",
                          "description": "Leave it blank",
                          "action": "Cut it!!"}

        res = self.client.put(review_detail_url(obj.pk), data=payload_update)
        obj.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(obj.headline,
                            payload_before["headline"])
        self.assertNotEqual(obj.source, payload_before["source"])
        self.assertNotEqual(obj.action, payload_before["action"])
        self.assertEqual(obj.action, payload_update["action"])
        self.assertEqual(obj.rating, float(payload_before["rating"]))
        self.assertEqual(obj.description, payload_update["description"])
        self.assertEqual(obj.source, payload_update["source"])

    def test_update_using_patch(self):
        payload_before = {"headline": "This is headline",
                          "source": "Top Secret",
                          "rating": "5.0",
                          "description": "Leave it blank",
                          "action": "Packup"}

        obj = Review.objects.create(**payload_before)

        payload_update = {"action": "Cut it!!",
                          "source": "Slim Shady"}

        res = self.client.patch(review_detail_url(obj.pk), payload_update)
        obj.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(obj.action, payload_before["action"])
        self.assertNotEqual(obj.source, payload_before["source"])
        self.assertEqual(obj.action, payload_update["action"])
        self.assertEqual(obj.source, payload_update["source"])
