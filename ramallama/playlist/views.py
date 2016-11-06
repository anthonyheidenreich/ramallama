from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import detail_route
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from playlist.models import Playlist, Artist, ArtistSource, Song, SongSource
from playlist.serializers import PlaylistSerializer, ArtistSerializer, ArtistSourceSerializer, SongSerializer, SongSourceSerializer



class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        """
        takes data as a dict
        converts from dict to json
        returns an HTTP response
        """
        json = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(json, **kwargs)


def load(func):
    def retrieve(cls, request, primary_key):
        obj = cls.get_object_class()
        try:
            playlist = obj.objects.get(pk=primary_key)
            return func(cls, request, playlist)
        except cls.get_object_class().DoesNotExist:
            return JSONResponse({'msg': 'not-found'}, status=404)
        except Exception as e:
            return JSONResponse({'msg': 'system-error', 'details': e}, status=500)
    return retrieve


class DefaultViewSet(generics.GenericAPIView):
    object_class = None

    def get_object_class(self):
        """
        Return the class to use for the object.
        Defaults to using `self.object_class`.
        You may want to override this if you need to provide different
        objects depending on the incoming request.
        """
        assert self.object_class is not None, (
            "'%s' should either include a `object_class` attribute, "
            "or override the `get_object_class()` method."
            % self.__class__.__name__
        )

        return self.object_class

    def not_implemented(self, request):
        """
        Not implemented actions
        """
        return JSONResponse({"msg":"invalid-request-type"}, status=405)


class PlaylistList(DefaultViewSet):
    object_class = Playlist
    serializer_class = PlaylistSerializer

    def get(self, request):
        """
        List all playlists
        """
        playlists = self.get_object_class().objects.all()
        serializer = self.get_serializer(playlists, many=True)
        return JSONResponse(serializer.data, status=200)

    def post(self, request):
        """
        Create a new playlist
        """
        data = JSONParser().parse(request)
        serializer = PlaylistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201) # 201 created!
        return JSONResponse(serializer.errors, status=400)


class PlaylistDetails(DefaultViewSet):
    object_class = Playlist
    serializer_class = PlaylistSerializer

    @load
    def get(self, request, playlist):
        """
        Retrieve, update or delete an individual playlist
        """
        serializer = self.get_serializer(playlist)
        return JSONResponse(serializer.data, status=200)

    @load
    def put(self, request, playlist):
        """
        Update an individual playlist
        """
        data = JSONParser().parse(request)
        serializer = PlaylistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=200)
        return JSONResponse(serializer.errors, status=400)

    @load
    def delete(self, request, primary_key):
        """
        Delete an individual playlist
        """
        playlisft.delete()
        return JSONResponse({}, status=204)  # 204 no content!


@csrf_exempt
def playlist_detail(request, primary_key):
    """
    Retrieve, update or delete an individual playlist
    """
    try:
        playlist = Playlist.objects.get(pk=primary_key)
    except Playlist.DoesNotExist:
        return JSONResponse({'msg': 'Not Found'}, status=404)

    # GET /playlists/ID -> return a specific playlist
    if request.method == 'GET':
        serializer = PlaylistSerializer(playlist)
        return JSONResponse(serializer.data, status=200)

    # UPDATE /playlists/ID -> update a specific playlist
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PlaylistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=200)
        return JSONResponse(serializer.errors, status=400)

    # DELETE /playlists/ID -> delete a specific playlist
    elif request.method == 'DELETE':
        playlist.delete()
        # 204 no content!
        return JSONResponse({}, status=204)
    return JSONResponse({"msg":"invalid request type"}, status=406)


@csrf_exempt
def artist_list(request):
    """
    List all artists or create a new artist
    """
    if request.method == 'GET':
        playlists = Artist.objects.all()
        serializer = ArtistSerializer(playlists, many=True)
        return JSONResponse(serializer.data, status=200)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArtistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # 201 created!
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)
    return JSONResponse({"msg":"invalid request type"}, status=406)


@csrf_exempt
def artist_detail(request, primary_key):
    """
    Retrieve, update or delete an individual artist
    """
    try:
        playlist = Artist.objects.get(pk=primary_key)
    except Artist.DoesNotExist:
        return JSONResponse({'msg', 'not-found'}, status=404)

    if request.method == 'GET':
        serializer = ArtistSerializer(playlist)
        return JSONResponse(serializer.data, status=200)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArtistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=200)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        playlist.delete()
        # 204 no content!
        return JSONResponse({}, status=204)
    return JSONResponse({"msg":"invalid request type"}, status=406)


