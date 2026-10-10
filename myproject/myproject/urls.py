"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

handler404 = 'myapp.views.custom_404'

urlpatterns = [
    path('', views.home, name='home'),
    path('music/',views.music, name='music'),
    path('json/', views.json_view, name='json_view'),
    path('user/<str:name>/', views.user_view, name='user_view'),
    path('search/', views.search_view, name='search_view'),
    path('hero/<str:hero_name>/' , views.superhero_view, name='superhero_view'),
    path('search_power/' ,views.power_search_view, name='power_search_view'),
    path('get_items/',views.get_items,name='get_items'),
    path('admin/', admin.site.urls),
    path('superheroes/', views.get_super_webslingers, name='superhero_view'),
]
