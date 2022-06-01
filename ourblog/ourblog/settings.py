import os
from pathlib import Path

import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = env('SECRET_KEY')


DEBUG = True

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'debug_toolbar',
    'crispy_forms',
    'social_django',
    'blog',
    'mptt',
    'taggit',
    'django_extensions',
    'rest_framework',
    'django_social_share',
    'webpush',
    'users',
]

INSTALLED_APPS += ('django_summernote', )

SITE_ID = 1
INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    '0.0.0.0',
    'localhost',
    # ...
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'ourblog.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                # 'blog.views.category_list',
            ],
        },
    },
]


DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

WSGI_APPLICATION = 'ourblog.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ourblog', 
        'USER': 'postgres', 
        'PASSWORD': env('PASSWORD'),
        'HOST': '127.0.0.1', 
        'PORT': '5432',
    }
}


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',
                            'social_core.backends.github.GithubOAuth2',
                            'social_core.backends.twitter.TwitterOAuth',
                            'social_core.backends.facebook.FacebookOAuth2')

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
CRISPY_TEMPLATE_PACK = 'bootstrap4'


LOGIN_REDIRECT_URL = ''
LOGIN_URL = 'users:login'
ACCOUNT_LOGOUT_REDIRECT_URL ='users:logout'
SUMMERNOTE_THEME = 'bs4'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
SOCIAL_AUTH_LOGIN_ERROR_URL = 'users:settings'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'users:settings'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

SOCIAL_AUTH_GITHUB_KEY = env('client_id')
SOCIAL_AUTH_GITHUB_SECRET = env('client_secret')

X_FRAME_OPTIONS = 'SAMEORIGIN'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_PORT = 2525
EMAIL_HOST_USER = env('EMAIL')
EMAIL_HOST_PASSWORD = env('PASS')
