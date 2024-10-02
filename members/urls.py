
from django.urls import path

from . import views

app_name = 'members'
urlpatterns = [
    path('quienes-somos/', views.InfoPage.as_view(), name='who'),
    path('unete/', views.JoinInfoPage.as_view(), name='join'),
    path('bot/', views.BotInfo.as_view(), name='bot_info'),
    path('members/add', views.JoinForm.as_view(), name='add_member'),
    path('members/success', views.JoinFormSuccess.as_view(), name='success'),
]