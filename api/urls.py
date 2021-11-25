from rest_framework.routers import DefaultRouter

from api.views import SearchViewSet

router = DefaultRouter()

router.register('search', SearchViewSet)

urlpatterns = router.urls
