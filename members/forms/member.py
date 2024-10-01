# coding=utf-8
from django import forms

from members.models import Member


class MemberForm(forms.ModelForm):

    class Meta:
        model = Member
        exclude = ['register_date']
        widgets = {
            'favourite_genre': forms.Textarea( attrs={'rows':2}),
            'help_other': forms.Textarea(attrs={'rows': 3}),
            'music_connection': forms.Textarea(attrs={'rows': 3}),
            'comments_extra': forms.Textarea(attrs={'rows': 5})
        }

