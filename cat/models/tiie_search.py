from collections import OrderedDict

from django.db import models
from django.apps import apps


def merge(dct1, dct2):
    result = OrderedDict()
    before_size = False
    last_2_value = None
    for key, value in dct1.items():
        if type(value) != list:
            values = [value]
        else:
            values = value

        if not before_size:
            before_size = len(values)

        if key in dct2:
            values.append(dct2[key])
            last_2_value = dct2[key]
        else:
            values.append(last_2_value)
        result[key] = values

    for key, value in dct2.items():
        if type(value) != list:
            values = [value]
        else:
            values = value

        if key not in dct1:
            values.append([None for _ in range(before_size)] + dct2[key])
            result[key] = values
    return result


def unpack(dct):
    return [[key] + value for key, value in dct.items()]


class TIIESearch(models.Model):
    init_date = models.DateField()
    end_date = models.DateField()

    def lines(self):
        return [search.get_type_display() for search in self.searches.all()]

    def values(self):
        values_1 = OrderedDict(sorted({key.strftime('%Y-%m-%d'): value for key, value in
                    list(self.searches.first().results.values_list('date', 'value'))}.items()))
        values_2 = OrderedDict(sorted({key.strftime('%Y-%m-%d'): value for key, value in
                    list(self.searches.all()[1].results.values_list('date', 'value'))}.items()))
        values_3 = OrderedDict(sorted({key.strftime('%Y-%m-%d'): value for key, value in
                    list(self.searches.last().results.values_list('date', 'value'))}.items()))
        values_1_2 = merge(values_1, values_2)
        values = merge(values_1_2, values_3)
        values = OrderedDict(sorted(values.items()))
        values = unpack(values)
        return values

    def perform(self):
        for search in self.searches.all():
            search.perform()

    class Meta:
        unique_together = ['init_date', 'end_date']
