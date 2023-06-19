from django.shortcuts import render,HttpResponse
from datetime import *
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
from .models import Customer,Orders
from telesign.messaging import MessagingClient
import string
from random import choice
from .serializers import UserSerializer

# Pin generator for the OTP API
def id_generator():
    chars = string.digits
    random =  ''.join(choice(chars) for _ in range(4))
    return random


# Editing the token with non-relevant user data
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email        
        return token

# Serialize the new token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


#One time pin API
def getOTP(phone):
    code=id_generator()
    customer_id = "ENTER CUSTOMER ID HERE"
    api_key = "SHHHHH...."
    phone_number = f"972{phone}"
    message = f"Welcome to Burger Road App! \nYour one time only Verafication Code is: {code}"
    message_type = "ARN"
    messaging = MessagingClient(customer_id, api_key)
    response = messaging.message(phone_number, message, message_type)
    with open('temp.txt','w')as f:
        f.write(code)
        f.close()

  
#Register function
@api_view(['POST'])
def register(r):
    newUser = User.objects.create(username=r.data['username'],password=make_password(r.data['password']),email=r.data['email'])
    Customer.objects.create(user=newUser)
    return JsonResponse({'userid':newUser.id},safe=False)



# Add phone to customer table and call OTP
@api_view(['POST'])
def verificationPhone(r,userID):
    phone = r.data['phone']
    newphone=str(phone).replace('-','')
    user = User.objects.get(id=userID)
    user.customer.phone = int(newphone)
    user.customer.save() 
# Uncomment here to use your API    
    #getOTP(newphone) 
    userID = {"userID":user.id}  
    return JsonResponse({"data":userID},safe=False)



# Verify OTP code
@api_view(['POST'])
def verify(r):
    return HttpResponse(200)
# Commented out this part to skip verifacation    
    # with open('temp.txt','r')as f:
    #     code1 = f.read()
    # code2 = r.data['code']
    # if code1==code2:
    #     return HttpResponse(200)
    # else:
    #     return HttpResponse(401)

@api_view(['GET'])
def getUserData(r,id):
    user = User.objects.get(id=id)
    data = UserSerializer(user)
 ## Finish implementing the serializers code ##

# Accept new order from client
@api_view(['POST'])
def newOrder(r):
    user = User.objects.get(id = r.data['user'])
    location = r.data['location']
    burgers = r.data['burgers']
    payment = r.data['payment']
    total = r.data['total']
    newOrder = Orders.objects.create(user=user,location=location,burgers=burgers,paymeth=payment,total=total)
   ##create Bill object to return for the client## 
    return HttpResponse(200) 