@csrf_exempt
def artist_source_list(request):
    """
    List all artist source or create a new artist source
    """
    if request.method == 'GET':
        playlists = ArtistSource.objects.all()
        serializer = ArtistSourceSerializer(playlists, many=True)
        return JSONResponse(serializer.data, status=200)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArtistSourceSerializer(data=data)
        print("data: {}".format(data))
        print("serializer: {}".format(serializer))
        if serializer.is_valid():
            serializer.save()
            # 201 created!
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)
    return JSONResponse({"msg":"invalid request type"}, status=406)


@csrf_exempt
def artist_source_detail(request, primary_key):
    """
    Retrieve, update or delete an individual artist source
    """
    try:
        artist = ArtistSource.objects.get(pk=primary_key)
    except ArtistSource.DoesNotExist:
        return JSONResponse({'msg': 'not-found'}, status=404)

    if request.method == 'GET':
        serializer = ArtistSourceSerializer(artist)
        return JSONResponse(serializer.data, status=200)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArtistSourceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=200)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        artist.delete()
        # 204 no content!
        return JSONResponse({}, status=204)
    return JSONResponse({"msg":"invalid request type"}, status=406)


@csrf_exempt
def song_list(request):
    """
    List all songs or create a new song
    """
    if request.method == 'GET':
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return JSONResponse(serializer.data, status=200)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SongSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # 201 created!
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)
    return JSONResponse({"msg":"invalid request type"}, status=406)


@csrf_exempt
def song_detail(request, primary_key):
    """
    Retrieve, update or delete an individual song
    """
    try:
        song = Song.objects.get(pk=primary_key)
    except song.DoesNotExist:
        return JSONResponse({'msg': 'not-found'}, status=404)

    if request.method == 'GET':
        serializer = SongSerializer(song)
        return JSONResponse(serializer.data, status=200)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SongSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=200)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        song.delete()
        # 204 no content!
        return JSONResponse({}, status=204)
    return JSONResponse({"msg":"invalid request type"}, status=406)


@csrf_exempt
def song_source_list(request):
    """
    List all song source or create a new song source
    """
    if request.method == 'GET':
        songsources = SongSource.objects.all()
        serializer = SongSourceSerializer(songsources, many=True)
        return JSONResponse(serializer.data, status=200)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SongSourceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # 201 created!
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

    return JSONResponse({"msg":"invalid request type"}, status=406)


@csrf_exempt
def song_source_detail(request, primary_key):
    """
    Retrieve, update or delete an individual song source
    """
    try:
        songsource = SongSource.objects.get(pk=primary_key)
    except SongSource.DoesNotExist:
        return JSONResponse({'msg': 'not-found'}, status=404)

    if request.method == 'GET':
        serializer = SongSourceSerializer(songsource)
        return JSONResponse(serializer.data, status=200)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SongSourceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=200)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        songsource.delete()
        # 204 no content!
        return JSONResponse({}, status=204)
    return JSONResponse({"msg":"invalid request type"}, status=406)


@csrf_exempt
def playlist_songs(request, primary_key):
    """
    Retreive a list of songs from a playlist
    Add a song to a playlist
    """
    try:
        # get the playlist
        playlist = Playlist.objects.get(pk=primary_key)
    except Playlist.DoesNotExist:
        return JSONResponse({'msg': 'not-found'}, status=404)

    if request.method == 'GET':
        songs = playlist.songs
        serializer = SongSerializer(songs, many=True)
        return JSONResponse(serializer.data, status=200)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SongSerializer(data=data)
        # get the song
        song_id = data.get('song')
        try:
            song = Song.objects.get(pk=song_id)
        except Song.DoesNotExist:
            return JSONResponse({'msg': 'not-found'}, status=404)
        # try adding the song to the playlist
        try:
            song.playlists.add(playlist)
            return JSONResponse(SongSerializer(playlist.songs, many=True).data, status=201)
        except Exception as e:
            return JSONResponse({'msg': '{}'.format(e)}, status=500)
    return JSONResponse({"msg":"invalid request type"}, status=406)


@csrf_exempt
def song_playlists(request, primary_key):
    """
    Retrieve a list of playlists that a song belongs to
    """
    try:
        # get the song
        song = Song.objects.get(pk=primary_key)
    except Song.DoesNotExist:
        return JSONResponse({"msg": "Song with ID {} does not exist".format(primary_key)}, status=404)

    if request.method == 'GET':
        playlists = song.playlists
        serializer = PlaylistSerializer(playlists, many=True)
        return JSONResponse(serializer.data, status=200)

    return JSONResponse({"msg":"invalid request type"}, status=406)

