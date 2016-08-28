from rest_framework import serializers
from playlist.models import Playlist, Song, SongSource


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('name', 'external_id', 'source', 'created_on', 'updated_on')


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('title', 'artist', 'year', 'playlists', 'created_on', 'updated_on')


class SongSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongSource
        fields = ('source', 'external_id', 'preview_url', 'created_on', 'updated_on')
