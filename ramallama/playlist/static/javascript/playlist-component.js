angular.
  module('ramallamaApp').
    component('playlistList', {
        templateUrl: '/app/templates/playlist-list.html',
        controller: function PlayListController($http) {
            var self = this;
            $http.get('/v1/playlists/').then(function(response) {
                self.playlists = response.data;
                angular.forEach(self.playlists, function(playlist) {
                    playlist.songs = []
                    $http.get('/v1/playlists/'+playlist.id+'/songs').then(function(response) {
                        playlist.songs = response.data;
                    });
                });
            });
        }
      });
