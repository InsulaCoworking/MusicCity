# coding=utf-8
from django import forms
from django.db.models import BLANK_CHOICE_DASH
from image_cropping import ImageCropWidget

from bands.helpers import get_url_for_social_network
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

    def clean(self):
        cleaned_data = super().clean()
        networks = ['instagram', 'facebook', 'twitter', 'bandcamp']

        for page in networks:
            field_name = '{}_link'.format(page)
            if cleaned_data[field_name]:
                cleaned_data[field_name] = get_url_for_social_network(cleaned_data[field_name], page)

        return cleaned_data


class BandProfileImageForm(forms.ModelForm):
    class Meta:
        model = Band
        fields = ['profile_image', 'profile_thumb']

        widgets = {
            'profile_image': ImageCropWidget()
        }