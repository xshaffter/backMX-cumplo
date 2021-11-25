from django.apps import apps
from rest_framework import serializers

from cat.models import Search, TIIESearch


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = (
            'type',
            'get_type_display',
            'init_date',
            'end_date',
            'values',
            'avg',
            'max',
            'min',
            'color'
        )


class TIIESearchSerializer(serializers.ModelSerializer):
    searches = SearchSerializer(many=True, read_only=True, required=False, allow_null=True)

    def create(self, validated_data):
        ExchangeValue = apps.get_model('cat', 'ExchangeValue')
        search = TIIESearch(**validated_data)
        search.save()
        for tiie in ['tiie_4_semanas', 'tiie_13_semanas', 'tiie_26_semanas', ]:
            Search(type=ExchangeValue.NAME_AS_CODE[tiie], init_date=search.init_date, end_date=search.end_date,
                   tiie_search=search).save()

        return search

    class Meta:
        model = TIIESearch
        fields = (
            'init_date',
            'end_date',
            'searches',
            'lines',
            'values'
        )
