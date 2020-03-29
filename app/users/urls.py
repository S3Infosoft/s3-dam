from . import views

from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

password_urls = [
    path("change/", views.PasswordChangeView.as_view(),
         name="password_change"),
    path("reset/done/", auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path("reset/complete/", auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
    path("new/<uidb64>/<token>/",
         views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path("set/", views.UserPasswordSet.as_view(), name="password_set"),
    path("reset/", views.PasswordResetView.as_view(),
         name="password_reset"),
]

urlpatterns = [
    path("global-settings/", views.GlobalInfoDetailUpdate.as_view(),
         name="global_settings"),
    path("profile/", views.ProfileDetailUpdate.as_view(), name="profile"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("password/", include(password_urls)),
    path("dashboard/", views.index, name="index"),
    path("", RedirectView.as_view(url="/dashboard/", permanent=True)),
]
