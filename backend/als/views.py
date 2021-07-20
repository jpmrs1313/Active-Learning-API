from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AL, Iteration
from .serializers import ALSerializer, IterationSerializer
from rest_framework import status
from django.http import Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required



@method_decorator([login_required, staff_member_required], name='dispatch')
class ALsViewSet(APIView):
    
    def get(self, request, format=None, *args, **kwargs):
        al = AL.objects.all()
        serializer = ALSerializer(al, many=True)
        
        return Response(serializer.data)

    def post(self, request, format=None):
        al_serializer = ALSerializer(data=request.data)

        if al_serializer.is_valid():
            al=al_serializer.save()
            return Response(al_serializer.data, status=status.HTTP_201_CREATED)
        return Response(al_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator([login_required, staff_member_required], name='dispatch')
class AL_APIView_Detail(APIView):
    serializer_class = ALSerializer
    
    def get_object(self, pk):
        try:
            return AL.objects.get(pk=pk)
        except AL.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        al = self.get_object(pk)
        serializer = ALSerializer(al)  
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        al = self.get_object(pk)
        serializer = ALSerializer(al, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        al = self.get_object(pk)
        al.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@method_decorator([login_required, staff_member_required], name='dispatch')        
class TrainActivateALsViewSet(APIView):
    def get(self, request, format=None):
        try:
            al=AL.objects.get(training_activated=True)
            serializer = ALSerializer(al)
            return Response(serializer.data)
        except AL.DoesNotExist:
            raise Http404

@method_decorator([login_required, staff_member_required], name='dispatch')
class TrainActivateALsViewSet_Detail(APIView):

    def get(self, request, pk, format=None):
        
        try:
            try:
                to_desactivate=AL.objects.get(training_activated=True)
                to_desactivate.training_activated = False

                to_activate=AL.objects.get(id=pk)
                to_activate.training_activated = True
                
                to_desactivate.save() 
                to_activate.save() 
    

                serializer = ALSerializer(to_activate)

                return Response(serializer.data)
            except AL.DoesNotExist:
   
                to_activate=AL.objects.get(id=pk)
                to_activate.training_activated = True
                to_activate.save() 
    
                serializer = ALSerializer(to_activate)

                return Response(serializer.data)
        except AL.DoesNotExist:
            raise Http404            
        
@method_decorator([login_required, staff_member_required], name='dispatch')
class PredictActivateALsViewSet(APIView):
    def get(self, request, format=None):
        try:
            al=AL.objects.get(predicting_activated=True)
            serializer = ALSerializer(al)
            return Response(serializer.data)
        except AL.DoesNotExist:
            raise Http404

@method_decorator([login_required, staff_member_required], name='dispatch')
class PredictActivateALsViewSet_Detail(APIView):

    def get(self, request, pk, format=None):
        
        try:
            try:
                to_desactivate=AL.objects.get(predicting_activated=True)
                to_desactivate.predicting_activated = False

                to_activate=AL.objects.get(id=pk)
                to_activate.predicting_activated = True
                
                to_desactivate.save() 
                to_activate.save() 
    

                serializer = ALSerializer(to_activate)

                return Response(serializer.data)
            except AL.DoesNotExist:
   
                to_activate=AL.objects.get(id=pk)
                to_activate.predicting_activated = True
                to_activate.save() 
    
                serializer = ALSerializer(to_activate)

                return Response(serializer.data)
        except AL.DoesNotExist:
            raise Http404            
        
@method_decorator([login_required, staff_member_required], name='dispatch')
class Iteration_APIView_Detail(APIView):
    serializer_class = IterationSerializer

    def get(self, request, pk, format=None):
        iteration = Iteration.objects.filter(id_al=pk)
        serializer = IterationSerializer(iteration, many=True)  
        return Response(serializer.data)




