from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import RadioSelect


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Opcional', label='Nombre')
    last_name = forms.CharField(max_length=30, required=False, help_text='Opcional', label='Apellidos')
    email = forms.EmailField(max_length=254, help_text='')
    username = forms.CharField(max_length=254, help_text='', label='Nombre de usuario')

    user_type = forms.ChoiceField(widget=RadioSelect(), choices=(('band','Banda'), ('venue', 'Espacio')))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', )