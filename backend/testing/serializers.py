from rest_framework import serializers
from .models import TestingDataset, TestingImage


class TestingDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestingDataset
        fields = '__all__'


class TestingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestingImage
        fields = '__all__'


