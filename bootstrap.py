from faker import Factory
import argparse
import requests


COMMANDS = {}
def command(func):
    COMMANDS[func.__name__] = func
    return func


class Bootstrap():

    def __init__(self, url):
        self.faker = Factory.create()
        self.url = url

    def _post(self, uri, json={}):
        print('{}/{}'.format(self.url, uri), json)
        r = requests.post('{}/{}/'.format(self.url, uri), json=json)
        return r.json()


    @command
    def playlists(self, number=1):
        """
        Create N playlists
        """
        created = []
        for _ in range(0, number):
            created.append(self.create_playlist())
        return created



    def create_playlist(self):
        """
        Creates a single playlist
        """
        pl = {
            'name': self.faker.sentence(nb_words=4),
            'external_id': self.faker.uuid4(),
            'source': 'Spotify',
        }
        return self._post('playlists', json=pl)


    @command
    def songs(self, number=1):
        """
        Create N Songs with Sources
        """
        created = []
        for _ in range(0, number):
            created.append(self.create_song())
        return created



    def create_song(self):
        """
        Create a single Song with Artist and Source
        """
        artist_obj = self.create_artist()

        source = {
            'source': 'Spotify',
            'external_id': self.faker.uuid4(),
        }
        song = {
            'title': self.faker.sentence(nb_words=4),
            'year': self.faker.year(),
            'artist': artist_obj['id']
        }
        song_response = self._post('songs', json=song)
        source['song'] = song_response.get('id');
        song_source = self._post('song-sources', json=source)
        return song_response


    @command
    def artists(self, number=1):
        """
        Create N Artists with Sources
        """
        created = []
        for _ in range(0, number):
            created.append(self.create_artist())
        return created


    def create_artist(self):
        """
        Create a single Artist with Artist Source
        """
        source = {
            'source': 'Spotify',
            'external_id': self.faker.uuid4(),
        }
        artist = {
            'name': self.faker.name()
        }
        artist_response = self._post('artists', json=artist)
        source['artist'] = artist_response.get('id');
        self._post('artist-sources', json=source)
        return artist_response


    @command
    def playlist_with_songs(self, playlist_count=1):
        """
        Create playlist(s) with some songs
        """
        song_count = 5
        for _ in range(0, playlist_count):
            playlist = self.create_playlist()
            song_list = self.songs(song_count)
            for song in song_list:
                r = self._post('playlists/{}/songs'.format(playlist.get('id')), json={'song': song.get('id')})
                print(r)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Populate data in the APIs')
    parser.add_argument('command', type=str, help='API type for which to generate data. Limit to: {}'.format(', '.join(COMMANDS.keys())))
    parser.add_argument('-u', '--url', dest='url', type=str, default='http://127.0.0.1/v1', help='number of records to create')
    parser.add_argument('-n', '--number', dest='number', type=int, default=1, help='number of records to create')
    args = parser.parse_args()

    bootstrap = Bootstrap(args.url)
    print(getattr(bootstrap, args.command)(args.number))
