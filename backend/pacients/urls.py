from django.urls import path
from rest_framework import routers
from .views import PatiantsViewSet

router = routers.DefaultRouter()
router.register('pacients', PatiantsViewSet)

urlpatterns = router.urls