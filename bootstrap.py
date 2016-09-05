from faker import Factory
import argparse
import requests


class Bootstrap():
    commands = {}

    @staticmethod
    def execute(command, args):
        try:
            fake = Factory.create()
            return Bootstrap.commands[command](fake, args.number)
        except Exception as e:
            raise e

    @staticmethod
    def available():
        return Bootstrap.commands.keys()


def command(func):
    Bootstrap.commands[func.__name__] = func
    return func


@command
def playlists(fake, number=1):
    """
    Create N playlists
    """
    created = []
    for _ in range(0, number):
        created.append(create_playlist(fake))
    return created

def create_playlist(fake):
    """
    Creates a single playlist
    """
    pl = {
        'name': fake.sentence(nb_words=4),
        'external_id': fake.uuid4(),
        'source': 'Spotify',
    }
    r = requests.post('http://127.0.0.1/v1/playlists', json=pl)
    return r.json()


@command
def songs(fake, number=1):
    """
    Create N Songs with Sources
    """
    created = []
    for _ in range(0, number):
        created.append(create_song(fake))
    return created

def create_song(fake):
    """
    Create a single Song with Artist and Source
    """
    artist_obj = create_artist(fake)

    source = {
        'source': 'Spotify',
        'external_id': fake.uuid4(),
    }
    song = {
        'title': fake.sentence(nb_words=4),
        'year': fake.year(),
        'artist': artist_obj['id']
    }
    r = requests.post('http://127.0.0.1/v1/songs', json=song)
    song_response = r.json()
    source['song'] = song_response.get('id');
    r = requests.post('http://127.0.0.1/v1/song-sources', json=source)
    return song_response


@command
def artists(fake, number=1):
    """
    Create N Artists with Sources
    """
    created = []
    for _ in range(0, number):
        created.append(create_artist(fake))
    return created

def create_artist(fake):
    """
    Create a single Artist with Artist Source
    """
    source = {
        'source': 'Spotify',
        'external_id': fake.uuid4(),
    }
    artist = {
        'name': fake.name()
    }
    r = requests.post('http://127.0.0.1/v1/artists', json=artist)
    artist_response = r.json()
    source['artist'] = artist_response.get('id');
    r = requests.post('http://127.0.0.1/v1/artist-sources', json=source)
    return artist_response

@command
def playlist_with_songs(fake, playlist_count=1):
    """
    Create playlist(s) with some songs
    """
    song_count = 5
    for _ in range(0, playlist_count):
        playlist = create_playlist(fake)
        song_list = songs(fake, song_count)
        for song in song_list:
            r = requests.post('http://127.0.0.1/v1/playlists/{}/songs'.format(playlist.get('id')), json={'song': song.get('id')})
            print(r.text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Populate data in the APIs')
    parser.add_argument('command', type=str, help='API type for which to generate data. Limit to: {}'.format(', '.join(Bootstrap.available())))
    parser.add_argument('-n', '--number', dest='number', type=int, default=1, help='number of records to create')
    args = parser.parse_args()

    bootstrap = Bootstrap()
    print(bootstrap.execute(args.command, args))
