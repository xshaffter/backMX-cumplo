from collections import OrderedDict

from django.utils.translation import gettext as _
from django.db import models
from django.apps import apps

from cat.functions import merge, unpack


class TIIESearch(models.Model):
    init_date = models.DateField(_("init date"))
    end_date = models.DateField(_("final date"))

    def lines(self):
        return [search.get_type_display() for search in self.searches.all()]

    def values(self):
        """
        :return: a key ordered list based on dict data obtained from
                results with the form [[key, value, value, value], [key, value, value, value]]
        """
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

    class Meta:
        unique_together = ['init_date', 'end_date']
        verbose_name_plural = _("TIIE Searches")
        verbose_name = _("TIIE Search")
