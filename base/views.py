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
from .models import Customer
from telesign.messaging import MessagingClient
import string
from random import choice
from .serializers import UserSerializer


def id_generator():
    chars = string.digits
    random =  ''.join(choice(chars) for _ in range(4))
    return random

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

def getOTP(phone):
    code=id_generator()
    customer_id = "FDDA74F5-2436-422D-94B4-F75F4C8795D6"
    api_key = "Ss/TO9V4jCcwpNCCUhb5PiZvj4eup5hcLEUHqWJ0Fju2qSJJ1Sp59MgcUsa9ihNqikj3O3rRIenNTv04rQNmyQ=="
    phone_number = f"972{phone}"
    message = f"Welcome to Burger Road App! \nYour one time only Verafication Code is: {code}"
    message_type = "ARN"
    messaging = MessagingClient(customer_id, api_key)
    response = messaging.message(phone_number, message, message_type)
    with open('temp.txt','w')as f:
        f.write(code)
        f.close()

  
# Added return userid for later adding phone
@api_view(['POST'])
def register(r):
    newUser = User.objects.create(username=r.data['username'],password=make_password(r.data['password']),email=r.data['email'])
    Customer.objects.create(user=newUser)
    return JsonResponse({'userid':newUser.id},safe=False)

@api_view(['POST'])
def verificationPhone(r,id):
    phone = r.data['phone']
    newphone=str(phone).replace('-','')
    user = User.objects.get(id=id)
    user.customer.phone = int(newphone)
    user.customer.save() 
    getOTP(newphone) 
    userID = {"userID":user.id}  
    return JsonResponse({"data":userID},safe=False)


#  SAVING THE FEW FREE TEXTS...REMEMBER TO UNCOMMENT!
@api_view(['POST'])
def verify(r):
    # return HttpResponse(200)
    with open('temp.txt','r')as f:
        code1 = f.read()
    code2 = r.data['code']
    if code1==code2:
        return HttpResponse(200)
    else:
        return HttpResponse(401)

@api_view(['GET'])
def getUserData(r,id):
    user = User.objects.get(id=id)
    data = UserSerializer(user)
# Finish implementing the serializers code