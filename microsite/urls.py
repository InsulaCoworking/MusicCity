from django.urls import path

from . import views

urlpatterns = [
    path('ciclos/', views.MicrositeList.as_view(), name='microsite_list'),
    path('sp/<slug:slug>/', views.MicrositeIndex.as_view(), name='microsite_index'),

]