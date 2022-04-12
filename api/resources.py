from tastypie import fields
from tastypie.fields import IntegerField
from tastypie.resources import ModelResource

from bands.models import Band, Venue, Event, Tag, Settings
from bands.models.news import News
from datetime import datetime


class TagResource(ModelResource):

    class Meta:
        queryset = Tag.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'tag'
        collection_name = 'tag'
        excludes = ['description']


class BandResource(ModelResource):
    tag = fields.ForeignKey(TagResource, 'tag', full=True, null=True)

    class Meta:
        queryset = Band.objects.all()
        list_allowed_methods = ['get']
        resource_name = 'bands'
        collection_name = 'bands'
        include_resource_uri = False

    # Add thumbnail field
    def dehydrate(self, bundle):
        if bundle.obj.profile_thumbnail:
            bundle.data['profile_thumbnail'] = bundle.obj.profile_thumbnail.url
        return bundle

    # Remove the wrapper
    def alter_list_data_to_serialize(self, request, data):
        if self.Meta.collection_name in data and len(data[self.Meta.collection_name]) > 0:
            # only return the first result, avoid the "meta" field
            return data[self.Meta.collection_name]
        else:
            return []


class VenueResource(ModelResource):
    events = fields.ToManyField('api.resources.EventResource', 'venue', full=True, null=True)

    class Meta:
        queryset = Venue.objects.all()
        list_allowed_methods = ['get']
        resource_name = 'venues'
        collection_name = 'venues'
        include_resource_uri = False

    # Add thumbnail field
    def dehydrate(self, bundle):
        if bundle.obj.profile_thumbnail:
            bundle.data['profile_thumbnail'] = bundle.obj.profile_thumbnail.url
        return bundle

    # Remove the wrapper
    def alter_list_data_to_serialize(self, request, data):
        if self.Meta.collection_name in data and len(data[self.Meta.collection_name]) > 0:
            # only return the first result, avoid the "meta" field
            return data[self.Meta.collection_name]
        else:
            return []


class EventResource(ModelResource):
    bands = fields.ManyToManyField('api.resources.BandResource', 'bands', full=False)

    class Meta:
        queryset = Event.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'events'
        collection_name = 'events'

    def dehydrate(self, bundle):
        print(bundle.data)
        cleaned_bands = []
        for band in bundle.data['bands']:
            try:
                # hopefully /api/v1/<resource_name>/<pk>/
                cleaned_bands.append(int(band.split('/')[-2]))
            except:
                pass
        bundle.data['bands'] = cleaned_bands

        return bundle


class UpcomingVenueResource(ModelResource):
    class Meta:
        queryset = Venue.objects.all()
        list_allowed_methods = ['get']
        resource_name = 'upcoming_venues'
        collection_name = 'venues'
        include_resource_uri = False

    # Add thumbnail field
    def dehydrate(self, bundle):
        if bundle.obj.profile_thumbnail:
            bundle.data['profile_thumbnail'] = bundle.obj.profile_thumbnail.url
        return bundle

    # Remove the wrapper
    def alter_list_data_to_serialize(self, request, data):
        if self.Meta.collection_name in data and len(data[self.Meta.collection_name]) > 0:
            # only return the first result, avoid the "meta" field
            return data[self.Meta.collection_name]
        else:
            return []


class UpcomingEventResource(ModelResource):
    bands = fields.ManyToManyField('api.resources.BandResource', 'bands', full=False)
    venues = fields.ForeignKey(UpcomingVenueResource(), 'venue', full=False)

    class Meta:
        queryset = Event.objects.filter(day__gte=datetime.now())
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'upcoming_events'
        collection_name = 'events'


class SettingsResource(ModelResource):
    class Meta:
        queryset = Settings.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'settings'
        collection_name = 'settings'

    def dehydrate(self, bundle):
        return bundle.data['value']


class NewsResource(ModelResource):
    class Meta:
        queryset = News.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'news'
        collection_name = 'news'

    # Remove the wrapper
    def alter_list_data_to_serialize(self, request, data):
        if self.Meta.collection_name in data and len(data[self.Meta.collection_name]) > 0:
            # only return the first result, avoid the "meta" field
            return data[self.Meta.collection_name]
        else:
            return []
