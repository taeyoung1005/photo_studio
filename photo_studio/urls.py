from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import index, main, album, album_new, photo_new, signup, download

app_name = 'photo_studio'

urlpatterns = [
    path('', index, name='index'),
    path('main/', main, name='main'),
    path('album/<int:album_id>/', album, name='album'),
    path('album_new/', album_new, name='album_new'),
    # path('album_edit/<int:album_id>/', views.album_edit, name='album_edit'),
    # path('album_delete/<int:album_id>/', views.album_delete, name='album_delete'),
    path('album/<int:album_id>/photo_new/', photo_new, name='photo_new'),
    # path('photo_edit/<int:photo_id>/', views.photo_edit, name='photo_edit'),
    # path('photo_delete/<int:photo_id>/', views.photo_delete, name='photo_delete'),
    path('album/<int:album_id>/download/', download, name='download'),
    
    path('login/', auth_views.LoginView.as_view(template_name='photo_studio/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
]