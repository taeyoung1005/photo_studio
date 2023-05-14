from PIL import Image
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from photo_studio.forms import UserForm, AlbumForm, PhotoForm
from .models import Album, Photo, Photo_templates

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
    photos = Photo.objects.filter(album_id=album_id, album__owner=request.user)
    photo_templates = Photo_templates.objects.all()
    
    context['photo_templates'] = photo_templates
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
        elif "property" not in request.POST:
            messages.error(request, "속성을 선택해주세요.")
    return render(request, 'photo_studio/photo_new.html', context=context)

@login_required
def download(request, album_id):
    context = {}
    context['album_id'] = album_id

    if request.method == "POST":
        photo_logo = Image.open('static/img/PhotoStudio.png').resize((650, 270))
        photo_ids = request.POST.getlist('photo_id')
        photo_list = []
        template_id = request.POST.getlist('template_id')[0]
        template_property = Photo_templates.objects.get(id=template_id).property
        property_list = [Photo.objects.get(id=i).property for i in request.POST.getlist('photo_id')]

        if template_property == '가로':
            pass
        elif template_property == '세로':

            for photo_id in photo_ids:
                photo = Photo.objects.get(id=photo_id)
                photo = Image.open(photo.image).resize((400, 300))
                photo_list.append(photo)
            new_image = Image.new('RGB',(950, 950), (0,0,0))
            new_image.paste(photo_logo, (150, 0))

            if len(photo_ids) == 1:
                new_image.paste(photo_list[0], (50, 250))
                new_image.show()
                return redirect('photo_studio:album', album_id=album_id)
            else:
                # 짝수번째
                x_offset = 50
                y_offset = 250
                for photo_id in range(0, len(photo_list), 2):
                    new_image.paste(photo_list[photo_id], (x_offset, y_offset))
                    y_offset += 350
                
                # 홀수번째
                x_offset = 500
                y_offset = 250
                for photo_id in range(1, len(photo_list), 2):
                    new_image.paste(photo_list[photo_id], (x_offset, y_offset))
                    y_offset += 350
                
                new_image.show()
        return redirect('photo_studio:album', album_id=album_id)
    render(request, 'photo_studio/download.html', context=context)

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