
from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.register),
    # adding the phone number to the new user
    path('verifyPhone/<int:userID>',views.verificationPhone),
    # verify the phone number 
    path('verify/',views.verify),
    path('order/',views.newOrder)
]
