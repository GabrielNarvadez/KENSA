# urls.py

from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.root_page_view, name="dashboard"),
    path('steel-sheets-list/', views.SteelSheetListView.as_view(), name='steel-sheet-list'),
    path('steel-sheets/add/', views.SteelSheetCreateView.as_view(), name='steel-sheet-add'),
    path('steel-sheets/<int:pk>/edit/', views.SteelSheetUpdateView.as_view(), name='steel-sheet-edit'),
    path('steel-sheets/<int:pk>/delete/', views.steel_sheet_delete, name='steel-sheet-delete'),
    path('steel-sheets/<int:pk>/', views.SteelSheetDetailView.as_view(), name='steel-sheet-detail'),

    # For inspections
    path('steel-sheets/inspections/', views.steel_sheet_inspection_list, name='steel-sheet-inspection-list'),
    path('steel-sheets/inspection/new/', views.steel_sheet_inspection_create, name='steel-sheet-inspection-create'),
    path('steel-sheets/inspection/<int:pk>/edit/', views.steel_sheet_inspection_edit, name='steel-sheet-inspection-edit'),
    path('steel-sheets/inspection/<int:pk>/delete/', views.steel_sheet_inspection_delete, name='steel-sheet-inspection-delete'),

    path('<str:template_name>/', views.dynamic_pages_view, name='dynamic_pages'),
]
