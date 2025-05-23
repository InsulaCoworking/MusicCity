from tastypie import fields
from tastypie.fields import IntegerField
from tastypie.resources import ModelResource

from bands.models import Band, Venue, Event, Tag, Settings
from bands.models.news import News
from datetime import datetime, timedelta
from microsite.models.microsite import Microsite
from puput.models import EntryPage


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


class MicrositeResource(ModelResource):

    class Meta:
        queryset = Microsite.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'microsites'
        collection_name = 'microsites'
        excludes = ['description', 'embed_code', 'embed_media', 'events',
                    'primary_bg', 'primary_text', 'secondary_bg', 'secondary_text']


class UpcomingEventResource(ModelResource):
    bands = fields.ManyToManyField('api.resources.BandResource', 'bands', full=True)
    venues = fields.ForeignKey(UpcomingVenueResource, 'venue', full=True, null=True, blank=True)
    microsites = fields.ManyToManyField(MicrositeResource, 'microsites', full=False, null=True, blank=True)

    class Meta:
        queryset = Event.objects.filter(day__gte=datetime.now())
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'upcoming_events'
        collection_name = 'events'

    def dehydrate(self, bundle):
        print(bundle.data)
        cleaned_ids = []
        for microsite in bundle.data['microsites']:
            try:
                # hopefully /api/v1/<resource_name>/<pk>/
                cleaned_ids.append(int(microsite.split('/')[-2]))
            except:
                pass
        bundle.data['microsites'] = cleaned_ids
        return bundle


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


class BlogResource(ModelResource):
    class Meta:
        queryset = EntryPage.objects.filter(date__gte=(datetime.now()-timedelta(days=120)))
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'blog'
        collection_name = 'entries'
