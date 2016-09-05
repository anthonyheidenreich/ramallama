angular.
  module('ramallamaApp').
    component('playlistList', {
        templateUrl: '/app/templates/playlist-list.html',
        controller: function PlayListController($http) {
            var self = this;
            $http.get('/v1/playlists/').then(function(response) {
                self.playlists = response.data;
            });
        }
      });
