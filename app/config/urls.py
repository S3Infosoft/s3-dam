from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
import debug_toolbar

###### photogue and sitemap ################
from photologue.views import GalleryListView
from photologue.views import PhotoListView
from photologue.sitemaps import GallerySitemap, PhotoSitemap
from django.contrib.sitemaps.views import sitemap

###########################################

sitemaps = {"photologue_galleries": GallerySitemap, "photologue_photos": PhotoSitemap}

urlpatterns = [
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("photologue", include("photologue.urls", namespace="photologue")),
    path("photolist", PhotoListView.as_view(), name="photo"),
    path("gallerylist", GalleryListView.as_view(paginate_by=5), name="gallery"),
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("api/v1/", include("apis.urls")),
    path("", include("users.urls")),
    path("asset/", include("asset.urls")),
    path("__debug__", include(debug_toolbar.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
