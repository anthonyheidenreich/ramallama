from rest_framework import serializers
from playlist.models import Playlist, Song, SongSource, Artist, ArtistSource

"""
Serializers can be used to do 2 things:
1. serialize: db -> object -> json
              pass in a playlist object when instantiating a Serializer object
              serializer.data will return the columns as a dictionary
              we can then render that dict into json
2. deserialize: json -> object -> db
                pass in a json object and parse it to create a dict.
                Instantiate a serializer object with the data=the dict
                check if the data is valid with serializer.is_valid()
                save to the db with serialier.save()

ModelSerializer class has create() and update() functions implemented
create(validated_data) : create and return a new playlist instance given the validated data
update(instance, validated_data) : update (in db) and return an existing playlist instance given the validated data
is_valid() : returns a boolean after validating if the data is ok
"""


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('id', 'name', 'external_id', 'source', 'created_on', 'updated_on')


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist', 'year', 'created_on', 'updated_on')


class SongSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongSource
        fields = ('id', 'source', 'song', 'external_id', 'preview_url', 'created_on', 'updated_on')

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name', 'created_on', 'updated_on')

class ArtistSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistSource
        fields = ('id', 'source', 'artist', 'external_id', 'created_on', 'updated_on')
