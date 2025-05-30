"""
Django settings for grocery_api project.

Generated by 'django-admin startproject' using Django 5.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(Path(__file__).resolve().parent.parent.parent / '.env')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Required for django-allauth
    
    # Third-party apps
    'mptt',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.openid_connect',
    'allauth.socialaccount.providers.google',  # Google provider
    'django_extensions',  # Added for development tools
    
    # Local apps
    'core',
    'categories',
    'accounts',
    'products',
    'orders',
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

ROOT_URLCONF = 'grocery_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'grocery_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')

if DATABASE_URL.startswith('sqlite'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # For future use with PostgreSQL, MySQL, etc.
    # You'll need to install dj-database-url for this
    # import dj_database_url
    # DATABASES = {
    #     'default': dj_database_url.parse(DATABASE_URL),
    # }
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Django AllAuth Configuration
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    # Django AllAuth authentication backends
    'allauth.account.auth_backends.AuthenticationBackend',
    # Django's default authentication backend
    'django.contrib.auth.backends.ModelBackend',
]

# AllAuth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Change to 'mandatory' in production
SOCIALACCOUNT_ADAPTER = 'accounts.adapters.CustomSocialAccountAdapter'

# OIDC Provider settings
# Replace these with your actual OIDC provider details
SOCIALACCOUNT_PROVIDERS = {
    'openid_connect': {
        'SERVERS': [
            {
                'id': os.environ.get('OIDC_PROVIDER_ID', 'your-oidc-provider'),
                'name': os.environ.get('OIDC_PROVIDER_NAME', 'Your OIDC Provider'),
                'server_url': os.environ.get('OIDC_SERVER_URL', 'https://your-oidc-provider.com'),
                'client_id': os.environ.get('OIDC_CLIENT_ID', 'your-client-id'),
                'client_secret': os.environ.get('OIDC_CLIENT_SECRET', 'your-client-secret'),
                'redirect_uri': os.environ.get('OIDC_REDIRECT_URI', 'http://localhost:8000/accounts/openid_connect/callback'),
                'authorization_endpoint': os.environ.get('OIDC_AUTHORIZATION_ENDPOINT', 'https://your-oidc-provider.com/authorize'),
                'token_endpoint': os.environ.get('OIDC_TOKEN_ENDPOINT', 'https://your-oidc-provider.com/token'),
                'userinfo_endpoint': os.environ.get('OIDC_USERINFO_ENDPOINT', 'https://your-oidc-provider.com/userinfo'),
                'jwks_uri': os.environ.get('OIDC_JWKS_URI', 'https://your-oidc-provider.com/jwks'),
            }
        ]
    },
    'google': {
        'APP': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID'),
            'secret': os.environ.get('GOOGLE_CLIENT_SECRET', 'YOUR_GOOGLE_CLIENT_SECRET'),
            'key': ''
        },
        'SCOPE': [
            'openid',  # Add OpenID Connect authentication
            'profile',
            'email',
            'phone',  # Add phone scope
            'https://www.googleapis.com/auth/userinfo.profile',  # More detailed profile info
            'https://www.googleapis.com/auth/user.phonenumbers.read',  # Access to phone numbers
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Simple JWT settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.environ.get('JWT_ACCESS_TOKEN_LIFETIME_MINUTES', 60))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.environ.get('JWT_REFRESH_TOKEN_LIFETIME_DAYS', 1))),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# Login/logout redirect URLs
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# DRF Spectacular settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Grocery API',
    'DESCRIPTION': '''
API for a grocery store management system

## Authentication Options

This API supports multiple authentication methods:

1. **JWT Tokens**: Used for API authentication
   - Get a token at `/api/token/`
   - Include in requests as `Authorization: Bearer <token>`

2. **OAuth/Social Authentication**: 
   - View available providers: `/api/accounts/oauth/providers/`
   - OpenID Connect: `/accounts/openid_connect/login/`
   - Google Login: `/api/accounts/oauth/google/`
   
   Callback endpoints:
   - Google Callback: `/api/accounts/oauth/google/callback/` (receives code & state parameters from Google)
''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # Optional UI settings
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
    },
    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,
    # Security scheme definitions
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Enter: "Bearer <JWT token>"',
        },
        'OpenID Connect': {
            'type': 'oauth2',
            'flows': {
                'authorizationCode': {
                    'authorizationUrl': '/accounts/openid_connect/login/',
                    'tokenUrl': '/api/token/',
                    'scopes': {
                        'profile': 'User profile information',
                        'email': 'Email access',
                    }
                }
            }
        }
    },
    # Apply security globally to all operations
    'SECURITY': [{'Bearer': []}],
    # Customize operation tags
    'TAGS': [
        {'name': 'Authentication', 'description': 'Authentication endpoints including OAuth providers'},
        {'name': 'token', 'description': 'JWT token management endpoints'},
    ],
    # Include pattern for callback URLs to ensure they are in the schema
    'SCHEMA_PATH_PREFIX_INSERT': '',
    # Make sure callback endpoints are visible even without explicit schema decoration
    'APPEND_COMPONENTS': {"schemas": {}},
}
