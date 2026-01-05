"""
Django settings for smart_tour project.
Django 5.2.7
"""
import os
from pathlib import Path
import pymysql
import cloudinary

# ========================
# BASE DIR
# ========================
BASE_DIR = Path(__file__).resolve().parent.parent

# ========================
# SECURITY
# ========================
SECRET_KEY = 'django-insecure-p_6bt^gw6b*a)am(w20z9ql$ixlyi#wrhzv-c18yc4t5l%4bv$'
DEBUG = True
ALLOWED_HOSTS = []

# ========================
# APPLICATIONS
# ========================
INSTALLED_APPS = [
        'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'tours.apps.ToursConfig',

    'ckeditor',
    'ckeditor_uploader',
    'rest_framework',
    'drf_yasg',
    'oauth2_provider',
]
JAZZMIN_SETTINGS = {

    "site_title": "Xin chào Admin",


    "site_header": "Xin chào",


    "site_brand": "Xin chào",


    "welcome_sign": "Chào mừng bạn quay lại!",


}

AUTH_USER_MODEL = 'tours.User'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'smart_tour.urls'
WSGI_APPLICATION = 'smart_tour.wsgi.application'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # 👈 override admin/login.html
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
pymysql.install_as_MySQLdb()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tourdb',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True


STATIC_URL = 'static/'



MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CKEDITOR_UPLOAD_PATH = "images/ckeditors/"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
        'extraPlugins': 'uploadimage,image2',
    }
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
}

cloudinary.config(
    cloud_name="dxxwcby8l",
    api_key="792844686918347",
    api_secret="T8ys_Z9zaKSqmKWa4K1RY6DXUJg"
)


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CLIENT_ID = 'kOditntahpflHNyaUMLSstRc5KkmZHhN2P0wXf9T'
CLIENT_SECRET = 'Ce79BktaI5NHf4YTf7jmzeARPSSrwA6qFPoTI714R4rWaGmzHvIrGD5pTNy83ZYNAzg11afpRWttldOA8npUQklkC6LhLn9sDVMyZ6N2HCVYBYsGY44RHzyDFOsELvHC'
