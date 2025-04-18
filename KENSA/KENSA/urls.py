from django.contrib import admin
from django.urls import path
from app.views import (
    index,
    tasks,
    invoice,
    add_customer_view,
    update_customer_view,
    delete_customer_view,
    search_customers_view
)
# Add this import to include the entire views module
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin route
    path('', index, name='index'),  # Index route
    path('tasks/', tasks, name='tasks'),  # Tasks route
    path('invoice/', invoice, name='invoice'),  # Invoice route
    path('add/', add_customer_view, name='add_customer'),  # Add customer
    path('update/', update_customer_view, name='update_customer'),  # Update customer
    path('delete/', delete_customer_view, name='delete_customer'),  # Delete customer
    path('search/', search_customers_view, name='search_customers_view'),  # Search customers
    path('undo/', views.undo_view, name='undo'),  # Undo action
    path('redo/', views.redo_view, name='redo'),  # Redo action
]
