from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from photo_studio.forms import UserForm, AlbumForm, PhotoForm
from .models import Album, Photo

# Create your views here.

def index(request):
    return render(request, 'photo_studio/index.html')

@login_required
def main(request):
    context = {}
    
    albums = Album.objects.filter(owner=request.user)
    
    context['albums'] = albums
    return render(request, 'photo_studio/main.html', context=context)

@login_required
def album(request, album_id):
    context = {}
    
    album_title = Album.objects.get(id=album_id).title
    photos = Photo.objects.filter(album_id=album_id)

    context['album_title'] = album_title
    context['photos'] = photos
    context['album_id'] = album_id
    return render(request, 'photo_studio/album.html', context=context)

@login_required
def album_new(request):
    if request.method == "POST":
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.owner = request.user
            album.save()
            return redirect('photo_studio:main')
    else:
        form = AlbumForm()
    return render(request, 'photo_studio/album_new.html', {'form': form})

@login_required
def photo_new(request, album_id):
    context = {}
    context['album_id'] = album_id

    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.album = Album.objects.get(id=album_id)
            photo.save()
            return redirect('photo_studio:album', album_id=album_id)
    else:
        context['form'] = PhotoForm()
    return render(request, 'photo_studio/photo_new.html', context=context)

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('photo_studio:index')
    else:
        form = UserForm()
    return render(request, 'photo_studio/signup.html', {'form': form})