from rest_framework import viewsets
from .models import ColdStorage, Scheme, CropProduction
from .serializers import ColdStorageSerializer, SchemeSerializer, CropProductionSerializer

class ColdStorageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ColdStorage.objects.all()
    serializer_class = ColdStorageSerializer
    filterset_fields = ['state', 'district', 'status']

class SchemeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer

class CropProductionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CropProduction.objects.all()
    serializer_class = CropProductionSerializer
    filterset_fields = ['state', 'district', 'crop', 'year']
