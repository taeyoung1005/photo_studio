"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from rest.views import AlbumViewSet, PhotoViewSet

app_name = 'config'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path('^album/(?P<username>.+)/$', AlbumViewSet.as_view()),
    re_path('^photo/(?P<username>.+)/$', PhotoViewSet.as_view()),
    path('', include('photo_studio.urls')),
]

# router = routers.DefaultRouter()
# router.register(r'album', AlbumViewSet)
# router.register(r'photo', PhotoViewSet)

# urlpatterns += router.urls