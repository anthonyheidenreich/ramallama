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
def playlist(fake, number=1):
    for _ in range(0, number):
        pl = {
            'name': fake.sentence(nb_words=4),
            'external_id': fake.uuid4(),
            'source': 'Spotify',
        }
        r = requests.post('http://127.0.0.1/v1/playlists', json=pl)


@command
def song(fake, number=1):
    songs = []
    for _ in range(0, number):
        artist_obj = artist(fake)[0]
        print('foo')
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
        print(r.text)
        song_response = r.json()
        songs.append(song_response)
        source['song'] = song_response.get('id');
        r = requests.post('http://127.0.0.1/v1/song-sources', json=source)
        print(r.text)
    return songs


@command
def artist(fake, number=1):
    artists = []
    for _ in range(0, number):
        source = {
            'source': 'Spotify',
            'external_id': fake.uuid4(),
        }
        artist = {
            'name': fake.name()
        }
        r = requests.post('http://127.0.0.1/v1/artists', json=artist)
        artist_response = r.json()
        artists.append(artist_response)
        source['artist'] = artist_response.get('id');
        r = requests.post('http://127.0.0.1/v1/artist-sources', json=source)
    return artists


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Populate data in the APIs')
    parser.add_argument('command', type=str, help='API type for which to generate data. Limit to: {}'.format(', '.join(Bootstrap.available())))
    parser.add_argument('-n', '--number', dest='number', type=int, default=1, help='number of records to create')
    args = parser.parse_args()

    bootstrap = Bootstrap()
    print(bootstrap.execute(args.command, args))
