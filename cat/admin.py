from django.contrib import admin

# Register your models here.
from cat.models import Search, ExchangeValue, TIIESearch


@admin.register(ExchangeValue)
class ExchangeValueAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'date',
        'value',
    )

    list_filter = (
        'type',
    )

@admin.register(Search)
class SeachAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'init_date',
        'end_date',
    )

    list_filter = (
        'type',
    )


@admin.register(TIIESearch)
class SeachAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'init_date',
        'end_date',
    )
