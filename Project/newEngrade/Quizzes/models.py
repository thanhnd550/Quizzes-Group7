from django.db import models

# Create your models here.
class Quiz(models.Model):
    title=models.CharField(max_length=50)
    ques=models.CharField(max_length=50)
    ans1=models.CharField(max_length=50)
    ans2=models.CharField(max_length=50)
    ans3=models.CharField(max_length=50)
    ans4=models.CharField(max_length=50)
    correct_ans=models.CharField(max_length=5)

    def __str__(self):
        return self.title