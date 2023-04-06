from django.db import models
import datetime as time
from django.contrib.auth.models import User
#models.FileField(upload_to='audio/',default='')
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.FloatField(max_length=10,default=None)