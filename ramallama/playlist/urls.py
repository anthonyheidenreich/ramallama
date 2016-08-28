from django.conf.urls import url
from playlist import views

urlpatterns = [
    url(r'^playlists/$', views.playlist_list),
    url(r'^playlists/(?P<pk>[0-9]+)/$', views.playlist_detail),
]