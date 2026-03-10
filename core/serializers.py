from rest_framework import serializers
from .models import ColdStorage, Scheme, CropProduction

class ColdStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColdStorage
        fields = '__all__'

class SchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheme
        fields = '__all__'

class CropProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropProduction
        fields = '__all__'
