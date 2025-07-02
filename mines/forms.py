from django import forms
from .models import Mine

class MineForm(forms.ModelForm):
    class Meta:
        model = Mine
        fields = ['name', 'city' , 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }