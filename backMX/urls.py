from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from cat.views import home as home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', home_view)
]
