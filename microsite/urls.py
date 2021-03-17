from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^sp/(?P<slug>[-\w]+)/$', views.microsite_index, name='pro_detail'),

]