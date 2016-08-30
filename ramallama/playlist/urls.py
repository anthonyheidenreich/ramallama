from django.conf.urls import url
from playlist import views

urlpatterns = [
    url(r'^v1/playlists/?$', views.playlist_list),
    url(r'^v1/playlists/(?P<pk>[0-9]+)/?$', views.playlist_detail),
    url(r'^v1/artists/?$', views.artist_list),
    url(r'^v1/artists/(?P<pk>[0-9]+)/?$', views.artist_detail),
    url(r'^v1/artist-sources/?$', views.artist_source_list),
    url(r'^v1/artist-sources/(?P<pk>[0-9]+)/?$', views.artist_source_detail),
]
