from django.db import models

# Create your models here.
class Class(models.Model):
    name=models.CharField(max_length=40)
    access_number=models.CharField(max_length=20)
    teacher=models.CharField(max_length=20)
