from django.conf.urls import url
from . import views          
urlpatterns = [

    url(r'^$', views.index),
    url(r'^regist$', views.regist),
    url(r'^login$', views.login),
    url(r'^travel$', views.success),
    url(r'^logout$', views.logout),
    #works until you log in 
    url(r'^add$', views.add),
    url(r'^join/(?P<id>\d+)$', views.join),
    url(r'dest/(?P<id>\d+)$', views.dest),
    url(r'add_plan$', views.add_plan),

  
  ]

