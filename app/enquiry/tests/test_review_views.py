from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Review
from ..forms import ReviewForm

REVIEW_LIST_URL = reverse("enquiry:review")


def review_detail_url(pk):
    return reverse("enquiry:review_detail", args=[pk])


class ReviewListViewTestCase(TestCase):

    def test_redirect_to_login_for_unauthenticated_user(self):

        res = self.client.get(REVIEW_LIST_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res,
                             reverse("login") + "?next=" + REVIEW_LIST_URL)

    def test_page_loads_for_authenticated_users(self):

        user = get_user_model().objects.create_user("test@s3-infosoft.com",
                                                    "django123")
        self.client.force_login(user)

        res = self.client.get(REVIEW_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "enquiry/review_list.html")


class ReviewDetailViewTestCaseUnAuth(TestCase):

    def test_redirect_to_login_if_unauthenticated(self):
        review = Review.objects.create(headline="HEADLINE",
                                       source="Source",
                                       rating=4.0,
                                       description="Description",
                                       action="Action")

        res = self.client.get(review_detail_url(review.pk))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "{}?next={}".format(
            reverse("login"),
            review_detail_url(review.pk)
        ))


class ReviewDetailViewTestCaseAuth(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user("test@test.com",
                                                         "django123")
        self.client.force_login(self.user)

        self.obj = Review.objects.create(headline="HEADLINE",
                                         source="Source",
                                         rating=4.0,
                                         description="Description",
                                         action="Action")

    def test_page_loads_successfully(self):
        res = self.client.get(review_detail_url(self.obj.pk))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "enquiry/review_detail.html")

    def test_page_renders_with_correct_context(self):
        res = self.client.get(review_detail_url(self.obj.pk))

        self.assertEqual(res.context["title"], self.obj.headline)
        self.assertIsInstance(res.context["form"], ReviewForm)

    def test_get_absolute_url_works_correctly(self):
        res1 = self.client.get(review_detail_url(self.obj.pk))
        res2 = self.client.get(self.obj.get_absolute_url())

        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res1.request["PATH_INFO"], res2.request["PATH_INFO"])
