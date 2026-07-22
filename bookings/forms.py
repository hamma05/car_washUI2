from django import forms
from .models import Booking
from services.models import Service

SERVICE_CHOICES = [
    ('Lavage interne et externe', 'Lavage interne et externe'),
    ('Lavage externe', 'Lavage externe'),
    ('Lavage rapide', 'Lavage rapide'),
]


class BookingForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    service = forms.ChoiceField(choices=SERVICE_CHOICES)

    class Meta:
        model = Booking
        fields = [
            'customer_name',
            'customer_phone',
            'date',
            'time',
            'notes',
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'customer_name': 'Nom complet',
            'customer_phone': 'Téléphone',
            'service': 'Service',
            'date': 'Date',
            'time': 'Heure',
            'notes': 'Notes',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.service:
            self.initial['service'] = self.instance.service.name
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        instance = super().save(commit=False)
        service_name = self.cleaned_data['service']
        instance.service = Service.objects.get(name=service_name)
        if commit:
            instance.save()
        return instance
