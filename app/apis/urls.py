from . import views
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path(
        "global-settings/",
        views.GlobalSettingsAPIView.as_view(),
        name="api_global_settings",
    ),
    path("log/", views.ActivityListAPIView.as_view(), name="activity_log"),
    path("", include(router.urls)),
]
