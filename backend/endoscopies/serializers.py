from rest_framework import serializers
from .models import Endoscopy,Frame


class EndoscopySerializer(serializers.ModelSerializer):
    class Meta:
        model = Endoscopy
        fields = '__all__'


class FrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = '__all__'


