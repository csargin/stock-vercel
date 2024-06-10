# example/views.py
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Ships
import os

def home(request):
    return render(request, 'home.html',{'api': "" })

def about(request):
    return render(request, 'about.html',{'api': "" })

def about(request):
    return render(request, 'about.html',{'api': "" })

def calendar(request):
    return render(request, 'calendar.html' ,{'api': "" } )
