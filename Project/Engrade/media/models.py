from django.db import models
from django.core.files.storage import FileSystemStorage

# Create your models here.

class Media(models.Model):
    name=models.CharField(max_length=20)
    image=models.ImageField(upload_to='site_media')
    def __str__(self):
        return self.image

