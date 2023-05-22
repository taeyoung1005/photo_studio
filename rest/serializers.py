from photo_studio.models import Album, Photo
from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['title', 'description']
        extra_kwargs = {'title': {'read_only': True}, 'description': {'read_only': True}}

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['album', 'title', 'description']
        extra_kwagrs = {'album': {'read_only': True}, 'title': {'read_only': True}, 'description': {'read_only': True}}