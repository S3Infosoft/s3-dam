from django.urls import path
from . import views
from photologue.views import GalleryListView
from photologue.views import PhotoListView


urlpatterns = [
    path("photolist", PhotoListView.as_view(), name="photo"),
    path("gallerylist", GalleryListView.as_view(paginate_by=5), name="gallery"),
    path("uploadPhoto", views.uploadPhoto, name="uploadPhoto"),
    path("uploadDocument/", views.uploadDocument, name="uploadDocument"),
]
