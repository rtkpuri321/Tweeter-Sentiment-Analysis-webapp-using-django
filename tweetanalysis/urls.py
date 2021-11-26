from django.contrib import admin
from django.urls import path
from tweetanalysis import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result.html', views.result, name='result')
]
