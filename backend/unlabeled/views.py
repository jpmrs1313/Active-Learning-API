from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UnlabeledDatasetSerializer, UnlabeledImageSerializer
from .models import UnlabeledDataset, UnlabeledImage
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
class Unlabeled_APIView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request, format=None, *args, **kwargs):
        dataset = UnlabeledDataset.objects.all()
        serializer = UnlabeledDatasetSerializer(dataset, many=True)
        
        return Response(serializer.data)

    def post(self, request, format=None):
        unlabeled_serializer = UnlabeledDatasetSerializer(data=request.data)
        if unlabeled_serializer.is_valid() and request.data['images']:
            unlabeled=unlabeled_serializer.save()

            serializer = UnlabeledImageSerializer(data=request.data)
            
            files_list = request.FILES.getlist('images')
            if serializer.is_valid():
                for item in files_list:
                    f = UnlabeledImage.objects.create(image=item, id_dataset=unlabeled)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
   
@method_decorator([login_required, staff_member_required], name='dispatch')
class Unlabeled_APIView_Detail(APIView):
    serializer_class = UnlabeledImageSerializer

    def get(self, request, id, format=None):
        try:
            dataset=UnlabeledDataset.objects.get(pk=id)
            filtered_images=UnlabeledImage.objects.filter(id_dataset=dataset.id)
            
            temp = tempfile.TemporaryFile()
            archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
            index=0
            for image in filtered_images:
                index=index+1
                archive.write(image.image.path, 'file%d.png' % index)

            archive.close()

            temp.seek(0)
            wrapper = FileWrapper(temp)

            response = HttpResponse(wrapper, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=test.zip'
            return response
        except UnlabeledDataset.DoesNotExist:
            raise Http404
        
    def delete(self, request, id, format=None):
        try:
            if UnlabeledDataset.objects.get(pk=id):
                filtered_images=UnlabeledImage.objects.filter(id_dataset=id)
                filtered_images.delete()
            unlabeled = UnlabeledDataset.objects.get(pk=id)
            unlabeled.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UnlabeledDataset.DoesNotExist:
            raise Http404
        
   