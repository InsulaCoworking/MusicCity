# coding=utf-8
from django import forms

from bands.models import Event


class EventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(EventForm, self).__init__(*args, **kwargs)

    event_bands = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Event
        exclude = ['created_by']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'venue_address': forms.TextInput(attrs={'class': 'form-control'}),
            'venue_name': forms.TextInput(attrs={'class': 'form-control'}),

            'poster': forms.FileInput(attrs={}),

            'venue': forms.HiddenInput(),

            'day': forms.DateInput(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'class': 'form-control'}),

            'price': forms.NumberInput(attrs={'class': 'form-control text-right', 'placeholder': 0.00}),
            'price_preorder': forms.NumberInput(attrs={'class': 'form-control text-right', 'placeholder': 0.00}),
            'ticket_link': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        if 'venue' in cleaned_data and cleaned_data['venue']:
            cleaned_data['venue_name'] = ''
            cleaned_data['venue_address'] = ''

        return cleaned_data
