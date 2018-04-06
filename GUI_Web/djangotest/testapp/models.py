from django.db import models

# Create your models here.


class login(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    secretkey = models.CharField(max_length=100)
    accesskey = models.CharField(max_length=100, default='0000')
