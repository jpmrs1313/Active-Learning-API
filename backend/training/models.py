from django.db import models
from als.models import AL
from django.db.models.signals import post_delete
from django.dispatch import receiver

class TrainingDataset(models.Model):
	name = models.CharField(max_length=50, null=False, blank=True)
	id_al = models.ForeignKey(AL, on_delete=models.CASCADE, default = None) 

class TrainingImage(models.Model):
	image = models.ImageField(upload_to="trainining/%Y/%m/%d", null=False, blank=True)
	id_dataset = models.ForeignKey(TrainingDataset, on_delete=models.CASCADE, default = None) 
	label = models.BooleanField(default=True)

@receiver(post_delete, sender=TrainingImage)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 