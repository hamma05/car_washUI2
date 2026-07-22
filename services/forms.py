from django import forms
from .models import Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'duration_minutes', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }
        labels = {
            'name': 'Nom',
            'description': 'Description',
            'price': 'Prix',
            'duration_minutes': 'Durée (minutes)',
            'is_active': 'Actif',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'is_active':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
