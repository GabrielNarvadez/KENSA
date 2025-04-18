@echo off

:: Define project and app names
set PROJECT_NAME=KENSA
set APP_NAME=app

:: Create the Django project
echo Creating Django project...
django-admin startproject %PROJECT_NAME%
cd %PROJECT_NAME%

:: Create the app
echo Creating Django app...
python manage.py startapp %APP_NAME%

:: Create folders for templates and static files
echo Setting up folders...
mkdir templates
mkdir static
mkdir static\css
mkdir static\js
mkdir static\images

mkdir %APP_NAME%\templates
mkdir %APP_NAME%\templates\%APP_NAME%
mkdir %APP_NAME%\static
mkdir %APP_NAME%\migrations

:: Create base.html
echo Creating base.html...
echo ^<!DOCTYPE html^> > templates\base.html
echo ^<html lang="en"^> >> templates\base.html
echo ^<head^> >> templates\base.html
echo ^    ^<meta charset="UTF-8"^> >> templates\base.html
echo ^    ^<meta name="viewport" content="width=device-width, initial-scale=1.0"^> >> templates\base.html
echo ^    ^<title^>{%% block title %%}KENSA{%% endblock %%}^</title^> >> templates\base.html
echo ^    ^<link rel="stylesheet" href="{%% static 'css/styles.css' %%}"^> >> templates\base.html
echo ^</head^> >> templates\base.html
echo ^<body^> >> templates\base.html
echo ^    ^<header^> >> templates\base.html
echo ^        ^<h1^>Welcome to KENSA^</h1^> >> templates\base.html
echo ^    ^</header^> >> templates\base.html
echo ^    ^<main^>{%% block content %%}{%% endblock %%}^</main^> >> templates\base.html
echo ^</body^> >> templates\base.html
echo ^</html^> >> templates\base.html

:: Create index.html
echo Creating index.html...
echo ^{% extends 'base.html' %} > %APP_NAME%\templates\%APP_NAME%\index.html
echo ^{% block title %}Home{% endblock %} >> %APP_NAME%\templates\%APP_NAME%\index.html
echo ^{% block content %} >> %APP_NAME%\templates\%APP_NAME%\index.html
echo ^<h2^>This is the homepage^</h2^> >> %APP_NAME%\templates\%APP_NAME%\index.html
echo ^{% endblock %} >> %APP_NAME%\templates\%APP_NAME%\index.html

:: Create static CSS file
echo Creating styles.css...
echo body { font-family: Arial, sans-serif; } > static\css\styles.css

:: Configure settings.py
echo Configuring settings.py...
powershell -Command "(gc %PROJECT_NAME%\settings.py) -replace 'INSTALLED_APPS = \[', 'INSTALLED_APPS = [\n    ''%APP_NAME%'',' | sc %PROJECT_NAME%\settings.py"
powershell -Command "(gc %PROJECT_NAME%\settings.py) -replace 'STATIC_URL = ''/static/''', 'STATIC_URL = ''/static/''\nSTATICFILES_DIRS = [BASE_DIR / ''static'']' | sc %PROJECT_NAME%\settings.py"

:: Configure views.py
echo Configuring views.py...
echo from django.shortcuts import render > %APP_NAME%\views.py
echo def index(request): >> %APP_NAME%\views.py
echo     return render(request, '%APP_NAME%/index.html') >> %APP_NAME%\views.py

:: Configure urls.py
echo Configuring app urls.py...
echo from django.urls import path > %APP_NAME%\urls.py
echo from . import views >> %APP_NAME%\urls.py
echo urlpatterns = [ >> %APP_NAME%\urls.py
echo     path('', views.index, name='index'), >> %APP_NAME%\urls.py
echo ] >> %APP_NAME%\urls.py

echo Configuring project urls.py...
powershell -Command "(gc %PROJECT_NAME%\urls.py) -replace 'urlpatterns = \[', 'urlpatterns = [\n    path('', include(''%APP_NAME%.urls'')),' | sc %PROJECT_NAME%\urls.py"

:: Finalizing setup
echo Migrating database...
python manage.py makemigrations
python manage.py migrate

echo Creating superuser...
python manage.py createsuperuser

echo Done! Run the server with 'python manage.py runserver'
