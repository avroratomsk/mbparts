"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 3.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from distutils.log import debug
import email
from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i66qhm!jgy*kj2z2ow9r@wv9pwe)!c4s5a6!nnx!m%9*e&w%a('

# SECURITY WARNING: don't run with debug turned on in production!




# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'admin',
    'django.contrib.auth',
    'accounts',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'snowpenguin.django.recaptcha3',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.vk',
    # 'allauth.socialaccount.providers.github',
    'sorl.thumbnail',
    'django_cleanup.apps.CleanupConfig',
    'ckeditor',
    'ckeditor_uploader',
    # 'django.contrib.sites',
    'cart',
    'orders',
    'setup',
    'home',
    'shop',
    'coupons',
    'blog',
    'yafeed',
    'serv',
    'api',
    'ones',
    'pay'
    
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Основные настройки django-allauth
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 5 # Определяет срок действия писем с подтверждением по электронной почте

# ACCOUNT_EMAIL_VERIFICATION = 'mandatory' # Когда установлено «mandatory», пользователь блокируется от входа, пока адрес электронной почты не будет подтвержден.
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 500 # Количество попыток не удачного ввода логина и пароля. После пользователь блокируется.
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300 # Время блокировки пользователя в секундах после количества не удачного ввода логина и пароля. 
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
LOGIN_REDIRECT_URL = '/accounts/profile/'
LOGOUT_REDIRECT_URL = '/'
# ACCOUNT_SIGNUP_FORM_CLASS = 'myaccount.forms.NewSignupForm'


from .set_whitenoise import *



ROOT_URLCONF = 'main.urls'




WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

from .local_settings import DATABASES


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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

from .static_setup import *

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DATE_INPUT_FORMATS = ['%d-%m-%Y']

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            ['Undo', 'Redo',
             '-', 'Bold', 'Italic', 'Underline',
             '-', 'Link', 'Unlink', 'Anchor',
             '-', 'Format',
             '-', 'Maximize',
             '-', 'Table',
             '-', 'Image',
             '-', 'Source',
             '-', 'NumberedList', 'BulletedList'
            ],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',
             '-', 'Font', 'FontSize', 'TextColor',
             '-', 'Outdent', 'Indent',
             '-', 'HorizontalRule',
             '-', 'Blockquote'
            ]
        ],
        'height': 500,
        'width': '100%',
        'toolbarCanCollapse': False,
        'forcePasteAsPlainText': True
    }
}

try:
    import django
    django.setup()
    from setup.models import ThemeSettings
    name = ThemeSettings.objects.get().name
    theme_name = 'core/theme/'+ name +'/views'

except:
    name = 'default'
    theme_name = 'core/theme/'+ name +'/views'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'core/admin/views'),
            os.path.join(BASE_DIR, theme_name)
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'setup.context_processors.setup',
                'setup.context_processors.codes',
                'setup.context_processors.colors',
                'setup.context_processors.theme',
                'shop.context_processors.categorys',
                'shop.context_processors.manufacts',
                'home.context_processors.pages',
                'home.context_processors.vin_form',
                'orders.context_processors.calback_form',

                'cart.context_processors.cart',
            ],
        },
    },
]

try:
    import django
    django.setup()
    from setup.models import BaseSettings
    setup = BaseSettings.objects.get()
    DEBUG = setup.debugging_mode
except:
    DEBUG = True
    

try:
    import django
    django.setup()
    from setup.models import EmailSettings
    email = EmailSettings.objects.get()

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = email.host
    EMAIL_HOST_USER = email.host_user
    EMAIL_HOST_PASSWORD = email.host_password
    EMAIL_FROM = email.host_from 
    EMAIL_PORT = email.host_port 
    EMAIL_USE_SSL = email.use_ssl
    EMAIL_USE_TLS = email.use_tls
    
except:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = '' 
    EMAIL_HOST_USER = '' 
    EMAIL_HOST_PASSWORD = '' 
    EMAIL_FROM = '' 
    EMAIL_PORT = 465 
    EMAIL_USE_SSL = True
    EMAIL_USE_TLS = False


DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

from .local_settings import RECAPTCHA_PUBLIC_KEY
from .local_settings import RECAPTCHA_PRIVATE_KEY
from .local_settings import RECAPTCHA_DEFAULT_ACTION
from .local_settings import RECAPTCHA_LANGUAGE
from .local_settings import RECAPTCHA_SCORE_THRESHOLD



from .local_settings import ALLOWED_HOSTS
from .local_settings import RESET_FILE





CART_SESSION_ID = 'cart'
