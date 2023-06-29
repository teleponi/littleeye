from pathlib import Path
import environ
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# hier .env angeben, wenn Docker
environ.Env.read_env(BASE_DIR / ".env")
env = environ.Env(
    DEBUG=(bool, False),
    DOCKER=(bool, False),
)

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
DOCKER = env("DOCKER")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")


if DOCKER:
    DATABASES = {
        "default": {
            "ENGINE": env("SQL_ENGINE", default="django.db.backends.sqlite3"),
            "NAME": env("SQL_DATABASE", default=str(BASE_DIR / "db.sqlite3")),
            "USER": env("SQL_USER", default="user"),
            "PASSWORD": env("SQL_PASSWORD", default="password"),
            "HOST": env("SQL_HOST", default="localhost"),
            "PORT": env("SQL_PORT", default="5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
# Port angabe istwichtig
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1",
    "http://127.0.0.1:1337",
    "https://littleeye.spielprinzip.com",
]

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_bootstrap5",
    "crispy_forms",
    "user",
    "issues",
    "courses",
]

CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# hier unser eigenes User-Model registrieren
AUTH_USER_MODEL = "user.User"
LOGIN_URL = "/accounts/login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    INSTALLED_APPS.extend(["debug_toolbar", "django_extensions"])
    INTERNAL_IPS = ("127.0.0.1",)
    MIDDLEWARE.extend(["debug_toolbar.middleware.DebugToolbarMiddleware"])

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # DIRS: suche auch an diesen Stellen
        "DIRS": [BASE_DIR / "project" / "templates"],
        "APP_DIRS": True,  # APP_DIRS: suche auch in den Apps nach templates
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

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

LANGUAGE_CODE = "de"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True  # Internationalisierung
USE_TZ = True  # speichere Datumsangaben als UTC in der DB


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

WHITENOISE_MANIFEST_STRICT = False  # sidecar not found in manifest 22.11.2022
STATIC_URL = "static/"  # PFAD in der URL (urlpath)
STATICFILES_DIRS = [BASE_DIR / "static"]  # Ort, wo Dateien liegen
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)s %(module)s %(asctime)s %(pathname)s%(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "INFO",
        },
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "gunicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "issues": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
