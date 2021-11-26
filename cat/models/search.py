from django.db import models

from django.utils.translation import gettext as _
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
        (TIIE_4_SEMANAS, _('TIIE 4 weeks')),
        (TIIE_13_SEMANAS, _('TIIE 13 weeks')),
        (TIIE_26_SEMANAS, _('TIIE 26 weeks')),
    )

    CODE_AS_COLOR = {
        str(UDIS): '',
        str(USD): '',
        str(TIIE_4_SEMANAS): '#104f2c',
        str(TIIE_13_SEMANAS): '#352da1',
        str(TIIE_26_SEMANAS): '#a60a17',
    }

    type = models.SmallIntegerField(_("type"), choices=TYPES, default=UDIS)
    init_date = models.DateField(_("init date"), )
    end_date = models.DateField(_("final date"), )
    results = models.ManyToManyField('cat.ExchangeValue', verbose_name=_("results"), related_name='queries')
    avg_value = models.DecimalField(_("avg value"), decimal_places=10, max_digits=15, null=True, blank=True)
    min_value = models.DecimalField(_("min value"), decimal_places=10, max_digits=15, null=True, blank=True)
    max_value = models.DecimalField(_("max value"), decimal_places=10, max_digits=15, null=True, blank=True)
    tiie_search = models.ForeignKey('cat.TIIESearch', verbose_name=_("tiie search"), null=True, blank=True, related_name='searches',
                                    on_delete=models.CASCADE)

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

    def search_results(self):
        """
        we get the results that may be between [init_date, end_date] and add them to the m2m
        """
        ExchangeValue = apps.get_model('cat', 'ExchangeValue')
        queryset = ExchangeValue.objects.filter(date__gte=self.init_date, date__lte=self.end_date, type=self.type)
        self.results.add(*queryset)

    class Meta:
        unique_together = ['type', 'init_date', 'end_date']
        verbose_name = _("Search")
        verbose_name_plural = _("Searches")
