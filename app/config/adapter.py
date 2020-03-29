from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model


class CustomSocialAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if user.id:
            return None
        try:
            user = get_user_model().objects.get(email=user.email)
            sociallogin.connect(request, user)
        except get_user_model().DoesNotExist:
            pass
