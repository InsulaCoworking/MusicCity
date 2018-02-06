# coding=utf-8
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import RadioSelect


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Opcional', label='Nombre')
    last_name = forms.CharField(max_length=30, required=False, help_text='Opcional', label='Apellidos')
    email = forms.EmailField(max_length=254, help_text='')
    username = forms.CharField(max_length=254, help_text='', label='Nombre de usuario')

    user_type = forms.ChoiceField(widget=RadioSelect(), choices=(('band','Banda'), ('venue', 'Espacio'), ('pro', 'Profesional')))
    token = forms.CharField(max_length=30, required=False, help_text='Si tenías una banda registrada en AlcaláSuena, '
                                                                     'puedes usar ese token para que los datos que ya '
                                                                     'tenemos de la banda se enlacen a tu cuenta',
                            label='Token de banda')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', )