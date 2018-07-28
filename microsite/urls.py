from django.conf.urls import url
from django.contrib.auth import views as auth_views

from bands.rss.events import NextEventsFeed
from . import views

urlpatterns = [


    url(r'^sp/(?P<slug>[-\w]+)/$', views.microsite_index, name='pro_detail'),

]