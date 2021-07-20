from django.urls import path
from .views import *

app_name = 'training'

urlpatterns = [
    path('training/', Training_APIView.as_view()),
    path('training/<int:id>/', Training_APIView_Detail.as_view()),    
]