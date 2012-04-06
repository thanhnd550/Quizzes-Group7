from django.db import models

# Create your models here.
class Title(models.Model):
    title=models.CharField(max_length=30)
    update_time=models.DateTimeField()
    Time_limit=models.IntegerField()
    def __str__(self):
        return self.id

class Question(models.Model):
    title=models.CharField(max_length=30)
    ques=models.CharField(max_length=100)
    ans1=models.CharField(max_length=100)
    ans2=models.CharField(max_length=100)
    ans3=models.CharField(max_length=100)
    ans4=models.CharField(max_length=100)
    correct_ans=models.CharField(max_length=100)
    number=models.IntegerField()

    def __str__(self):
        return self.title