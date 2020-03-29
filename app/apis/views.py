from . import serializers, mixins
from enquiry import models as enq_models
from schedules.models import Schedule
from users.models import GlobalInfo
from activities.forms import ReportForm

from django.urls import reverse
from django.core.cache import cache

from rest_framework import generics, views, status
from rest_framework.response import Response

from easyaudit.models import CRUDEvent


class GlobalSettingsAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.GlobalInfoSerializer

    def get_object(self):
        return GlobalInfo.objects.first()


class SchedulePendingListAPIView(generics.ListAPIView):
    serializer_class = serializers.ScheduleSerializer
    queryset = Schedule.objects.exclude(status__in=["FINISHED", "FAILED"])


class ScheduleFinishedListAPIView(generics.ListAPIView):
    serializer_class = serializers.ScheduleSerializer
    queryset = Schedule.objects.filter(status__in=["FINISHED", "FAILED"])


class ReportAPIView(views.APIView):

    @staticmethod
    def get(request):
        form = ReportForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            enquiry = cd["enquiry_type"]
            start_date = cd["start_date"]
            end_date = cd["end_date"]

            # keys to get data from cache
            key = f"{enquiry}-{start_date}-{end_date}"

            # get the data from cache if present
            queryset = cache.get(key)
            if queryset:
                if enquiry == "OTA":
                    serializer = serializers.OTASerializer(queryset, many=True)
                elif enquiry == "PARTNER":
                    serializer = serializers.PartnerSerializer(queryset,
                                                               many=True)
                else:
                    serializer = serializers.ReviewSerializer(queryset,
                                                              many=True)
            else:

                # Generating queryset and serializer on the
                # type of data requested
                # Serializer to send the data as json for Datatables.js
                if enquiry == "OTA":
                    queryset = enq_models.OTA.objects.filter(
                        registration__date__gte=start_date,
                        registration__date__lte=end_date,

                    )
                    serializer = serializers.OTASerializer(queryset,
                                                           many=True)
                elif enquiry == "PARTNER":
                    queryset = enq_models.Partner.objects.filter(
                        created__date__gte=start_date,
                        created__date__lte=end_date,
                    )
                    serializer = serializers.PartnerSerializer(queryset,
                                                               many=True)
                else:
                    queryset = enq_models.Review.objects.filter(
                        created__date__gte=start_date,
                        created__date__lte=end_date,
                    )
                    serializer = serializers.ReviewSerializer(queryset,
                                                              many=True)

                # set the queryset and serializer in cache
                cache.set(key, queryset)

            csv_url = reverse("activity:csv", args=[
                start_date.day, start_date.month, start_date.year,
                end_date.day, end_date.month, end_date.year,
                enquiry,
            ])

            pdf_url = reverse("activity:pdf", args=[
                start_date.day, start_date.month, start_date.year,
                end_date.day, end_date.month, end_date.year,
                enquiry,
            ])

            email_url = reverse("activity:report_email", args=[
                start_date.day, start_date.month, start_date.year,
                end_date.day, end_date.month, end_date.year,
                enquiry,
            ])

            return Response({"data": serializer.data,
                             "start_date": start_date,
                             "end_date": end_date,
                             "enquiry_type": enquiry,
                             "csv_url": csv_url,
                             "pdf_url": pdf_url,
                             "email_url": email_url}, status=200)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivityListAPIView(generics.ListAPIView):
    serializer_class = serializers.CRUDEventSerializer
    queryset = CRUDEvent.objects.all()


class OTAViewset(mixins.CRUDModelViewSetMixin):
    serializer_class = serializers.OTASerializer
    queryset = enq_models.OTA.objects.all()


class PartnerViewSet(mixins.CRUDModelViewSetMixin):
    serializer_class = serializers.PartnerSerializer
    queryset = enq_models.Partner.objects.all()


class ReviewViewSet(mixins.CRUDModelViewSetMixin):
    serializer_class = serializers.ReviewSerializer
    queryset = enq_models.Review.objects.all()
