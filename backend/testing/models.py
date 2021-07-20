from django.db import models
from als.models import AL
from django.db.models.signals import post_delete
from django.dispatch import receiver

class TestingDataset(models.Model):
	name = models.CharField(max_length=50, null=False, blank=True)
	id_al = models.ForeignKey(AL, on_delete=models.CASCADE, default = None) 

class TestingImage(models.Model):
	image = models.ImageField(upload_to="testing/%Y/%m/%d", null=False, blank=True)
	id_dataset = models.ForeignKey(TestingDataset, on_delete=models.CASCADE, default = None) 
	label = models.BooleanField(default=True)

@receiver(post_delete, sender=TestingImage)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 