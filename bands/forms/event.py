# coding=utf-8
from django import forms
from django.db.models import BLANK_CHOICE_DASH

from bands.models import Venue, Event


class EventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        form = super(EventForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Event
        exclude = ['created_by']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':6}),
            'venue_address': forms.TextInput(attrs={'class': 'form-control'}),
            'venue_name': forms.TextInput(attrs={'class': 'form-control'}),

            'poster': forms.FileInput(attrs={}),

            'bands': forms.HiddenInput(),
            'venue': forms.HiddenInput(),

            'day': forms.DateInput(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'class': 'form-control'}),

            'price': forms.NumberInput(attrs={'class': 'form-control text-right', 'placeholder':0.00}),
            'price_preorder': forms.NumberInput(attrs={'class': 'form-control text-right', 'placeholder':0.00}),
            'ticket_link': forms.TextInput(attrs={'class': 'form-control'}),
        }

