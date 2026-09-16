from django.shortcuts import render
# project/myapp/views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse('Hello, Nithin!')
