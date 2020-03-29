from . import views
from django.urls import path

app_name = "activity"

urlpatterns = [
    path("csv/<int:s_day>/<int:s_month>/<int:s_year>/<int:e_day>/"
         "<int:e_month>/<int:e_year>/<str:model>/",
         views.export_csv, name="csv"),
    path("pdf/<int:s_day>/<int:s_month>/<int:s_year>/<int:e_day>/"
         "<int:e_month>/<int:e_year>/<str:model>/",
         views.export_pdf, name="pdf"),
    path("report/email/<int:s_day>/<int:s_month>/<int:s_year>/<int:e_day>/"
         "<int:e_month>/<int:e_year>/<str:model>/",
         views.send_report_email, name="report_email"),
    path("report/", views.generate_report, name="report"),
    path("log/", views.activity_log, name="activity-log")
]
