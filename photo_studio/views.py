from datetime import datetime
from PIL import Image, ExifTags
from django.http import HttpResponse, FileResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from photo_studio.forms import UserForm, UserFormForEdit, AlbumForm, PhotoForm
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
def album_edit(request, album_id):
    context = {}
    context['album_id'] = album_id

    if request.method == "POST":
        form = AlbumForm(request.POST)
        album = Album.objects.get(id=album_id)
        if form.is_valid():
            album.title = form.cleaned_data['title']
            album.start_date = form.cleaned_data['start_date']
            album.last_date = form.cleaned_data['last_date']
            album.description = form.cleaned_data['description']
            album.save()
            return redirect('photo_studio:main')
    else:
        album = Album.objects.get(id=album_id)
        form = AlbumForm(instance=album)
        context['form'] = form
        context['start_date'] = str(album.start_date)
        context['last_date'] = str(album.last_date)
    return render(request, 'photo_studio/album_edit.html', context=context)

@login_required
def album_delete(request, album_id):
    album = Album.objects.get(id=album_id)
    album.delete()
    return redirect('photo_studio:main')

@login_required
def photo_new(request, album_id):
    context = {}
    context['album_id'] = album_id

    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.album = Album.objects.get(id=album_id)
            photo.owner = request.user
            photo.save()
            return redirect('photo_studio:album', album_id=album_id)
        elif "property" not in request.POST:
            messages.error(request, "속성을 선택해주세요.")
    return render(request, 'photo_studio/photo_new.html', context=context)

@login_required
def photo_edit(request, album_id, photo_id):
    context = {}
    context['album_id'] = album_id
    context['photo_id'] = photo_id

    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        photo = Photo.objects.get(id=photo_id)
        if form.is_valid():
            photo.title = form.cleaned_data['title']
            photo.description = form.cleaned_data['description']
            photo.image = form.cleaned_data['image']
            photo.property = form.cleaned_data['property']
            photo.save()
            return redirect('photo_studio:album', album_id=album_id)
        elif "property" not in request.POST:
            messages.error(request, "속성을 선택해주세요.")
    else:
        photo = Photo.objects.get(id=photo_id)
        form = PhotoForm(instance=photo)
        context['form'] = form
    return render(request, 'photo_studio/photo_edit.html', context=context)

@login_required
def photo_delete(request, album_id, photo_id):
    photo = Photo.objects.get(id=photo_id)
    photo.delete()
    return redirect('photo_studio:album', album_id=album_id)

@login_required
def download(request, album_id):
    context = {}
    context['album_id'] = album_id
    response = None
    if request.method == "POST":
        # photo_logo = Image.open('static/img/PhotoStudio.png').resize((650, 270))
        now = datetime.now()
        photo_ids = request.POST.getlist('photo_id')
        photo_list = []
        template_id = request.POST.getlist('template_id')[0]
        template = Photo_templates.objects.get(id=template_id)
        template_property = template.property
        if template_property == '가로':
            template = Image.open(template.template_url).resize((1800, 1200))
            for photo_id in photo_ids:
                photo = Photo.objects.get(id=photo_id)
                photo = Image.open(photo.image).resize((651, 520))
                photo_list.append(photo)

            # 짝수번째
            x_offset = 69
            y_offset = 68
            for photo_id in range(0, len(photo_list), 2):
                template.paste(photo_list[photo_id], (x_offset, y_offset))
                y_offset += 538
            
            # 홀수번째
            x_offset = 738
            y_offset = 68
            for photo_id in range(1, len(photo_list), 2):
                template.paste(photo_list[photo_id], (x_offset, y_offset))
                y_offset += 538

            template.save(f'static/img/merge_image/{now.strftime("%Y-%m-%d_%H_%M_%S")}.png')
            img = open(f'static/img/merge_image/{now.strftime("%Y-%m-%d_%H_%M_%S")}.png', 'rb')
            response = FileResponse(img)
            
        elif template_property == '세로':
            template = Image.open(template.template_url).resize((1200, 1800))
            for photo_id in photo_ids:
                photo = Photo.objects.get(id=photo_id)
                photo = Image.open(photo.image)
                for orientation in ExifTags.TAGS.keys() : 
                    if ExifTags.TAGS[orientation]=='Orientation' : break 
                exif=dict(photo._getexif().items())
                if exif[orientation] == 3 : 
                    photo=photo.rotate(180, expand=True)
                elif exif[orientation] == 6 : 
                    photo=photo.rotate(270, expand=True)
                elif exif[orientation] == 8 : 
                    photo=photo.rotate(90, expand=True)
                photo_list.append(photo.resize((508 , 612)))

            # 짝수번째
            x_offset = 64
            y_offset = 425
            for photo_id in range(0, len(photo_list), 2):
                template.paste(photo_list[photo_id], (x_offset, y_offset))
                y_offset += 637
            
            # 홀수번째
            x_offset = 630
            y_offset = 128
            for photo_id in range(1, len(photo_list), 2):
                template.paste(photo_list[photo_id], (x_offset, y_offset))
                y_offset += 637
            
            template.save(f'static/img/merge_image/{now.strftime("%Y-%m-%d_%H_%M_%S")}.png')
            img = open(f'static/img/merge_image/{now.strftime("%Y-%m-%d_%H_%M_%S")}.png', 'rb')
            response = FileResponse(img)
        return response
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

@login_required
def account(request):
    if request.method == "POST":
        form = UserFormForEdit(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('photo_studio:account')
    else:
        form = UserFormForEdit(instance=request.user)
    return render(request, 'photo_studio/account.html', {'form': form})