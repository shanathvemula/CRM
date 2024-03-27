from django.db import models
from django.contrib.auth.models import User, Group, Permission
# Create your models here.

class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    building =models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    deleted = models.BooleanField(default=False)