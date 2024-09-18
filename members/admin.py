# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from csvexport.actions import csvexport
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from members.models import Member


@admin.action(description="Exportar seleccionados en CSV")
def export_as_csv(modeladmin, request, queryset):
    return csvexport(modeladmin, request, queryset)

@admin.register(Member)
class MemberAdmin(ModelAdmin):
    actions = [csvexport]
    list_display = ["first_name", "last_name", "email", "register_date", ]

