from django.db import models
from als.models import AL
from django.db.models.signals import post_delete
from django.dispatch import receiver

class UnlabeledDataset(models.Model):
	name = models.CharField(max_length=50, null=False, blank=True)
	id_al = models.ForeignKey(AL, on_delete=models.CASCADE, default = None) 

class UnlabeledImage(models.Model):
	image = models.ImageField(upload_to="unlabeled/%Y/%m/%d", null=False, blank=True)
	id_dataset = models.ForeignKey(UnlabeledDataset, on_delete=models.CASCADE, default = None) 
	blocked = models.BooleanField(default=False, editable=False)

@receiver(post_delete, sender=UnlabeledImage)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 
# Create your models here.
