from django.shortcuts import render
# project/myapp/views.py
from django.http import HttpResponse , JsonResponse
import sqlite3
import os


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
    query = request.GET.get('q', 'Coding')
    category = request.GET.get('category', 'Programming')
    return HttpResponse(f'You searched for: {query} in category: {category}')

#URL parameter captures superhero name and passes to view
def superhero_view(request, hero_name):
    return HttpResponse(f'{hero_name} is here to save the day!')
        
#Query parameter captures superhero power and passes to view
def power_search_view(request):
    power = request.GET.get('power', 'Superman')
    return HttpResponse(f'You searched for the power: {power}')

#custom 404 error handler
def custom_404(request, exception):
    return render(request, '404.html', status=404)

def get_items(request):
    # Create a new SQLite connection for each request
    connection = sqlite3.connect('db.sqlite3')
    items = []
    try:
        # Retrieve items from database
        raw_query = "SELECT * FROM items WHERE name LIKE 'i%'"
        items = connection.execute(raw_query).fetchall()

    finally:
        # Close the connection to ensure it is not reused
        connection.close()

    return HttpResponse(items)

#View to retrieve superheroes from the database
def get_super_webslingers(request):
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite3')
    connection = sqlite3.connect(db_path)
    superheroes = []
    try:
        raw_query = "SELECT * FROM superheroes WHERE superpower='Web-slinging'"
        superheroes = connection.execute(raw_query).fetchall()
    finally:
        connection.close()

    return HttpResponse(superheroes)

