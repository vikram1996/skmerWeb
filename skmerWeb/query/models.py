from django.db import models
from skmerApp.models import skmerUser
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from django.conf import settings

# Create your models here.

#creates subdirectory : media/<userID>/filename.fastq
def get_upload_path(instance, filename):
    return '{0}/{1}'.format(instance.createUser.pk, filename)


#validates file extension
def validate_file_extension(value):
    if not (value.name.endswith('.fastq') or value.name.endswith('.fna')) :
        raise ValidationError(u'Please upload a fastQ or fna file only')

#input fastq file of skmer
class inputQueryFile(models.Model):
    biologicalName = models.CharField(max_length=100 , blank= True )
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True)
    fileExtension = models.CharField(max_length=10 , blank = True)
    createUser = models.ForeignKey(skmerUser, on_delete=models.CASCADE)
    collectionName = models.CharField(max_length=200 , blank= True )
    fastQ = models.FileField(upload_to=get_upload_path, validators=[validate_file_extension])

    def __str__(self):
        return str(self.pk) +'--'+ self.fastQ.name +self.fileExtension +'--' +self.biologicalName

    def printname(self):
        name = (self.fastQ.name).split('/')[-1]
        return name

@receiver(models.signals.post_delete, sender=inputQueryFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.fastQ:
        if os.path.isfile(instance.fastQ.path):
            os.remove(instance.fastQ.path)


#output txt file of skmer
class analysisFile(models.Model):
    createDateTime = models.DateTimeField(auto_now_add=True, blank=True)
    createUser = models.ForeignKey(skmerUser, on_delete=models.CASCADE)
    createInputFile = models.ForeignKey(inputQueryFile, on_delete=models.CASCADE)
    analysis = models.FileField()
    distanceEdit = models.FileField(upload_to=get_upload_path)
    distanceJukesCantor = models.FileField(upload_to=get_upload_path)

@receiver(post_delete, sender=analysisFile)
def submission_delete(sender, instance, **kwargs):
    instance.distanceEdit.delete(False)
    instance.distanceJukesCantor.delete(False)