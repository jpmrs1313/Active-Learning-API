from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import Exam
from .serializers import ExamSerializer
from rest_framework.response import Response
from django.http import Http404
from rest_framework import permissions
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from accounts.decorators import medic_required


@method_decorator([login_required, medic_required], name='dispatch')  
class ExamViewSet(ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    


@method_decorator([login_required, medic_required], name='dispatch')  
class Exam_Pacient_APIView(APIView):
    serializer_class = ExamSerializer

    def get(self, request, id, format=None):
        try:
            exams=Exam.objects.filter(id_pacient=id)
            serializer = ExamSerializer(exams, many=True)
            return Response(serializer.data)
        except Exam.DoesNotExist:
            raise Http404