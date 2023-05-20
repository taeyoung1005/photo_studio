from photo_studio.models import Album, Photo
from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['owner', 'title', 'description']
        extra_kwargs = {'owner': {'read_only': True}, 'title': {'read_only': True}, 'description': {'read_only': True}}

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['album', 'title', 'description', 'owner']
        extra_kwagrs = {'album': {'read_only': True}, 'title': {'read_only': True}, 'description': {'read_only': True}, 'owner': {'read_only': True}}