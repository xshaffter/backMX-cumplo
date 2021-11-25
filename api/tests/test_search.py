from datetime import datetime, date

from django.db import IntegrityError
from django.test import TestCase
from cat.models import ExchangeValue, Search


class SearchTestCase(TestCase):
    def setUp(self):
        init_date = date(2021, 1, 1)
        end_date = date(2021, 1, 2)
        ExchangeValue.objects.create(type=ExchangeValue.UDIS, value=10, date=init_date)
        ExchangeValue.objects.create(type=ExchangeValue.UDIS, value=10, date=end_date)
        Search.objects.create(init_date=init_date, end_date=end_date, type=Search.UDIS)

    def test_only_type_date(self):
        self.assertEqual(IntegrityError, lambda x: ExchangeValue.objects.create(type=ExchangeValue.UDIS, value=10, date=datetime.today()))
