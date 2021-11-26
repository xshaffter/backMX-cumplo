from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _


class ExchangeValue(models.Model):
    UDIS = 0
    USD = 1
    TIIE_4_SEMANAS = 2
    TIIE_13_SEMANAS = 3
    TIIE_26_SEMANAS = 4
    TYPES = (
        (UDIS, 'UDIS'),
        (USD, 'USD'),
        (TIIE_4_SEMANAS, _('TIIE 4 weeks')),
        (TIIE_13_SEMANAS, _('TIIE 13 weeks')),
        (TIIE_26_SEMANAS, _('TIIE 26 weeks')),
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

    type = models.SmallIntegerField(_("type"), choices=TYPES, default=UDIS)
    value = models.DecimalField(_("value"), decimal_places=10, max_digits=15)
    date = models.DateField(_("date"))

    @staticmethod
    def verify_exists(value_type, data):
        formatted_date = datetime.strptime(data['fecha'], '%d/%m/%Y').strftime('%Y-%m-%d')
        return ExchangeValue.objects.filter(type=value_type, date=formatted_date).exists()

    @staticmethod
    def change_keys(data):
        """
        :param data: dict data with the values obtained from the api
        :return: digested dict with transformed data
        """
        values = []
        for serie in data:
            # we change the string code to the DB code
            value_type = ExchangeValue.SERIE_AS_CODE[serie['idSerie']]
            # only add data if it isn't in the DB
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
        verbose_name = _('Exchange value')
        verbose_name_plural = _('Exchange values')