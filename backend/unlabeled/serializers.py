from rest_framework import serializers
from .models import UnlabeledDataset, UnlabeledImage


class UnlabeledDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnlabeledDataset
        fields = '__all__'


class UnlabeledImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnlabeledImage
        fields = '__all__'


