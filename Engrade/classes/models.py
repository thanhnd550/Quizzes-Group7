from django.db import models

# Create your models here.
class Class(models.Model):
    name=models.CharField(max_length=40)
    access_number=models.CharField(max_length=20)
    teacher=models.CharField(max_length=20)
    teacher_email=models.CharField(max_length=20)
    permission=models.BooleanField()
class Can_Access_Class(models.Model):
    class_number=models.IntegerField()
    can_access=models.BooleanField()
    user_name=models.CharField(max_length=40)
