from rest_framework import serializers
from .models import AL, Iteration


class ALSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['n_instances'] <= 0 :
            raise serializers.ValidationError("n_instances has to be bigger than 0")
        if data['accuracy_goal'] <= 0 or data['accuracy_goal'] > 100 :
            raise serializers.ValidationError("accuracy_goal has to be between [0,100]")
        return data

    class Meta:
        model = AL
        fields = '__all__'

    
class IterationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Iteration
        fields = '__all__'
