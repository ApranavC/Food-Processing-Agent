from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ColdStorageViewSet, SchemeViewSet, CropProductionViewSet

router = DefaultRouter()
router.register(r'cold-storages', ColdStorageViewSet)
router.register(r'schemes', SchemeViewSet)
router.register(r'crop-production', CropProductionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
