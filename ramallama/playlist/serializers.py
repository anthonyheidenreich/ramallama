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

class CustomModelSerializer(serializers.ModelSerializer):

    def error_code(cls, value):
        ERROR_CODE_LOOKUP = {
            'This field is required': 'cannot-be-blank'
        }
        if value in ERROR_CODE_LOOKUP:
            return ERROR_CODE_LOOKUP[value]
        elif value.endswith("is not a valid choice."):
            return 'invalid-choice'
        return 'invalid-input'

    @property
    def errors(cls):
        errors = []
        for key, values in super(serializers.ModelSerializer, cls).errors.items():
            for value in values:
                errors.append({
                    'code': cls.error_code(value),
                    'description': value,
                    'field': key
                })
        return errors


class PlaylistSerializer(CustomModelSerializer):
    class Meta:
        model = Playlist
        fields = ('id', 'name', 'external_id', 'source', 'created_on', 'updated_on')
        read_only = ('created_on', 'updated_on', 'id')


class SongSerializer(CustomModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist', 'year', 'created_on', 'updated_on')
        read_only = ('created_on', 'updated_on', 'id')


class SongSourceSerializer(CustomModelSerializer):
    class Meta:
        model = SongSource
        fields = ('id', 'source', 'song', 'external_id', 'preview_url', 'created_on', 'updated_on')
        read_only = ('created_on', 'updated_on', 'id')


class ArtistSerializer(CustomModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name', 'created_on', 'updated_on')
        read_only = ('created_on', 'updated_on', 'id')


class ArtistSourceSerializer(CustomModelSerializer):
    class Meta:
        model = ArtistSource
        fields = ('id', 'source', 'artist', 'external_id', 'created_on', 'updated_on')
        read_only = ('created_on', 'updated_on', 'id')
