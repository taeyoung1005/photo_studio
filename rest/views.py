from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from photo_studio.models import User, Album, Photo
from rest.serializers import AlbumSerializer, PhotoSerializer


class IsOwnerAlbum(permissions.BasePermission):
    def has_permission(self, request, view):
        username = request.user.username
        if username in request.path:
            return True
        else:
            return False

# Create your views here.
class AlbumViewSet(generics.ListAPIView):
    serializer_class = AlbumSerializer
    authenticated = [TokenAuthentication]
    permission_classes = [IsOwnerAlbum, IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']
    
    def get_queryset(self):
        username = self.kwargs['username']
        return Album.objects.filter(owner=username)


class IsOwnerPhoto(permissions.BasePermission):
    def has_permission(self, request, view):
        username = request.user.username
        print(username)
        if username in request.path:
            return True
        else:
            return False

class PhotoViewSet(generics.ListAPIView):
    serializer_class = PhotoSerializer
    authenticated = [TokenAuthentication]
    permission_classes = [IsOwnerPhoto, IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']
    
    def get_queryset(self):
        username = self.kwargs['username']
        return Photo.objects.filter(owner=username)
    