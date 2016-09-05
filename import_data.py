import os
from os import listdir
import json
import requests

def main():
    playlists_file_names = listdir('/vagrant/user_playlists')
    tracks_file_names = listdir('/vagrant/playlist_tracks')

    import_artists(tracks_file_names)


def read_from_file(path):
    """
    Read from file path and return list of json objects
    """
    with open(path, 'r') as f:
        data = json.loads(f.read())
    return data

def post(model_type, params):
    """
    Make an http request to populate database 
    """
    pass

def import_artists(tracks_file_names):
    for filename in tracks_file_names:
        path = '/vagrant/playlist_tracks/{}'.format(filename)
        content = read_from_file(path)
        tracks = content['items']
        for track in tracks:
            preview_url = track['preview_url']
            artist_name = track['artist_name']
            track_id = track['track_id']
            track_name = track['track_name']
            artist_id = track['artist_id']

            # create the artist
            artist = {
                "name": artist_name,
            }
            artist_source = {
                "source": "Spotify",
                "external_id": artist_id
            }

            r = requests.post('http://127.0.0.1/v1/artists', json=artist)
            print("STATUS: {}, {}".format(r.status_code, r.text))
            response = r.json()
            # create the artist source
            artist_source['artist'] = response.get('id')
            r = requests.post('http://127.0.0.1/v1/artist-sources', json=artist_source)
            print("STATUS: {}, {}".format(r.status_code, r.text))
            


def import_songs():
    pass

def import_playlists():
    pass

if __name__ == "__main__":
    main()