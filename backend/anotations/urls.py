from django.urls import path
from .views import AnotationsViewSet
app_name = 'anotations'

urlpatterns = [
    path('anotations/', AnotationsViewSet.as_view()),
]