# forms.py
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter task',
            'id': 'id_title'
        })
    )
    priority = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Priority',
            'id': 'id_priority',
            'min': 0
        })
    )

    class Meta:
        model = Task
        fields = ['title', 'priority']
