from datetime import datetime

from django.db import IntegrityError
from django.test import TestCase
from cat.models import ExchangeValue


class ExchangeValueTestCase(TestCase):
    def setUp(self):
        ExchangeValue.objects.create(type=ExchangeValue.UDIS, value=10, date=datetime.today())

    def test_only_type_date(self):
        self.assertEqual(IntegrityError, lambda x: ExchangeValue.objects.create(type=ExchangeValue.UDIS, value=10, date=datetime.today()))
