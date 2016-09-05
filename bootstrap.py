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
            return "error. {}".format(e)

    @staticmethod
    def available():
        return Bootstrap.commands.keys()


def command(func):
    Bootstrap.commands[func.__name__] = func
    return func


@command
def playlists(fake, number=1):
    created = []
    for _ in range(0, number):
        created.append(playlist(fake))
    return created

def playlist(fake):
    pl = {
        'name': fake.sentence(nb_words=4),
        'external_id': fake.uuid4(),
        'source': 'Spotify',
    }
    r = requests.post('http://127.0.0.1/v1/playlists', json=pl)
    return r.json()


@command
def songs(fake, number=1):
    created = []
    for _ in range(0, number):
        created.append(song(fake))
    return created

def song(fake):
    artist_obj = artist(fake)
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
    created = []
    for _ in range(0, number):
        created.append(artist(fake))
    return created

def artist(fake):
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Populate data in the APIs')
    parser.add_argument('command', type=str, help='API type for which to generate data. Limit to: {}'.format(', '.join(Bootstrap.available())))
    parser.add_argument('-n', '--number', dest='number', type=int, default=1, help='number of records to create')
    args = parser.parse_args()

    bootstrap = Bootstrap()
    print(bootstrap.execute(args.command, args))
