import os.path
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FrameSerializer, EndoscopySerializer
from .models import Frame, Endoscopy
from rest_framework import status
from django.http import Http404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import tempfile, zipfile
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from als.models import AL
from anotations.estimators import *
from anotations.query import *
from training.models import TrainingImage
import numpy as np
from PIL import Image
from modAL.models import ActiveLearner
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from tensorflow.keras.models import load_model
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from accounts.decorators import medic_required


@method_decorator([login_required, medic_required], name='dispatch')  
class Endoscopy_APIView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request, format=None, *args, **kwargs):
        endoscopy = Endoscopy.objects.all()
        serializer = EndoscopySerializer(endoscopy, many=True)
        
        return Response(serializer.data)

    def post(self, request, format=None):
        endoscopy_serializer = EndoscopySerializer(data=request.data)
        if endoscopy_serializer.is_valid() and request.data['images']:
            endoscopy=endoscopy_serializer.save()

            serializer = FrameSerializer(data=request.data)
            
            files_list = request.FILES.getlist('images')
            if serializer.is_valid():
                for item in files_list:
                    f = Frame.objects.create(image=item, id_endoscopy=endoscopy)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
@method_decorator([login_required, medic_required], name='dispatch')  
class Endoscopy_APIView_Detail(APIView):
    serializer_class = FrameSerializer

    def get(self, request, id, format=None):
        try:
            if Endoscopy.objects.get(pk=id):
                filtered_images=Frame.objects.filter(id_endoscopy=id)
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
        except Endoscopy.DoesNotExist:
            raise Http404
        
    def delete(self, request, id, format=None):
        try:
            if Endoscopy.objects.get(pk=id):
                filtered_images=Frame.objects.filter(id_endoscopy=id)
                filtered_images.delete()
            endoscopy = Endoscopy.objects.get(pk=id)
            endoscopy.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Endoscopy.DoesNotExist:
            raise Http404
        
@method_decorator([login_required, medic_required], name='dispatch')  
class Predict_APIView_Detail(APIView):

    def get(self, request, id, format=None):
        
        if Endoscopy.objects.get(pk=id):
            filtered_images=Frame.objects.filter(id_endoscopy=id)
            
            endoscopy=[]
            for image in filtered_images:
                image.image.open()
                img = np.array(Image.open(image.image).convert("RGB"))
                endoscopy.append(img)

            #get active learning technic activated for predicting
            al=AL.objects.get(predicting_activated=True)

            model=globals()[al.model]
            cnn=model()

            if(os.path.exists("media/models/%d.h5" % al.id)):  cnn=load_model("media/models/%d.h5" % al.id)
            results=cnn.predict(np.array(endoscopy,dtype = float))

            temp = tempfile.TemporaryFile()
            archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
            index=0
            for x, y in zip(filtered_images, results):
                if(y==1): archive.write(x.image.path, 'informative/%d.png' % index)
                else:archive.write(x.image.path, 'non_informative/%d.png' % index)
                index+=1
            archive.close()

            temp.seek(0)
            wrapper = FileWrapper(temp)

            response = HttpResponse(wrapper, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=results.zip'
            return response
