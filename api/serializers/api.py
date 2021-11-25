import requests

from django.utils.translation import gettext as _
from django.conf import settings
from rest_framework import serializers

from cat.models import ExchangeValue


class ApiSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=10, required=True)
    init_date = serializers.DateField(format=settings.DATE_FORMAT, required=True)
    end_date = serializers.DateField(format=settings.DATE_FORMAT, required=True)

    def validate(self, attrs):
        init_date = attrs.get('init_date', None)
        end_date = attrs.get('end_date', None)

        if end_date < init_date:
            raise serializers.ValidationError(_("La fecha final no puede ser menor a la fecha inicial"))

        return attrs

    def create(self, validated_data):
        type = validated_data.pop('type')
        serie = ExchangeValue.CODE_AS_SERIE[type]
        base_url = settings.BANXICO_URL
        response = requests.get(base_url.format(series=serie, **validated_data))
        return response.json()

