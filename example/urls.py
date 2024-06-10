# example/urls.py
from django.urls import path
from example import views
from example.views import home

urlpatterns = [
    path('', views.home, name ="home"),
    path('about.html', views.about,name ="about"),
    path('calendar.html', views.calendar, name ="calendar"),

]
