from django.shortcuts import render,HttpResponse
from datetime import *
import os
from random import choice
from django.conf import settings
from django.http import  JsonResponse 
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.core import mail
from django.contrib.auth.models import User
# Create your views here.
def hello(r):
    return HttpResponse("Hello",r)
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email        
        return token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
def register(r):
    newUser = User.objects.create(username=r.data['username'],password=make_password(r.data['password']),email=r.data['email'])
    with open('temp.txt','w')as f:
        f.write(newUser.username)
        f.close()    
    return JsonResponse({'output':f"Welcome aboard {newUser.username} !"},safe=False)

@api_view(['POST'])
def verificationPhone(r):
    with open('temp.txt','r')as f:
        username=f.read()
    user = User.objects.get(username=username)
    print(user.customer)
    user.customer.phone = r.data['phone']
    print(user.customer)
    user.save()    
    return HttpResponse(200)