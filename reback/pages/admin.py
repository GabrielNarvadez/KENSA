from django.contrib import admin
from .models import SteelSheet, SteelSheetInspection

@admin.register(SteelSheet)
class SteelSheetAdmin(admin.ModelAdmin):
    list_display = ['lot_number', 'part_name', 'category', 'quantity', 'created_at']
    search_fields = ['lot_number', 'part_name', 'category']
    list_filter = ['category', 'created_at']

@admin.register(SteelSheetInspection)
class SteelSheetInspectionAdmin(admin.ModelAdmin):
    list_display = ('sheet', 'inspector', 'inspection_date', 'surface_deformation', 'scratches_percent', 'dent', 'stain', 'conductivity_test', 'decision')
    search_fields = ('sheet__lot_number', 'inspector__username')
    list_filter = ('decision', 'conductivity_test', 'inspector')