from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from playlist.models import Playlist, Artist, ArtistSource
from playlist.serializers import PlaylistSerializer, ArtistSerializer, ArtistSourceSerializer


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


@csrf_exempt
def playlist_list(request):
    """
    List all playlists or create a new playlist
    """
    # GET /playlists -> return a list of all playlists
    if request.method == 'GET':
        # retreive all playlists from database
        playlists = Playlist.objects.all()
        serializer = PlaylistSerializer(playlists, many=True)
        return JSONResponse(serializer.data, status=200)

    # POST /playlists -> create a playlist
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PlaylistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # 201 created!
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

    return JSONResponse({"msg":"invalid request type"}, status=406)

@csrf_exempt
def playlist_detail(request, primary_key):
    """
    Retrieve, update or delete an individual playlist
    """
    try:
        playlist = Playlist.objects.get(pk=primary_key)
    except Playlist.DoesNotExist:
        return HttpResponse(status=404)

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
        return HttpResponse(status=204)

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
        return HttpResponse(status=404)

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
        return HttpResponse(status=204)

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
        playlist = ArtistSource.objects.get(pk=primary_key)
    except ArtistSource.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ArtistSourceSerializer(playlist)
        return JSONResponse(serializer.data, status=200)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArtistSourceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=200)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        playlist.delete()
        # 204 no content!
        return HttpResponse(status=204)