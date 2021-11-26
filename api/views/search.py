from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import SearchSerializer, ExchangeValueSerializer, ApiSerializer
from api.serializers.search import TIIESearchSerializer
from cat.models import Search, ExchangeValue, TIIESearch


@transaction.atomic
@api_view(['GET'])
def search(request):
    """
    :param request: WSGIRequest item with the values: type: int, init_date: date, end_date: date
    :return: HttpResponse with json data for the obtained results according to the type and between init_date and end_date
    """
    data = request.GET.dict()
    data['type'] = ExchangeValue.NAME_AS_CODE[data['type']]
    search_serializer = SearchSerializer(data=data)
    if search_serializer.is_valid(raise_exception=False):
        search = search_serializer.save()
        api_request = ApiSerializer(data={
            'init_date': search.init_date,
            'end_date': search.end_date,
            'type': search.type
        })
        api_request.is_valid(raise_exception=True)
        api_result = api_request.save()

        series = api_result['bmx']['series']
        values = ExchangeValue.change_keys(series)

        serializer = ExchangeValueSerializer(data=values, many=True)
        serializer.is_valid(raise_exception=False)
        serializer.save()
        search.search_results()
    else:
        search = Search.objects.get(**data)

    serializer_data = SearchSerializer(search)
    return Response(data=serializer_data.data, status=status.HTTP_200_OK)


@transaction.atomic
@api_view(['GET'])
def tiie_search(request):
    """
    :param request: WSGIRequest item with the values: type: int, init_date: date, end_date: date
    :return: HttpResponse with json data for the obtained TIIE results for every done sub search
    """
    data = request.GET.dict()
    data.pop('type')
    search_serializer = TIIESearchSerializer(data=data)
    if search_serializer.is_valid(raise_exception=False):
        search = search_serializer.save()  # type: TIIESearch
        for sub_search in search.searches.all():  # type: Search
            api_request = ApiSerializer(data={
                'init_date': sub_search.init_date,
                'end_date': sub_search.end_date,
                'type': sub_search.type
            })
            api_request.is_valid(raise_exception=True)
            api_result = api_request.save()

            series = api_result['bmx']['series']
            values = ExchangeValue.change_keys(series)

            serializer = ExchangeValueSerializer(data=values, many=True)
            serializer.is_valid(raise_exception=False)
            serializer.save()
            sub_search.search_results()
    else:
        search = TIIESearch.objects.get(**data)
    serializer_data = TIIESearchSerializer(search)
    return Response(data=serializer_data.data, status=status.HTTP_200_OK)
