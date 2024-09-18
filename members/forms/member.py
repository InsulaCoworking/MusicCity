# coding=utf-8
from django import forms

from helpers.forms.BootstrapForm import BootstrapForm
from members.models import Member


class MemberForm(forms.ModelForm):

    class Meta:
        model = Member
        exclude = ['register_date']
        widgets = {
            'favourite_genre': forms.Textarea( attrs={'rows':2}),
            'help_other': forms.Textarea(attrs={'rows': 3})
        }

