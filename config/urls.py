from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from cat.views import home as home_view
from api import views as api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/search/', api_views.search, name='search'),
    path('api/tiie_search/', api_views.tiie_search, name='tiie-search'),
    path('', home_view)
]
