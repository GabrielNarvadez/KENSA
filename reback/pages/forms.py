# forms.py
from django import forms
from .models import SteelSheetInspection

class SteelSheetInspectionForm(forms.ModelForm):
    class Meta:
        model = SteelSheetInspection
        fields = [
            'sheet',                # FK
            'inspector',            # FK
            'surface_deformation',  # Bool
            'scratches_percent',    # Int
            'dent',                 # Bool
            'stain',                # Bool
            'other_remarks',        # Char
            'conductivity_test',    # Choices
            'decision',             # Choices
            'notes',                # Text
        ]
        widgets = {
            'sheet': forms.Select(attrs={'class': 'form-select'}),
            'inspector': forms.Select(attrs={'class': 'form-select'}),
            'surface_deformation': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'dent': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'stain': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'conductivity_test': forms.Select(attrs={'class': 'form-select'}),
            'decision': forms.Select(attrs={'class': 'form-select'}),
            'other_remarks': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 1, 'style': 'resize:vertical;', 'class': 'form-control'}),
        }
