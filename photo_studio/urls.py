from django.urls import path, include
from django.contrib.auth import views as auth_views

from .import views

app_name = 'photo_studio'

urlpatterns = [
    path('', views.index, name='index'),
    path('main/', views.main, name='main'),
    path('album/<int:album_id>/', views.album, name='album'),
    path('album_new/', views.album_new, name='album_new'),
    
    path('login/', auth_views.LoginView.as_view(template_name='photo_studio/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]