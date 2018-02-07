# coding=utf-8
from django import forms
from django.contrib.auth.models import User
from django.db.models import BLANK_CHOICE_DASH

from bands.models import Band


class ProfileForm(forms.ModelForm):


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'enabled':False }),
        }

