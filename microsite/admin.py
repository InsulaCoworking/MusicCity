# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from microsite.models import Microsite


from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget


class MicrositeAdminForm(forms.ModelForm):

    class Meta:
        model = Microsite
        exclude = []

    description = forms.CharField(widget=CKEditorWidget())


class MicrositeAdmin(admin.ModelAdmin):
    form = MicrositeAdminForm


admin.site.register(Microsite, MicrositeAdmin)