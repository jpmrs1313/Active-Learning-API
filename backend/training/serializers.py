from rest_framework import serializers
from .models import TrainingDataset, TrainingImage


class TrainingDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingDataset
        fields = '__all__'


class TrainingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingImage
        fields = '__all__'


