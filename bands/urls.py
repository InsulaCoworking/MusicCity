from django.urls import path
from django.contrib.auth import views as auth_views

from bands.rss.events import NextEventsFeed
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('app/', views.app_info, name='app_info'),
    path('survey/', views.survey, name='survey'),

    path('venues/', views.venues_list, name='venues_list'),
    path('venues/map/', views.venues_map_info, name='venues_map_info'),
    path('venues/add/', views.venue_add, name='venue_add'),
    path('venues/<int:pk>/', views.venue_detail, name='venue_detail'),
    path('venues/<int:pk>/history/', views.venue_history, name='venue_history'),
    path('venues/<int:pk>/edit/', views.venue_edit, name='venue_edit'),

    path('bands/', views.BandList.as_view(), name='bands_list'),
    path('bands/add', views.AddBand.as_view(), name='band_add'),
    path('bands/<int:pk>/', views.BandDetail.as_view(), name='band_detail'),
    path('bands/<int:pk>/edit/', views.BandEdit.as_view(), name='band_edit'),
    path('bands/<int:pk>/update_image/', views.BandImageEdit.as_view(), name='band_update_image'),
    path('band/edit/<token>/', views.edit_band_token, name='edit_band_token'),
    path('bands/link/<token>/', views.link_band, name='link_band'),

    path('agenda/', views.events_schedule, name='events_schedule'),
    path('events/', views.events_schedule, name='events'),
    path('events/add/', views.event_add, name='event_add'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:pk>/<slug:slug>/', views.event_detail, name='event_detail_slug'),

    path('events/feed/', NextEventsFeed(), name='event_feed'),

    path('pros/', views.pro_list, name='pros_list'),
    path('pros/add/', views.pro_add, name='pro_add'),
    path('pros/map/', views.pros_map_info, name='pros_map_info'),
    path('pros/<int:pk>/', views.pro_detail, name='pro_detail'),
    path('pros/<int:pk>/edit/', views.pro_edit, name='pro_edit'),

    # path('billing/', views.billing_form, name='billing'),
    # path('billing/list/', views.billing_list, name='billing'),
    # path('billing/download/', views.download_csv, name='download_csv'),
    path('login/', auth_views.LoginView.as_view(), {'redirect_authenticated_user': True }, name='login'),
    path('logout/',  auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('dashboard/', views.profile, name='dashboard'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path('profile/edit/password', views.profile_save_password, name='profile_save_password'),
    path('profile/events', views.user_events, name='user_events'),
    path('profile/history', views.user_history, name='user_history'),

]