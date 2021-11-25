from datetime import datetime

from django.conf import settings
from django.db import models


class ExchangeValue(models.Model):
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

    SERIE_AS_CODE = {
        settings.SERIE_UDIS: UDIS,
        settings.SERIE_USD: USD,
        settings.SERIE_TIIE_4_SEMANAS: TIIE_4_SEMANAS,
        settings.SERIE_TIIE_13_SEMANAS: TIIE_13_SEMANAS,
        settings.SERIE_TIIE_26_SEMANAS: TIIE_26_SEMANAS,
    }
    CODE_AS_SERIE = {
        str(UDIS): settings.SERIE_UDIS,
        str(USD): settings.SERIE_USD,
        str(TIIE_4_SEMANAS): settings.SERIE_TIIE_4_SEMANAS,
        str(TIIE_13_SEMANAS): settings.SERIE_TIIE_13_SEMANAS,
        str(TIIE_26_SEMANAS): settings.SERIE_TIIE_26_SEMANAS,
    }
    NAME_AS_SERIE = {
        'udis': settings.SERIE_UDIS,
        'usd': settings.SERIE_USD,
        'tiie_4_semanas': settings.SERIE_TIIE_4_SEMANAS,
        'tiie_13_semanas': settings.SERIE_TIIE_13_SEMANAS,
        'tiie_26_semanas': settings.SERIE_TIIE_26_SEMANAS,
    }
    NAME_AS_CODE = {
        'udis': UDIS,
        'usd': USD,
        'tiie_4_semanas': TIIE_4_SEMANAS,
        'tiie_13_semanas': TIIE_13_SEMANAS,
        'tiie_26_semanas': TIIE_26_SEMANAS,
    }

    type = models.SmallIntegerField(choices=TYPES, default=UDIS)
    value = models.DecimalField(decimal_places=10, max_digits=15)
    date = models.DateField()

    @staticmethod
    def verify_exists(value_type, data):
        formatted_date = datetime.strptime(data['fecha'], '%d/%m/%Y').strftime('%Y-%m-%d')
        return ExchangeValue.objects.filter(type=value_type, date=formatted_date).exists()

    @staticmethod
    def change_keys(data):
        values = []
        for serie in data:
            value_type = ExchangeValue.SERIE_AS_CODE[serie['idSerie']]
            datos = [{
                'type': value_type,
                'date': dato['fecha'],
                'value': dato['dato']
            } for dato in serie['datos'] if not ExchangeValue.verify_exists(value_type, dato)]
            values += datos

        return values

    def __str__(self):
        return f'${self.get_type_display()}|{self.date.strftime("%Y-%m-%d")}'

    class Meta:
        unique_together = ['type', 'date']
