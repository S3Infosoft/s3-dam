import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'atnvxcapm%14e+m-o6fk!#o_i4q8yaebpfiko+&2-1=ct!bk6-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['10.1.33.6', "localhost", "mysite.com"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",

    # Packages
    "rest_framework",
    "import_export",
    "easyaudit",
    "debug_toolbar",
    "background_task",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",

    # Apps
    "users.apps.UsersConfig",
    "enquiry.apps.EnquiryConfig",
    "schedules.apps.SchedulesConfig",
    "activities.apps.ActivitiesConfig",
    "apis.apps.ApisConfig",
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # django-easy-audit middleware
    "easyaudit.middleware.easyaudit.EasyAuditMiddleware",
    # django-debug-toolbar middleware
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DB_NAME"),
        "HOST": os.environ.get("DB_HOST"),
        "USER": os.environ.get("DB_USER"),
        "PORT": os.environ.get("DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = os.path.join(BASE_DIR, "static"),
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")

AUTH_USER_MODEL = "users.CustomUser"

LOGIN_URL = "login"
LOGOUT_URL = "logout"

LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "login"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

if os.path.isfile("email.txt"):
    with open("email.txt") as email:
        EMAIL_HOST_USER = email.readline().strip()
        EMAIL_HOST_PASSWORD = email.readline().strip()
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOG_DIR = os.path.join(BASE_DIR, "logs")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "format": {
            "format": "%(levelname)s: %(filename)s: %(asctime)s: %(message)s",
        }
    },

    "handlers": {
        "auth_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOG_DIR + "/auth.log",
            "formatter": "format",
        },
        "api_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOG_DIR + "/api.log",
            "formatter": "format",
        }
    },

    "loggers": {
        "auth": {
            "handlers": ["auth_file"],
            "level": "INFO",
            "propagate": True,
        },
        "api": {
            "handlers": ["api_file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# django-import-export
IMPORT_EXPORT_USE_TRANSACTIONS = True

# django-easy-audit
DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS = False
DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS = False
DJANGO_EASY_AUDIT_UNREGISTERED_CLASSES_EXTRA = ["users.CustomUser"]

# django-debug-toolbar
INTERNAL_IPS = ["localhost"]
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

# if DEBUG:
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True
}


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "TIMEOUT": 75,
        "OPTIONS": {
            "MAX_ENTRIES": 1000
        }
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

BACKGROUND_TASK_RUN_ASYNC = True

# Django-allauth settings
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SOCIALACCOUNT_ADAPTER = "config.adapter.CustomSocialAdapter"
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
