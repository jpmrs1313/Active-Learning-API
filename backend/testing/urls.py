from django.urls import path
from .views import *

app_name = 'testing'

urlpatterns = [
    path('testing/', Testing_APIView.as_view()),
    path('testing/<int:id>/', Testing_APIView_Detail.as_view()),    
]