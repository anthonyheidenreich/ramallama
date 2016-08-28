from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from playlist.models import Playlist
from playilst.serializers import PlaylistSerializer

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
        # 
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





