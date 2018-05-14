from django.db import models

# Create your models here.
class UserToken(models.Model):

    username = models.CharField(max_length=128)
    token = models.CharField(max_length=64)
    api_token = models.CharField(max_length=128)
