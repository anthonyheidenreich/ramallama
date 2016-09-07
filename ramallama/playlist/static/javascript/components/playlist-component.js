angular.
  module('ramallamaApp').
    component('playlist', {
        templateUrl: '/app/templates/playlist.html',
        controller: function PlayListController($scope, $http) {
            var self = this;
            $http.get('/v1/playlists/x').then(function(response)){
                
            }

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