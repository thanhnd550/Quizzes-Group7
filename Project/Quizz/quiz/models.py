from django.db import models
from django import forms

# Create your models here.

class QuizForm(models.Model):
    def __init__(self, name = "Unknown", time = 10):
        self.name = name
        self.time = time
    def setName(self, name):
        self.name = name
    def setTime(self, time):
        self.time = time
    def __str__(self):
        return "Name: %s; Time: %s" % (self.name, self.time)
