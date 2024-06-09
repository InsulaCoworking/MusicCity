from django.conf.urls import url
from django.contrib.auth import views as auth_views

from bands.rss.events import NextEventsFeed
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

    url(r'^bands/$', views.BandList.as_view(), name='bands_list'),
    url(r'^bands/add$', views.AddBand.as_view(), name='band_add'),
    url(r'^bands/(?P<pk>\d+)/$', views.BandDetail.as_view(), name='band_detail'),
    url(r'^bands/(?P<pk>\d+)/edit/$', views.BandEdit.as_view(), name='band_edit'),
    url(r'^bands/(?P<pk>\d+)/update_image/$', views.BandImageEdit.as_view(), name='band_update_image'),
    url(r'^band/edit/(?P<token>\w+)/$', views.edit_band_token, name='edit_band_token'),
    url(r'^bands/link/(?P<token>\w+)/$', views.link_band, name='link_band'),

    url(r'^agenda/$', views.events_schedule, name='events_schedule'),
    url(r'^events/$', views.events_schedule, name='events'),
    url(r'^events/add/$', views.event_add, name='event_add'),
    url(r'^events/(?P<pk>\d+)/$', views.event_detail, name='event_detail'),
    url(r'^events/(?P<pk>\d+)/edit/$', views.event_edit, name='event_edit'),
    url(r'^events/(?P<pk>\d+)/(?P<slug>[-\w\d]+)/$', views.event_detail, name='event_detail_slug'),

    url(r'^events/feed/$', NextEventsFeed(), name='event_feed'),

    url(r'^pros/$', views.pro_list, name='pros_list'),
    url(r'^pros/add/$', views.pro_add, name='pro_add'),
    url(r'^pros/map/$', views.pros_map_info, name='pros_map_info'),
    url(r'^pros/(?P<pk>\d+)/$', views.pro_detail, name='pro_detail'),
    url(r'^pros/(?P<pk>\d+)/edit/$', views.pro_edit, name='pro_edit'),

    # url(r'^billing/$', views.billing_form, name='billing'),
    # url(r'^billing/list/$', views.billing_list, name='billing'),
    # url(r'^billing/download/$', views.download_csv, name='download_csv'),
    url(r'^login/$', auth_views.LoginView.as_view(), {'redirect_authenticated_user': True }, name='login'),
    url(r'^logout/$',  auth_views.LogoutView.as_view(), name='logout'),
    url(r'^register/$', views.register, name='register'),

    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    url(r'^dashboard/$', views.profile, name='dashboard'),
    url(r'^profile/edit$', views.edit_profile, name='edit_profile'),
    url(r'^profile/edit/password$', views.profile_save_password, name='profile_save_password'),
    url(r'^profile/events$', views.user_events, name='user_events'),
    url(r'^profile/history', views.user_history, name='user_history'),

    url(r'^bot/$', views.bot_info, name='bot_info'),
]