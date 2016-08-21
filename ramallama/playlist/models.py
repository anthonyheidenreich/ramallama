from django.db import models


SOURCE_CHOICES = (('Spotify', 'Spotify'), ('Amazon', 'Amazon'), ('Google', 'Google'))

class Playlist(models.Model):
    name = models.CharField(max_length=200)
    external_id = models.CharField(max_length=100)
    source = models.CharField(choices=SOURCE_CHOICES, max_length=20)
    created_on = models.DateTimeField(auto_now_add=True) 
    updated_on = models.DateTimeField(auto_now=True)
    # owner = 
    def __str__(self):
        return self.name
    class Meta:
        ordering = ('created_on',)

class Song(models.Model):
    title = models.CharField(max_length=200)
    year = models.CharField(max_length=10, blank=True)
    playlists = models.ManyToManyField(Playlist)
    created_on = models.DateTimeField(auto_now_add=True) 
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ('created_on',)

class SongSource(models.Model):
    source = models.CharField(choices=SOURCE_CHOICES, max_length=20)
    external_id = models.CharField(max_length=100)
    preview_url = models.CharField(max_length=200, blank=True)
    created_on = models.DateTimeField(auto_now_add=True) 
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.external_id
    class Meta:
        ordering = ('created_on',)

class Artist(models.Model):
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField(Song)
    created_on = models.DateTimeField(auto_now_add=True) 
    updated_on = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('created_on',)

class ArtistSource(models.Model):
    source = models.CharField(choices=SOURCE_CHOICES, max_length=20)
    external_id = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True) 
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.external_id
    class Meta:
        ordering = ('created_on',)

