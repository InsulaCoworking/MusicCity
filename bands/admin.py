# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from import_export import resources
from import_export.admin import ExportMixin

from bands.models import Band, Venue, Event, Tag, BandToken, Settings, Professional, ProfessionalTag
from bands.models.billing_info import BillingInfo
from bands.models.news import News

admin.site.register(Band)
admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(Tag)
admin.site.register(BandToken)
admin.site.register(Settings)
admin.site.register(News)
admin.site.register(BillingInfo)
admin.site.register(ProfessionalTag)
admin.site.register(Professional)

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class UserAdmin(ExportMixin, UserAdmin):
    resource_class = UserResource
    pass

admin.site.unregister(User)
admin.site.register(User, UserAdmin)