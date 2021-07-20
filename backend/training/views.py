from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TrainingDatasetSerializer, TrainingImageSerializer
from .models import TrainingDataset, TrainingImage
from rest_framework import status
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import tempfile, zipfile
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required   


@method_decorator([login_required, staff_member_required], name='dispatch')
class Training_APIView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request, format=None, *args, **kwargs):
        dataset = TrainingDataset.objects.all()
        serializer = TrainingDatasetSerializer(dataset, many=True)
        
        return Response(serializer.data)

    def post(self, request, format=None):
        training_serializer = TrainingDatasetSerializer(data=request.data)
        if training_serializer.is_valid() and request.data['informative_images'] and request.data['informative_images']:
            training=training_serializer.save()

            serializer = TrainingDatasetSerializer(data=request.data)
            
            informative_list = request.FILES.getlist('informative_images')
            non_informative_list = request.FILES.getlist('non_informative_images')
            if serializer.is_valid():
                for item in informative_list:
                    f = TrainingImage.objects.create(image=item, id_dataset=training, label=True)
                for item in non_informative_list:
                    f = TrainingImage.objects.create(image=item, id_dataset=training, label=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
@method_decorator([login_required, staff_member_required], name='dispatch')
class Training_APIView_Detail(APIView):
    serializer_class = TrainingImageSerializer

    def get(self, request, id, format=None):
        try:
            if TrainingDataset.objects.get(pk=id):
                informative_images=TrainingImage.objects.filter(id_dataset=id,label=True)
                non_informative_images=TrainingImage.objects.filter(id_dataset=id,label=False)

                
                temp = tempfile.TemporaryFile()
                archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
                index=0
                for image in informative_images:
                    index=index+1
                    archive.write(image.image.path, 'informative/file%d.png' % index) 
                index=0
                for image in non_informative_images:
                    index=index+1
                    archive.write(image.image.path, 'non_informative/file%d.png' % index) 
                archive.close()

                temp.seek(0)
                wrapper = FileWrapper(temp)

                response = HttpResponse(wrapper, content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename=test.zip'
                return response
        except TrainingDataset.DoesNotExist:
            raise Http404
        
    def delete(self, request, id, format=None):
        try:
            if TrainingDataset.objects.get(pk=id):
                filtered_images=TrainingImage.objects.filter(id_dataset=id)
                filtered_images.delete()
            training = TrainingDataset.objects.get(pk=id)
            training.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except TrainingDataset.DoesNotExist:
            raise Http404
        