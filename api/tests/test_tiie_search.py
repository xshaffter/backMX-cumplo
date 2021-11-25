from datetime import datetime, date

from django.db import IntegrityError
from django.test import TestCase
from cat.models import TIIESearch


class TIIESearchTestCase(TestCase):
    def setUp(self):
        init_date = date(2021, 1, 1)
        end_date = date(2021, 1, 24)
        TIIESearch.objects.create(init_date=init_date, end_date=end_date)

    def test_only_type_date(self):
        self.assertEqual(IntegrityError, lambda x: ExchangeValue.objects.create(type=ExchangeValue.UDIS, value=10, date=datetime.today()))
