from os import path
from .query import *
from .estimators import *
from modAL.models import ActiveLearner
from als.models import AL, Iteration
from als.serializers import ALSerializer
from training.models import TrainingDataset,TrainingImage
from training.serializers import TrainingDatasetSerializer, TrainingImageSerializer
from testing.models import TestingDataset,TestingImage
from testing.serializers import TestingDatasetSerializer, TestingImageSerializer
from unlabeled.models import UnlabeledDataset,UnlabeledImage
from unlabeled.serializers import UnlabeledDatasetSerializer, UnlabeledImageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
import tempfile, zipfile
from django.http import HttpResponse
from rest_framework import status
from wsgiref.util import FileWrapper
import numpy as np
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from PIL import Image
from tensorflow.keras.models import load_model
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from accounts.decorators import specialist_required


@method_decorator([login_required, specialist_required], name='dispatch')
class AnotationsViewSet(APIView):

    def zip(self,index,unlabeled_dataset):
            #send zip file with images
            temp = tempfile.TemporaryFile()
            archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)

            images=[]
            for idx in index: images.append(UnlabeledImage.objects.filter(id_dataset=unlabeled_dataset.id,blocked=False)[int(idx)])

            for image in images:
                image.blocked=True
                image.save()
                archive.write(image.image.path, '%d.png' % image.id)

            archive.close()

            temp.seek(0)
            wrapper = FileWrapper(temp)

            response = HttpResponse(wrapper, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=unlabeled.zip'
            return response
        
    def load_unlabeled_images(self,unlabeled_dataset):
            unlabeled_images=UnlabeledImage.objects.filter(id_dataset=unlabeled_dataset.id, blocked=False)

            pool=[]
            #unlabeled_images to numpy  
            for image in unlabeled_images: 
                image.image.open()
                img = np.array(Image.open(image.image).convert("RGB"))
                pool.append(img)
        
            return pool
    
    def load_train_images(self,training_dataset):
        training_images=TrainingImage.objects.filter(id_dataset=training_dataset.id)

        x_train, y_train = [], []  
        #training_images to numpy      
        for image in training_images: 
            image.image.open()
            img = np.array(Image.open(image.image).convert("RGB"))
            x_train.append(img)

            if(image.label==True): y_train.append(1)
            else: y_train.append(0)
        return x_train, y_train

    def get(self, request, format=None):
        try:
            #get active learning technic activated for training
            al=AL.objects.get(training_activated=True)
            if(al.is_quering): return Response("Try later please, get anotations is busy. This helps avoid concurrency")
            else:
                al.is_quering=True
                al.save()
                
                model=globals()[al.model]
                classifier = KerasClassifier(model)

                #globals allows to call a function by a string  Ex: UncertaintySampling(10) ->  globals()["cnn"](10)
                query_techinc=globals()[al.query_technic](al.n_instances)

                #create modal framework active learning instance
                learner = ActiveLearner(
                    classifier,
                    query_techinc,
                    )

                #globals allows to call a function by a string  Ex: cnn ->  globals()["cnn"]
                if(path.exists("media/models/%d.h5" % al.id)): 
                    learner.estimator.model=load_model("media/models/%d.h5" % al.id)
                else:
                    training_dataset=TrainingDataset.objects.get(id_al=al.id)
                    x_train, y_train = self.load_train_images(training_dataset)
                    learner.teach(np.array(x_train,dtype = float),np.array(y_train,dtype = float))
                
                #load images
                unlabeled_dataset=UnlabeledDataset.objects.get(id_al=al.id)
            
                pool = self.load_unlabeled_images(unlabeled_dataset)

                #get images to anotate
                index,_=learner.query(np.array(pool))

                al.is_quering=False
                al.save()

                # return response with zip file with images
                return self.zip(index,unlabeled_dataset)
        except AL.DoesNotExist:
            raise Http404

    def save_labels(self, ids, labels):
        al=AL.objects.get(training_activated=True)
        training_dataset=TrainingDataset.objects.get(pk=al.id)
        
        for id, label in zip(ids, labels):
            image = UnlabeledImage.objects.get(id=id)
            TrainingImage.objects.create(image=image.image, id_dataset=training_dataset, label=label)

    def train(self,ids,labels):
  
        x, y = [],[]
        for id, label in zip(ids, labels):
            image = UnlabeledImage.objects.get(id=id)
            img = np.array(Image.open(image.image).convert("RGB"))
            x.append(img)
            if(label==True): y.append(1)
            else: y.append(0)

        #get active learning technic activated for training
        al=AL.objects.get(training_activated=True)
                        
        #globals allows to call a function by a string  Ex: cnn ->  globals()["cnn"]
        model=globals()[al.model]
        
        classifier = KerasClassifier(model)
            
        #globals allows to call a function by a string  Ex: UncertaintySampling(10) ->  globals()["cnn"](10)
        query_techinc=globals()[al.query_technic](al.n_instances)

        training_images=TrainingImage.objects.filter(id_dataset=al.id)

        x_train, y_train = [], []  
        #training_images to numpy      
        for image in training_images: 
            image.image.open()
            img = np.array(Image.open(image.image).convert("RGB"))
            x_train.append(img)

            if(image.label==True): y_train.append(1)
            else: y_train.append(0)
        
        learner = ActiveLearner(
                classifier,
                query_techinc,
                np.array(x_train,dtype = float),
                np.array(y_train,dtype = float)
            )

        if(path.exists("media/models/%d.h5" % al.id)): learner.estimator.model=load_model("media/models/%d.h5" % al.id)
        learner.teach(x,y)

        testing_images=TestingImage.objects.filter(id_dataset=al.id)

        x_test, y_test = [], []  
        #testing_images to numpy      
        for image in testing_images: 
            image.image.open()
            img = np.array(Image.open(image.image).convert("RGB"))
            x_test.append(img)

            if(image.label==True): y_test.append(1)
            else: y_test.append(0)

        learner.estimator.model.save("media/models/%d.h5" % al.id)

        accuracy=learner.score(np.array(x_test,dtype = float),np.array(y_test,dtype = float), verbose=0)
        Iteration.objects.create(accuracy=accuracy, id_al=al)
        
    def post(self, request, format=None):
        try:
            if len(request.POST.getlist('id'))==len(request.POST.getlist('label')):  
                
                ids = request.POST.getlist('id')
                labels=request.POST.getlist('label')
                
                self.train(ids,labels)
                self.save_labels(ids,labels)

                return Response(status=status.HTTP_201_CREATED)

            return Response("id field and label not have the same length", status=status.HTTP_400_BAD_REQUEST)
        except:
            raise