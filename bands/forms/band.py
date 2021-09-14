# coding=utf-8
from django import forms
from django.db.models import BLANK_CHOICE_DASH

from bands.models import Band


class BandForm(forms.ModelForm):

    class Meta:
        model = Band
        exclude = ['owner']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'public_space': forms.CheckboxInput(attrs={'class': ''}),
            'num_members': forms.NumberInput(attrs={'class': 'form-control'}),
            'facebook_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Página de Facebook'}),
            'youtube_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Canal de Youtube'}),
            'instagram_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Perfil de Instagram'}),
            'twitter_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Perfil de Twitter'}),
            'bandcamp_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Página de BandCamp'}),
            'webpage_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Página web'}),
            'spotify_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Perfil de Spotify'}),
            'presskit_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Presskit'}),
            'profile_image': forms.FileInput(attrs={}),
            'band_image': forms.FileInput(attrs={}),

            'embed_code': forms.Textarea(attrs={'class': 'form-control'}),
            'embed_media': forms.Textarea(attrs={'class': 'form-control'}),


        }

