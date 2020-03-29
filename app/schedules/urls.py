from . import views
from django.urls import path

app_name = "schedule"

urlpatterns = [
    path("new/", views.schedule, name="new"),
    path("completed/", views.display_schedule, name="completed"),
    path("uncomplete/", views.display_schedule, name="uncomplete"),
]
