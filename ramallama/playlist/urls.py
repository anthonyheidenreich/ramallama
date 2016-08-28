from django.conf.urls import url
from playlist import views

urlpatterns = [
    url(r'^v1/playlists/?$', views.playlist_list),
    url(r'^v1/playlists/(?P<pk>[0-9]+)/?$', views.playlist_detail),
]
