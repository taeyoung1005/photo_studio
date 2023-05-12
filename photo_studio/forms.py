from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Album, Photo


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", "phone_number", "first_name", "last_name")

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ("title", "start_date", "last_date", "description")

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ("album", "title", "description", "image")