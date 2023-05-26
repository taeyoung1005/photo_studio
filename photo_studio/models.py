from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(primary_key=True, max_length=20, verbose_name="아이디")
    phone_number = models.CharField(max_length=15, verbose_name="전화번호")
    email = models.EmailField(max_length=50, verbose_name="이메일")
    last_login = models.DateTimeField(auto_now=True, verbose_name="최근 접속일")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="가입일")
    first_name = models.CharField(max_length=20, verbose_name="이름")
    last_name = models.CharField(max_length=20, verbose_name="성")
    
    is_staff = models.BooleanField(default=False, verbose_name="관리자 여부")
    is_active = models.BooleanField(default=True, verbose_name="활성화 여부")
    is_superuser = models.BooleanField(default=False, verbose_name="최고 관리자 여부")

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자"
    
class Album(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="사용자")
    title = models.CharField(max_length=50, verbose_name="제목")
    start_date = models.DateField(verbose_name="시작일", blank=True, null=True)
    end_date = models.DateField(verbose_name="종료일", blank=True, null=True)
    description = models.CharField(max_length=100, verbose_name="설명")
    thumbnail = models.ImageField(upload_to="static/thumbnail", verbose_name="썸네일", default="", null=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "앨범"
        verbose_name_plural = "앨범"
    
class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name="앨범")
    title = models.CharField(max_length=50, verbose_name="제목")
    description = models.CharField(max_length=100, verbose_name="설명")
    image = models.ImageField(upload_to="static/img/%Y/%m/%d", verbose_name="이미지")
    property = models.CharField(max_length=50, verbose_name="속성", default="", null=False)
    owner = models.CharField(max_length=20, verbose_name="사용자")
    
    def __str__(self):
        return self.title
    
    def album_title(self):
        return self.album.title
    
    class Meta:
        verbose_name = "사진"
        verbose_name_plural = "사진"

class Photo_templates(models.Model):
    template_url = models.ImageField(upload_to="static/img/templates", verbose_name="템플릿")
    property = models.CharField(max_length=50, verbose_name="속성", default="", null=False)

    def __str__(self):
        return self.template_url.name
    
    class Meta:
        verbose_name = "템플릿"
        verbose_name_plural = "템플릿"