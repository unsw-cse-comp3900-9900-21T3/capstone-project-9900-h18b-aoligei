"""
Django settings for e_commerce project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0b5sxdud%h5in(&+#2stqoqt17=@s0*7e3$wsn_^7q0k7ew9(f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'mdeditor',
    'embed_video',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # project apps
    'Product',
    'User',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'e_commerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'e_commerce.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': '9900',
#         'USER': 'hello',
#         'PASSWORD': '93239323',
#         'HOST': 'comp9323db.c4ewkd5opwpk.us-east-2.rds.amazonaws.com',
#         'PORT': '3306',
#         'OPTIONS': {
#             "init_command": "SET sql_mode = 'STRICT_TRANS_TABLES ' ",
#         }
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Australia/Sydney'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'Users/login/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

MEDIA_URL = "/media/"

SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False
SIMPLEUI_HOME_QUICK = False
SIMPLEUI_HOME_ACTION = False

SIMPLEUI_LOGO = 'https://github.com/Hankin72/COMP9315_21T1/blob/master/_20t1/LogoMakr-9VRdnu.png?raw=true'
SIMPLEUI_HOME_PAGE = '/products/dashboard/'
SIMPLEUI_HOME_TITLE = 'Website traffic'
SIMPLEUI_HOME_ICON = 'fa fa-eye'


SIMPLEUI_CONFIG = {
    # Whether to use the system default menu, it is recommended to close it when customizing the menu.
    'system_keep': False,

    #  用于菜单排序和过滤, 不填此字段为默认排序和全部显示。空列表[] 为全部不显示.
    'menu_display': ['Product', 'Authentication and Authorization'],

    # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时刷新展示菜单内容。
    # 一般建议关闭。
    'dynamic': False,

    'menus': [
        {
            'app': 'auth',
            'name': 'Authentication and Authorization',
            'icon': 'fas fa-user-shield',
            'models': [
                {
                    'name': 'Users',
                    'icon': 'fa fa-user',
                    'url': 'auth/user/'
                },
                {
                    'name': 'Group',
                    'icon': 'fa fa-th-list',
                    'url': 'auth/group/'
                }
            ]
        },

        {
            'name': 'Product',
            'icon': 'fa fa-th-list',
            'models': [
                {
                    'name': 'Product',
                    'url': 'Product/product/',
                    'icon': 'fa fa-tasks'
                },
                {
                    'name': 'Category',

                    'url': 'Product/category/',
                    'icon': 'fa fa-tasks'
                },
                {
                    'name': 'Rating',
                    'url': 'Product/rating/',
                    'icon': 'fa fa-tasks'
                },
                {
                    'name': 'Format',
                    'url': 'Product/format/',
                    'icon': 'fa fa-tasks'
                },
                {
                    'name': 'Availability',
                    'url': 'Product/availability/',
                    'icon': 'fa fa-tasks'
                },

            ]
        },
    ]
}

EMAIL_HOST = "smtp.163.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = "aoligei_9900@163.com"
EMAIL_HOST_PASSWORD = "LVULKCYNQVNYGQKM"
EMAIL_USE_TLS = False    # 一般都为False
EMAIL_FROM = "aoligei_9900@163.com"