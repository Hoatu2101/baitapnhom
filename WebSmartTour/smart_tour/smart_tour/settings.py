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

    "site_title": "Travel Admin System",
    "site_header": "Hệ thống Quản lý Tours",
    "site_brand": "Travel Services",
    "welcome_sign": "Chào mừng !",
    "copyright": "Travel Company Ltd",
    "search_model": ["auth.User", "tours.Service"],
    "user_avatar": "get_avatar_url",
    # --- Menu ---
    "topmenu_links": [
        {"name": "Trang chủ", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"model": "tours.Service"},
        {"model": "tours.Booking"},
    ],


    "order_with_respect_to": [
        "tours.Invoice",
        "tours.Booking",
        "tours.Service",
        "tours.Review",
        "tours.User",
        "tours.Role",
    ],


    "icons": {
        "auth": "fas fa-users-cog",

        "tours.User": "fas fa-user-circle",
        "tours.Role": "fas fa-user-tag",

        "tours.Service": "fas fa-globe-asia",

        "tours.Booking": "fas fa-clipboard-list",
        "tours.BookingTour": "fas fa-suitcase-rolling",
        "tours.BookingHotel": "fas fa-hotel",
        "tours.BookingTransport": "fas fa-shuttle-van",

        # Review & Invoice
        "tours.Review": "fas fa-star",
        "tours.Invoice": "fas fa-file-invoice-dollar",
    },

    "default_icon_parents": "fas fa-compass",
    "default_icon_children": "fas fa-map-marker-alt",

    "show_sidebar": True,
    "navigation_expanded": True,
    "changeform_format": "horizontal_tabs",
}


JAZZMIN_UI_TWEAKS = {
    "theme": "cerulean",
    "theme": "flatly",
    "navbar": "navbar-primary navbar-dark",
    "sidebar": "sidebar-light-primary",
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
    cloud_name="dlvwfou7y",
    api_key="539475968685867",
    api_secret="fxQr19ONES9YnIRQmI0FdC0wD5c"
)


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CLIENT_ID = 'ZlVy3clJj8ruazS8Ysl073V67BsPPZ9SUAqWabfd'
CLIENT_SECRET = 'UoAxy8sPjUJm9lVal9fVp9Bvum2fO5GwXlfIGpoeBUnDSLqQU4GMwCNrppFwJPsJwUMqu1N8CGCk6YNTXzCBBIHS0r7N4JhgZxSy7SS6LWH8EVnodcQ7Nz5PBrYWApw0'
