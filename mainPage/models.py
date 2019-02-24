from django.contrib.auth.hashers import make_password, check_password
from django.db import models


# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=40)
    mail = models.EmailField(max_length=50)
    isActive=models.BooleanField(default=False)
    uuid=models.CharField(max_length=50)


