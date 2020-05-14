from . import serializers, mixins
from users.models import GlobalInfo

from django.urls import reverse
from django.core.cache import cache

from rest_framework import generics, views, status
from rest_framework.response import Response

from easyaudit.models import CRUDEvent


class GlobalSettingsAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.GlobalInfoSerializer

    def get_object(self):
        return GlobalInfo.objects.first()


class ActivityListAPIView(generics.ListAPIView):
    serializer_class = serializers.CRUDEventSerializer
    queryset = CRUDEvent.objects.all()
