from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ciclos/$', views.MicrositeList.as_view(), name='microsite_list'),
    url(r'^sp/(?P<slug>[-\w]+)/$', views.MicrositeIndex.as_view(), name='microsite_index'),

]