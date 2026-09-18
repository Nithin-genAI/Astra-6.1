from django.shortcuts import render
# project/myapp/views.py
from django.http import HttpResponse

def home(request):
    return render(request, 'welcome.html')

def music(request):
    return HttpResponse('Hello,Welcome to my Music app!')
