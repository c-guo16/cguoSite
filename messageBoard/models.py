from django.db import models

# Create your models here.
class publicMessage(models.Model):
    username=models.CharField(max_length=20,default="游客")
    content=models.CharField(max_length=140)
    time=models.DateTimeField(auto_now_add=True)