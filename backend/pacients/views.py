from rest_framework.viewsets import ModelViewSet
from .models import Pacient
from .serializers import PacientSerializer
from rest_framework import permissions
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from accounts.decorators import medic_required


@method_decorator([login_required, medic_required], name='dispatch')  
class PatiantsViewSet(ModelViewSet):
    queryset = Pacient.objects.all()
    serializer_class = PacientSerializer

