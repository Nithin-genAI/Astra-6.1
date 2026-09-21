from django.shortcuts import render
# project/myapp/views.py
from django.http import HttpResponse , JsonResponse

def home(request):
    return render(request, 'welcome.html')

def music(request):
    return HttpResponse('Hello,Welcome to my Music app!')

def json_view(request):
    return JsonResponse({'message': 'Hello, this is a JSON response from the json_view function.'})
     
