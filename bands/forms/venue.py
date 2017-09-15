# coding=utf-8
from django import forms
from django.db.models import BLANK_CHOICE_DASH

from bands.models import Venue


class VenueForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        form = super(VenueForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Venue
        exclude = ['owner']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'readonly':True}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'readonly':True}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'public_space': forms.CheckboxInput(attrs={'class': ''}),
            'facebook_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Página de Facebook'}),
            'twitter_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Perfil de Twitter'}),
            'webpage_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Página web'}),
        }

