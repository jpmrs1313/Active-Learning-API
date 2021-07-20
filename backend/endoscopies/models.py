from django.db import models
from exams.models import Exam
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Endoscopy(models.Model):
	name = models.CharField(max_length=50, null=False, blank=True)
	id_exam = models.ForeignKey(Exam, on_delete=models.CASCADE, default = None) 


class Frame(models.Model):
	image = models.ImageField(upload_to="endoscopies/%Y/%m/%d", null=False, blank=True)
	id_endoscopy = models.ForeignKey(Endoscopy, on_delete=models.CASCADE, default = None) 

	def __str__(self):
		return self.name


@receiver(post_delete, sender=Frame)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 