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
    path('steel-sheets-individual-status/', views.steel_sheet_status, name='steel-sheet-status'),

    #Computer Vision
    path('scan-log/', views.scan_log_view, name='scan-log'),
    path('scan-log/<int:pk>/', views.scan_log_detail, name='scan-log-view'),
    path('scan-log/<int:pk>/edit/', views.scan_log_edit, name='scan-log-edit'),
    path('scan-log/<int:pk>/delete/', views.scan_log_delete, name='scan-log-delete'),


    path('<str:template_name>/', views.dynamic_pages_view, name='dynamic_pages'),
]

print("LOADED reback.pages.urls")
