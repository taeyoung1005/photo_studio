from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import index, main, album, album_new, album_edit, album_delete, photo_new, signup, download, account, photo_edit, photo_delete

app_name = 'photo_studio'

urlpatterns = [
    path('', index, name='index'),
    path('main/', main, name='main'),
    path('album/<int:album_id>/', album, name='album'),
    path('album/new/', album_new, name='album_new'),
    path('album_edit/<int:album_id>/', album_edit, name='album_edit'),
    path('album_delete/<int:album_id>/', album_delete, name='album_delete'),
    path('album/<int:album_id>/photo_new/', photo_new, name='photo_new'),
    path('album/<int:album_id>/photo_edit/<int:photo_id>', photo_edit, name='photo_edit'),
    path('album/<int:album_id>/photo_delete/<int:photo_id>/', photo_delete, name='photo_delete'),
    path('album/<int:album_id>/download/', download, name='download'),

    path('login/', auth_views.LoginView.as_view(template_name='photo_studio/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
    path('account/', account, name='account'),
]
