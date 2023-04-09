
from django.urls import path
from . import views
urlpatterns = [
    path('', views.hello),
    path('register/',views.register),
    path('verifyPhone/',views.verificationPhone),
    path('verify/',views.verify)
]
