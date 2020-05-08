from django.urls import path
from . import views


urlpatterns = [
    path("uploadPhoto", views.uploadPhoto, name="uploadPhoto"),
    path("uploadDocument/", views.uploadDocument, name="uploadDocument"),
]
