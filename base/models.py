from django.db import models
from datetime import *
from django.contrib.auth.models import User

# The customer fields is added to the User built-in table
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.FloatField(max_length=10,default=0)
    orders = models.JSONField(default=dict)


class Orders(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    location = models.TextField(default='Unknown')
    burgers = models.JSONField()
    appetizers = models.CharField(max_length=20,default='None')
    drinks = models.CharField(max_length=20,default='None')
    payment = models.CharField(max_length=10,default='Unknown')
    total = models.FloatField()
    timestamp = models.TimeField(auto_now=True)
    datestamp = models.DateField(auto_now=True)

class Bills(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    burgers = models.JSONField()
    appetizers = models.CharField(max_length=20,default='None')
    drinks = models.CharField(max_length=20,default='None')
    total = models.FloatField()
