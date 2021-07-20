from django.urls import path
from .views import *
app_name = 'als'

urlpatterns = [
    path('als/', ALsViewSet.as_view()),
    path('als/<int:pk>/', AL_APIView_Detail.as_view()),
    path('als/train_activated/', TrainActivateALsViewSet.as_view()),    
    path('als/train_activated/<int:pk>/', TrainActivateALsViewSet_Detail.as_view()), 
    path('als/predict_activated/', PredictActivateALsViewSet.as_view()),    
    path('als/predict_activated/<int:pk>/', PredictActivateALsViewSet_Detail.as_view()), 
    path('als/stats/<int:pk>/', Iteration_APIView_Detail.as_view()), 
]