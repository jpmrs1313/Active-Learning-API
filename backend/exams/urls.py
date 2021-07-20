from django.urls import path
from rest_framework import routers
from .views import ExamViewSet,Exam_Pacient_APIView

router = routers.DefaultRouter()
router.register('exams', ExamViewSet)

urlpatterns = [
    path('exams/pacient/<int:id>/', Exam_Pacient_APIView.as_view())
]
urlpatterns += router.urls

