from tastypie.api import Api

from api.resources import *


def get_api(version_name):

    api = Api(api_name=version_name)

    api.register(BandResource())
    api.register(VenueResource())
    api.register(EventResource())
    api.register(TagResource())
    api.register(SettingsResource())
    api.register(NewsResource())
    api.register(UpcomingEventResource())
    api.register(UpcomingVenueResource())
    api.register(MicrositeResource())

    return api