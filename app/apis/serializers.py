from users.models import GlobalInfo
from rest_framework import serializers
from easyaudit.models import CRUDEvent


class GlobalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalInfo
        fields = "__all__"


class CRUDEventSerializer(serializers.ModelSerializer):
    event_type = serializers.SerializerMethodField()
    content_type = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = CRUDEvent
        exclude = ("object_id", "user_pk_as_string", "object_json_repr")

    @staticmethod
    def get_event_type(obj):
        return obj.get_event_type_display()
