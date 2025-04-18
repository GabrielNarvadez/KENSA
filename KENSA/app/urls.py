from django.urls import path, include
from app import views 
from django.contrib import admin  

urlpatterns = [
    path('', views.index, name='index'),  # Main index view
    path('admin/', admin.site.urls),  # Django Admin
]