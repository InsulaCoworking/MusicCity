from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^app/$', views.app_info, name='app_info'),
    url(r'^survey/', views.survey, name='survey'),

    url(r'^venues/$', views.venues_list, name='venues_list'),
    url(r'^venues/map/$', views.venues_map_info, name='venues_map_info'),
    url(r'^venues/add/', views.venue_add, name='venue_add'),
    url(r'^venues/(?P<pk>\d+)/$', views.venue_detail, name='venue_detail'),
    url(r'^venues/(?P<pk>\d+)/history/$', views.venue_history, name='venue_history'),
    url(r'^venues/(?P<pk>\d+)/edit/', views.venue_edit, name='venue_edit'),

    url(r'^bands/$', views.bands_list, name='bands_list'),
    url(r'^bands/add$', views.band_add, name='band_add'),
    url(r'^bands/(?P<pk>\d+)/$', views.band_detail, name='band_detail'),
    url(r'^bands/(?P<pk>\d+)/edit/$', views.band_edit, name='band_edit'),
    url(r'^band/edit/(?P<token>\w+)/$', views.edit_band_token, name='edit_band_token'),

    url(r'^agenda/$', views.events_schedule, name='events_schedule'),
    url(r'^events/$', views.events_schedule, name='events'),
    url(r'^events/add/$', views.event_add, name='event_add'),
    url(r'^events/(?P<pk>\d+)/$', views.event_detail, name='event_detail'),
    url(r'^events/(?P<pk>\d+)/edit/$', views.event_edit, name='event_edit'),

    url(r'^pros/$', views.pro_list, name='pros_list'),
    url(r'^pros/map/$', views.pros_map_info, name='pros_map_info'),
    url(r'^pros/(?P<pk>\d+)/$', views.pro_detail, name='pro_detail'),

    # url(r'^billing/$', views.billing_form, name='billing'),
    # url(r'^billing/list/$', views.billing_list, name='billing'),
    # url(r'^billing/download/$', views.download_csv, name='download_csv'),
    url(r'^login/$', auth_views.login, {'redirect_authenticated_user': True }, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),

    url(r'^dashboard/$', views.profile, name='dashboard'),
    url(r'^profile/events$', views.user_events, name='user_events'),
    url(r'^profile/history', views.user_history, name='user_history'),
]