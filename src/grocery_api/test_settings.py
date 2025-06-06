import os
from pathlib import Path

from grocery_api.settings import *  # noqa: F401, F403

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "postgres"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "TEST": {
            # Use the same database but with test_ prefixed tables
            "NAME": os.environ.get("POSTGRES_DB", "postgres"),
        },
    }
}

TEST_DATABASE_PREFIX = "test_"

# use an existing database rather than trying to create a new one
TEST_DATABASE_CREATE = False
TEST_DATABASE_NAME = os.environ.get("TEST_POSTGRES_DB", "grocery_api_test")
