from django.db import models

from django.apps import apps
from django.db.models import Avg, Min, Max


class Search(models.Model):
    UDIS = 0
    USD = 1
    TIIE_4_SEMANAS = 2
    TIIE_13_SEMANAS = 3
    TIIE_26_SEMANAS = 4
    TYPES = (
        (UDIS, 'UDIS'),
        (USD, 'USD'),
        (TIIE_4_SEMANAS, 'TIIE 4 semanas'),
        (TIIE_13_SEMANAS, 'TIIE 13 semanas'),
        (TIIE_26_SEMANAS, 'TIIE 26 semanas'),
    )

    CODE_AS_COLOR = {
        str(UDIS): '',
        str(USD): '',
        str(TIIE_4_SEMANAS): '#104f2c',
        str(TIIE_13_SEMANAS): '#352da1',
        str(TIIE_26_SEMANAS): '#a60a17',
    }

    type = models.SmallIntegerField(choices=TYPES, default=UDIS)
    init_date = models.DateField()
    end_date = models.DateField()
    results = models.ManyToManyField('cat.ExchangeValue', related_name='queries')
    avg_value = models.DecimalField(decimal_places=10, max_digits=15, null=True, blank=True)
    min_value = models.DecimalField(decimal_places=10, max_digits=15, null=True, blank=True)
    max_value = models.DecimalField(decimal_places=10, max_digits=15, null=True, blank=True)
    tiie_search = models.ForeignKey('cat.TIIESearch', null=True, blank=True, related_name='searches', on_delete=models.CASCADE)

    def avg(self):
        if not self.avg_value:
            self.avg_value = self.results.aggregate(total=Avg('value'))['total']
            self.save()
        return self.avg_value

    def min(self):
        if not self.min_value:
            self.min_value = self.results.aggregate(total=Min('value'))['total']
            self.save()
        return self.min_value

    def max(self):
        if not self.max_value:
            self.max_value = self.results.aggregate(total=Max('value'))['total']
            self.save()
        return self.max_value

    def values(self):
        return self.results.values_list('date', 'value').order_by('date').distinct()

    def color(self):
        return self.CODE_AS_COLOR[str(self.type)]

    def perform(self):
        from api.serializers import ApiSerializer, ExchangeValueSerializer
        ExchangeValue = apps.get_model('cat', 'ExchangeValue')
        api_request = ApiSerializer(data={
            'init_date': self.init_date,
            'end_date': self.end_date,
            'type': self.type
        })
        api_request.is_valid(raise_exception=True)
        data = api_request.save()

        series = data['bmx']['series']
        values = ExchangeValue.change_keys(series)

        serializer = ExchangeValueSerializer(data=values, many=True)
        serializer.is_valid(raise_exception=False)
        serializer.save()
        queryset = ExchangeValue.objects.filter(date__gte=self.init_date, date__lte=self.end_date, type=self.type)
        self.results.add(*queryset)

    class Meta:
        unique_together = ['type', 'init_date', 'end_date']
