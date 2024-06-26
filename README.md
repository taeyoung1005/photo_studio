
# 포토 스튜디오

포토 스튜디오는 사용자가 사진 앨범을 생성, 관리, 편집할 수 있는 웹 애플리케이션입니다. 사용자는 사진을 업로드하고 템플릿을 적용하며 합성된 이미지를 다운로드할 수 있습니다. 또한, 사용자 인증 및 계정 관리를 지원합니다.

## 목차
- [소개](#소개)
- [기능](#기능)
- [설치](#설치)
- [사용법](#사용법)
- [구성](#구성)
- [종속성](#종속성)
- [문제 해결](#문제-해결)
- [기여자](#기여자)
- [라이선스](#라이선스)

## 소개
포토 스튜디오는 사용자가 사진을 앨범으로 정리하고, 커스텀 템플릿을 적용하며 합성 이미지를 다운로드할 수 있도록 도와주는 애플리케이션입니다. 이 애플리케이션은 사진 관리를 위한 직관적인 인터페이스를 제공하며, 인증된 사용자에게 다양한 기능을 제공합니다.

## 기능
- 사용자 인증 (회원가입, 로그인, 로그아웃)
- 사진 앨범 생성, 편집, 삭제
- 앨범 내 사진 업로드 및 관리
- 사진에 템플릿 적용
- 합성 이미지 다운로드
- 계정 관리 및 편집

## 설치
로컬에서 포토 스튜디오 애플리케이션을 설정하려면 다음 단계를 따르세요:

1. **저장소 클론:**
   ```bash
   git clone https://github.com/yourusername/photo-studio.git
   cd photo-studio
   ```

2. **종속성 설치:**
   ```bash
   pip install -r requirements.txt
   ```

3. **마이그레이션 실행:**
   ```bash
   python manage.py migrate
   ```

4. **슈퍼유저 생성:**
   ```bash
   python manage.py createsuperuser
   ```

5. **개발 서버 시작:**
   ```bash
   python manage.py runserver
   ```

6. **애플리케이션 접근:**
   웹 브라우저를 열고 `http://127.0.0.1:8000`으로 이동합니다.

## 사용법
### 사용자 인증
- **회원가입:** `/signup/`에서 새로운 사용자 계정을 만듭니다.
- **로그인:** `/login/`에서 계정에 로그인합니다.
- **로그아웃:** `/logout/`에서 계정에서 로그아웃합니다.

### 앨범 관리
- **새 앨범 생성:** `/album/new/`에서 앨범 세부 정보를 입력합니다.
- **앨범 보기:** `/album/<album_id>/`으로 이동합니다.
- **앨범 편집:** `/album_edit/<album_id>/`으로 이동합니다.
- **앨범 삭제:** `/album_delete/<album_id>/`으로 이동합니다.

### 사진 관리
- **새 사진 추가:** `/album/<album_id>/photo_new/`에서 사진을 업로드합니다.
- **사진 편집:** `/album/<album_id>/photo_edit/<photo_id>/`으로 이동합니다.
- **사진 삭제:** `/album/<album_id>/photo_delete/<photo_id>/`으로 이동합니다.

### 합성 이미지 다운로드
- **이미지 다운로드:** `/album/<album_id>/download/`으로 이동하여 사진과 템플릿을 선택하여 합성합니다.

### 계정 관리
- **계정 세부 정보 수정:** `/account/`으로 이동합니다.

## 구성
### 설정
`settings.py`에서 Django 설정을 필요에 맞게 수정합니다.

### 정적 파일
정적 파일이 `STATIC_URL` 및 `STATICFILES_DIRS`에 올바르게 구성되었는지 확인합니다.

### 미디어 파일
사진 업로드를 위한 미디어 파일 처리를 설정합니다:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## 종속성
- Django
- Pillow
- Requests

다음 명령어로 종속성을 설치합니다:
```bash
pip install -r requirements.txt
```

## 문제 해결
- **TemplateDoesNotExist 오류:** 모든 템플릿이 올바른 디렉토리에 있는지 확인합니다.
- **데이터베이스 오류:** 데이터베이스 마이그레이션을 적용하려면 `python manage.py migrate` 명령어를 실행합니다.
- **정적/미디어 파일 문제:** `settings.py`에서 정적 및 미디어 파일 구성을 확인합니다.
