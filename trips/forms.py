from django import forms
from .models import Trip
from django.core.exceptions import ValidationError


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            'title',
            'max_persons',
            'price',
            'trip_date_start',
            'trip_date_end',
            'city',
            'description',
            'trip_picture'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'max_persons': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'trip_date_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'trip_date_end': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'trip_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('trip_date_start')
        end = cleaned_data.get('trip_date_end')

        if start and end and end < start:
            raise ValidationError("End date must be after start date.")