from django.urls import path
from .views import *

app_name = 'unlabeled'

urlpatterns = [
    path('unlabeled/', Unlabeled_APIView.as_view()),
    path('unlabeled/<int:id>/', Unlabeled_APIView_Detail.as_view()),    
]