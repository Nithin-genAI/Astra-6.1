from django.shortcuts import render
# project/myapp/views.py
from django.http import HttpResponse , JsonResponse

def home(request):
    return render(request, 'welcome.html')

def music(request):
    return HttpResponse('Hello,Welcome to my Music app!')

def json_view(request):
    data ={
        "message": "Hello, this is a JSON response from the json_view function.",
        "status": "Success",       
        "code": 200
    }
    return JsonResponse(data)
     
#URL parameter captures user name and passes to view
# and also captures query parameter for favorite color and passes to view
def user_view(request, name):
    color = request.GET.get('color','red')
    return HttpResponse(f'Hello, {name}! Your favorite color is {color}.')

#Query parameter captures search query (additional parameter) and passes to view
def search_view(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', 'Programming')
    return HttpResponse(f'You searched for: {query} in category: {category}')