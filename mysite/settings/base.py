"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = [s.strip() for s in os.getenv("ALLOWED_HOSTS", "").split(",")]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core.apps.CoreConfig",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "django_editorjs_fields",
    "fontawesomefree",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.base_template_context_processor",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "ja"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# app_name/staticは各アプリごとの静的ファイルディレクトリ、staticfiles/はcollectstaticしたあとの静的ファイル配信先

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "core.MyUser"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# allauth関係の設定

SITE_ID = 1
AUTHENTICATION_BACKENDS = (
    "allauth.account.auth_backends.AuthenticationBackend",  # 一般ユーザー用
    "django.contrib.auth.backends.ModelBackend",  # 管理サイト用
)

ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_USERNAME_REQUIRED = True

LOGIN_REDIRECT_URL = "core:index"
ACCOUNT_LOGOUT_REDIRECT_URL = "core:index"

# ボタン一発でログアウトする設定
ACCOUNT_LOGOUT_ON_GET = True

# django-allauthが送信するメールの件名に自動付与される接頭辞をブランクにする
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""

# デフォルトのメール送信元
DEFAULT_FROM_EMAIL = os.getenv("FROM_EMAIL")

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# EditorJSの画像アップロード先の設定
EDITORJS_IMAGE_UPLOAD_PATH = "images/"
EDITORJS_IMAGE_UPLOAD_PATH_DATE = "%Y/%m/%d/"

EDITORJS_DEFAULT_PLUGINS = (
    "@editorjs/paragraph",
    "@editorjs/image",
    "@editorjs/header",
    "@editorjs/list",
    "@editorjs/checklist",
    "@editorjs/quote",
    "@editorjs/raw",
    "@editorjs/code",
    "@editorjs/inline-code",
    "@editorjs/embed",
    "@editorjs/delimiter",
    "@editorjs/warning",
    "@editorjs/link",
    "@editorjs/marker",
    "@editorjs/table",
    "editorjs-math",
)

EDITORJS_DEFAULT_CONFIG_TOOLS = {
    "Image": {
        "class": "ImageTool",
        "inlineToolbar": True,
        "config": {
            "endpoints": {
                "byFile": reverse_lazy("editorjs_image_upload"),
                "byUrl": reverse_lazy("editorjs_image_by_url"),
            },
            "additionalRequestHeaders": [{"Content-Type": "multipart/form-data"}],
        },
    },
    "Header": {
        "class": "Header",
        "inlineToolbar": True,
        "config": {
            "placeholder": "見出しを入力...",
            "levels": [2, 3, 4, 5, 6],
            "defaultLevel": 2,
        },
    },
    "Checklist": {"class": "Checklist", "inlineToolbar": True},
    "List": {"class": "List", "inlineToolbar": True},
    "Quote": {"class": "Quote", "inlineToolbar": True},
    "Raw": {"class": "RawTool"},
    "Code": {"class": "CodeTool"},
    "InlineCode": {"class": "InlineCode"},
    "Embed": {"class": "Embed"},
    "Delimiter": {"class": "Delimiter"},
    "Warning": {"class": "Warning", "inlineToolbar": True},
    "LinkTool": {
        "class": "LinkTool",
        "config": {
            "endpoint": reverse_lazy("editorjs_linktool"),
        },
    },
    "Marker": {"class": "Marker", "inlineToolbar": True},
    "Table": {"class": "Table", "inlineToolbar": True},
    "Math": {"class": "MathTex"},
}
