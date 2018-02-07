# coding=utf-8
from django import forms
from django.db.models import BLANK_CHOICE_DASH

from bands.models import Professional


class ProfessionalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        form = super(ProfessionalForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Professional
        exclude = ['user']
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
            'presskit_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Presskit'}),
            'youtube_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Canal de Youtube'}),
            'profile_image': forms.FileInput(attrs={}),
            'embed_code': forms.Textarea(attrs={'class': 'form-control'}),
            'embed_media': forms.Textarea(attrs={'class': 'form-control'}),

            'image': forms.FileInput(attrs={}),
        }

