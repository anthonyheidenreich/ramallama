from django.conf.urls import url
from playlist import views


urlpatterns = [
    url(r'^v1/playlists/?$', views.PlaylistList.as_view(), name="playlist-list"),
    url(r'^v1/playlists/(?P<primary_key>[0-9]+)/?$', views.PlaylistDetails.as_view(), name="playlist-details"),
    url(r'^v1/artists/?$', views.artist_list),
    url(r'^v1/artists/(?P<primary_key>[0-9]+)/?$', views.artist_detail),
    url(r'^v1/artist-sources/?$', views.artist_source_list),
    url(r'^v1/artist-sources/(?P<primary_key>[0-9]+)/?$', views.artist_source_detail),
    url(r'^v1/songs/?$', views.song_list),
    url(r'^v1/songs/(?P<primary_key>[0-9]+)/?$', views.song_detail),
    url(r'^v1/song-sources/?$', views.song_source_list),
    url(r'^v1/song-sources/(?P<primary_key>[0-9]+)/?$', views.song_source_detail),
    url(r'^v1/playlists/(?P<primary_key>[0-9]+)/songs/?$', views.playlist_songs),
    url(r'^v1/songs/(?P<primary_key>[0-9]+)/playlists/?$', views.song_playlists),
]
