from datetime import date
from rest_framework.serializers import ModelSerializer,DateField, ValidationError
from .models import Exam

    
class ExamSerializer(ModelSerializer):
    exam_date = DateField()
    
    def validate_exam_date(self, dob):
        if (dob < date.today()):
            raise ValidationError("Invalid exam_date. Cant be before today")
        return dob

    class Meta:
        model = Exam
        fields = ['id_exam', 'id_pacient','exam_date', 'exam_type', 'exam_notes', 'exam_result']
