from rest_framework import serializers

from cat.models import ExchangeValue


class ExchangeValueSerializer(serializers.ModelSerializer):
    date = serializers.DateField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = ExchangeValue
        fields = (
            'type',
            'get_type_display',
            'value',
            'date'
        )
