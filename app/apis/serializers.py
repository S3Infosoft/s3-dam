from enquiry import models as enq_models
from schedules.models import Schedule
from users.models import GlobalInfo

from rest_framework import serializers

from easyaudit.models import CRUDEvent


class GlobalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalInfo
        fields = "__all__"


class ScheduleSerializer(serializers.ModelSerializer):
    ota_name = serializers.StringRelatedField()
    creator = serializers.StringRelatedField()

    class Meta:
        model = Schedule
        fields = ("id", "creator", "ota_name",
                  "check_in_date", "check_out_date", "status")


class CRUDEventSerializer(serializers.ModelSerializer):
    event_type = serializers.SerializerMethodField()
    content_type = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = CRUDEvent
        exclude = ("object_id", "user_pk_as_string",
                   "object_json_repr")

    @staticmethod
    def get_event_type(obj):
        return obj.get_event_type_display()


class OTASerializer(serializers.ModelSerializer):

    class Meta:
        model = enq_models.OTA
        fields = "__all__"


class PartnerSerializer(serializers.ModelSerializer):
    partner_type_display = serializers.SerializerMethodField()

    class Meta:
        model = enq_models.Partner
        fields = "__all__"

    @staticmethod
    def get_partner_type_display(obj):
        return obj.get_partner_type_display()


class ReviewSerializer(serializers.ModelSerializer):
    rating_display = serializers.SerializerMethodField()

    class Meta:
        model = enq_models.Review
        fields = "__all__"

    @staticmethod
    def get_rating_display(obj):
        return obj.get_rating_display()
