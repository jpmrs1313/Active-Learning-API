from datetime import date
from rest_framework.serializers import ModelSerializer, ValidationError, DateField
from .models import Pacient


class PacientSerializer(ModelSerializer):
    birth_date = DateField()

    def validate_birth_date(self, dob):
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if (age<0 or age >150):
            raise ValidationError("Invalid date of birth. Has to be between 0 and 150 years")
        return dob

    class Meta:
        model = Pacient
        fields = ['id_pacient', 'first_name', 'last_name', 'birth_date', 'total_exams', 'remarks']

