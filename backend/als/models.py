from django.db import models


class AL(models.Model):
    name = models.CharField(max_length=50, null=False, blank=True)
    n_instances = models.IntegerField(null=False, default=10)
    accuracy_goal = models.FloatField(null=False, default=85)
    training_activated = models.BooleanField(default=False, editable=False)
    predicting_activated = models.BooleanField(default=False, editable=False)
    is_quering = models.BooleanField(default=False, editable=False)

    technics = (
        ('RandomSampling', 'RandomSampling'),
        ('UncertaintySampling', 'UncertaintySampling'),
        ('ClusterBasedSampling', 'ClusterBasedSampling'),
        ('OutlierSampling', 'OutlierSampling'),
        ('RepresentativeSampling', 'RepresentativeSampling'),
        ('UncertaintyWithClusteringSampling', 'UncertaintyWithClusteringSampling'),
        ('UncertaintyWithModelOutliersSampling', 'UncertaintyWithModelOutliersSampling'),
        ('RepresentativeWithClusteringSampling','RepresentativeWithClusteringSampling'),
        ('HighestEntropyClusteringSampling', 'HighestEntropyClusteringSampling'),
        ('UncertaintyWithRepresentativeSampling', 'UncertaintyWithRepresentativeSampling'),
        ('HighestEntropyUncertaintySampling', 'HighestEntropyUncertaintySampling'),
        ('OutliersWithRepresentativeSampling', 'OutliersWithRepresentativeSampling'),
    )
    
    query_technic = models.CharField(max_length=50, choices=technics, default='RandomSampling')

    classifiers = (
        ('cnn', 'cnn'),
        ('vgg16', 'vgg16'),
        ('vgg19', 'vgg19'),
        ('resnet50','resnet50'),
        ('resnet50v2', 'resnet50v2'),
        ('xception', 'xception'),
        ('inceptionv3', 'inceptionv3'),
    )

    model = models.CharField(max_length=50, choices=classifiers, default='cnn')


class Iteration(models.Model):
    accuracy = models.FloatField(null=False, default=0)
    id_al= models.ForeignKey(AL, on_delete=models.CASCADE, default = None) 