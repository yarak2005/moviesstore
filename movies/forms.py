from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars']
        widgets = {
            'stars': forms.RadioSelect(choices=[(i, f'{i} star{"s" if i != 1 else ""}') for i in range(1, 6)])
        }
