from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.serializers import SearchSerializer
from api.serializers.search import TIIESearchSerializer
from cat.models import Search, ExchangeValue, TIIESearch


class SearchViewSet(viewsets.ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer
    permission_classes = []

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if data['type'] != 'tiie':
            data['type'] = ExchangeValue.NAME_AS_CODE[data['type']]
            search = SearchSerializer(data=data)
            if search.is_valid(raise_exception=False):
                search = search.save()
                search.perform()
            else:
                search = Search.objects.get(**data)

            serializer_data = SearchSerializer(search)
        else:
            data.pop('type')
            search = TIIESearchSerializer(data=data)
            if search.is_valid(raise_exception=False):
                search = search.save()
                search.perform()
            else:
                search = TIIESearch.objects.get(**data)
            serializer_data = TIIESearchSerializer(search)

        return Response(data=serializer_data.data, status=status.HTTP_200_OK)
