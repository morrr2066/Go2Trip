from django import forms
from .models import Trip

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['title', 'max_persons', 'price', 'trip_date', 'destinations', 'contact_info']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'max_persons': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'trip_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'destinations': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control'}),

        }